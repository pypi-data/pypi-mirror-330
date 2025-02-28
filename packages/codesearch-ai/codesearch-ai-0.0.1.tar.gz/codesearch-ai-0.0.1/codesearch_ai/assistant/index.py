import os
import hashlib

import numpy as np
from colorama import Fore, Style
from faiss import IndexFlatL2
from sqlitedict import SqliteDict

from codesearch_ai.cli.config import get_file_path

INDEX_CACHE_FILENAME = "index_cache.sqlite"
INDEX_CACHE_PATH = "~/.cache/codesearch_ai"


TEXT_CHARS = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F})


def is_text_file(filepath):
    return not bool(open(filepath, "rb").read(1024).translate(None, TEXT_CHARS))


def get_text_files(directory=".", ignore_paths=[]):
    text_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in ignore_paths]
        for i, filename in enumerate(files, start=1):
            filepath = os.path.join(root, filename)
            if (
                os.path.isfile(filepath)
                and not any(ignore_path in filepath for ignore_path in ignore_paths)
                and is_text_file(filepath)
            ):
                text_files.append(filepath)
    return text_files


def get_file_hash(contents):
    """Generate a hash of file contents for cache validation"""
    return hashlib.sha256(contents.encode('utf-8')).hexdigest()


def get_cache_key(filepath, embed_model_path=None):
    """Generate a unique cache key that includes directory and model info"""
    abs_path = os.path.abspath(filepath)
    if embed_model_path:
        model_hash = hashlib.sha256(embed_model_path.encode('utf-8')).hexdigest()[:8]
        return f"{abs_path}_{model_hash}"
    return abs_path


def get_files_with_contents(directory, ignore_paths, cache_db):
    text_files = get_text_files(directory, ignore_paths)
    files_with_contents = []
    with SqliteDict(cache_db, autocommit=True) as cache:
        for filepath in text_files:
            abs_path = os.path.abspath(filepath)
            file_stat = os.stat(abs_path)
            cache_key = get_cache_key(abs_path)
            cached_info = cache.get(cache_key)
            
            # Check if we have a valid cache entry
            if cached_info and cached_info["mtime"] == file_stat.st_mtime:
                files_with_contents.append(cached_info)
                continue
                
            try:
                with open(abs_path, "r") as file:
                    contents = file.read()
                file_hash = get_file_hash(contents)
                
                # Store file info with hash for validation
                file_info = {
                    "filepath": abs_path,
                    "contents": contents,
                    "mtime": file_stat.st_mtime,
                    "hash": file_hash
                }
                cache[cache_key] = file_info
                files_with_contents.append(file_info)
            except UnicodeDecodeError:
                print(
                    f"{Fore.LIGHTBLACK_EX}Skipping {filepath} because it is not a text file.{Style.RESET_ALL}"
                )
                continue
    return files_with_contents


def create_file_index(embed, ignore_paths, embed_chunk_size, extra_dirs=[]):
    cache_db = get_file_path(INDEX_CACHE_PATH, INDEX_CACHE_FILENAME)
    current_dir = os.path.abspath(".")

    print(f"{Fore.LIGHTBLACK_EX}Finding files to index...{Style.RESET_ALL}")
    # Start with current directory
    files_with_contents = get_files_with_contents(current_dir, ignore_paths, cache_db)

    # Add files from additional folders
    for folder in extra_dirs:
        abs_folder = os.path.abspath(folder)
        if os.path.exists(abs_folder):
            folder_files = get_files_with_contents(abs_folder, ignore_paths, cache_db)
            files_with_contents.extend(folder_files)
        else:
            print(
                f"{Fore.YELLOW}Warning: Additional folder {folder} does not exist{Style.RESET_ALL}"
            )

    if not files_with_contents:
        print(
            f"{Fore.YELLOW}Warning: No text files found, creating first-file.txt...{Style.RESET_ALL}"
        )
        with open("first-file.txt", "w") as file:
            file.write(
                "Dir-assistant requires a file to be initialized, so this one was created because "
                "the directory was empty."
            )
        files_with_contents = get_files_with_contents(current_dir, ignore_paths, cache_db)

    chunks = []
    embeddings_list = []
    with SqliteDict(cache_db, autocommit=True) as cache:
        for file_info in files_with_contents:
            filepath = file_info["filepath"]
            cache_key = get_cache_key(filepath, embed.model_path)
            
            cached_data = cache.get(cache_key)
            if cached_data and cached_data["hash"] == file_info["hash"]:
                print(
                    f"{Fore.LIGHTBLACK_EX}Using cached embeddings for {filepath}{Style.RESET_ALL}"
                )
                chunks.extend(cached_data["chunks"])
                embeddings_list.extend(cached_data["embeddings"])
                continue

            print(f"{Fore.LIGHTBLACK_EX}Creating embeddings for {filepath}{Style.RESET_ALL}")
            file_chunks, file_embeddings = process_file(
                embed, filepath, file_info["contents"], embed_chunk_size
            )
            chunks.extend(file_chunks)
            embeddings_list.extend(file_embeddings)
            
            # Cache the results with hash for validation
            cache[cache_key] = {
                "chunks": file_chunks,
                "embeddings": file_embeddings,
                "hash": file_info["hash"],
                "mtime": file_info["mtime"]
            }

    print(f"{Fore.LIGHTBLACK_EX}Creating index from embeddings...{Style.RESET_ALL}")
    embeddings = np.array(embeddings_list)
    index = IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, chunks


def process_file(embed, filepath, contents, embed_chunk_size):
    lines = contents.split("\n")
    current_chunk = ""
    start_line_number = 1
    chunks = []
    embeddings_list = []

    print(f"{Fore.LIGHTBLACK_EX}Creating embeddings for {filepath}{Style.RESET_ALL}")
    for line_number, line in enumerate(lines, start=1):
        # Process each line individually if needed
        line_content = line
        while line_content:
            proposed_chunk = current_chunk + line_content + "\n"
            chunk_header = f"---------------\n\nUser file '{filepath}' lines {start_line_number}-{line_number}:\n\n"
            proposed_text = chunk_header + proposed_chunk
            chunk_tokens = embed.count_tokens(proposed_text)

            if chunk_tokens <= embed_chunk_size:
                current_chunk = proposed_chunk
                break  # The line fits in the current chunk, break out of the inner loop
            else:
                # Split line if too large for a new chunk
                if current_chunk == "":
                    split_point = find_split_point(
                        embed, line_content, embed_chunk_size, chunk_header
                    )
                    current_chunk = line_content[:split_point] + "\n"
                    line_content = line_content[split_point:]
                else:
                    # Save the current chunk as it is, and start a new one
                    chunks.append(
                        {
                            "tokens": embed.count_tokens(chunk_header + current_chunk),
                            "text": chunk_header + current_chunk,
                            "filepath": filepath,
                        }
                    )
                    embedding = embed.create_embedding(chunk_header + current_chunk)
                    embeddings_list.append(embedding)
                    current_chunk = ""
                    start_line_number = line_number  # Next chunk starts from this line
                    # Do not break; continue processing the line

    # Add the remaining content as the last chunk
    if current_chunk:
        chunk_header = f"---------------\n\nUser file '{filepath}' lines {start_line_number}-{len(lines)}:\n\n"
        chunks.append(
            {
                "tokens": embed.count_tokens(chunk_header + current_chunk),
                "text": chunk_header + current_chunk,
                "filepath": filepath,
            }
        )
        embedding = embed.create_embedding(chunk_header + current_chunk)
        embeddings_list.append(embedding)

    return chunks, embeddings_list


def find_split_point(embed, line_content, max_size, header):
    for split_point in range(1, len(line_content)):
        if embed.count_tokens(header + line_content[:split_point] + "\n") >= max_size:
            return split_point - 1
    return len(line_content)


def search_index(embed, index, query, all_chunks):
    query_embedding = embed.create_embedding(query)
    distances, indices = index.search(
        np.array([query_embedding]), 100
    )  # 819,200 tokens max with default embedding
    relevant_chunks = [all_chunks[i] for i in indices[0] if i != -1]
    return relevant_chunks


def clear(args, config_dict):
    cache_db = get_file_path(INDEX_CACHE_PATH, INDEX_CACHE_FILENAME)
    if os.path.exists(cache_db):
        os.remove(cache_db)
        print(f"Deleted {cache_db}")
    else:
        print(f"{cache_db} does not exist.")
