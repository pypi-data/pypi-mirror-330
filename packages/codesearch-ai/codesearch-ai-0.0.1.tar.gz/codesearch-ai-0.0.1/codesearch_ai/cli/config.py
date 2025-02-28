from os import environ, getenv, makedirs
from os.path import expanduser, join
from subprocess import run
import os

import toml
from dynaconf import Dynaconf

CONFIG_FILENAME = "config.toml"
CONFIG_PATH = "~/.config/codesearch_ai"
CONFIG_DEFAULTS = {
    "SYSTEM_INSTRUCTIONS": "You are a helpful AI assistant.",
    "GLOBAL_IGNORES": [
        '.git', 'node_modules', '__pycache__', '*.pyc',
        'venv', 'env', '.env', '.venv',
        'dist', 'build', '*.egg-info',
        '.DS_Store', 'Thumbs.db', 'package-lock.json'
    ],
    "CONTEXT_FILE_RATIO": 0.9,
    "ACTIVE_MODEL_IS_LOCAL": True,
    "ACTIVE_EMBED_IS_LOCAL": True,
    "OUTPUT_ACCEPTANCE_RETRIES": 1,
    "USE_CGRAG": True,
    "PRINT_CGRAG": False,
    "COMMIT_TO_GIT": False,
    "MODELS_PATH": "~/.local/share/codesearch_ai/models/",
    "EMBED_MODEL": "nomic-embed-text-v1.5.Q5_K_M.gguf",
    "LLM_MODEL": "QwQ-LCoT-7B-Instruct-Q4_0.gguf",
    "LLAMA_CPP_OPTIONS": {
        "n_ctx": 10000,
        "verbose": False,
    },
    "LLAMA_CPP_EMBED_OPTIONS": {
        "n_ctx": 8192,
        "n_batch": 512,
        "verbose": False,
        "rope_scaling_type": 2,
        "rope_freq_scale": 0.75,
    },
    "LLAMA_CPP_COMPLETION_OPTIONS": {
        "frequency_penalty": 1.1,
    },
    "LITELLM_MODEL": "gemini/gemini-1.5-flash-latest",
    "LITELLM_CONTEXT_SIZE": 500000,
    "LITELLM_MODEL_USES_SYSTEM_MESSAGE": False,
    "LITELLM_PASS_THROUGH_CONTEXT_SIZE": False,
    "LITELLM_EMBED_MODEL": "gemini/text-embedding-004",
    "LITELLM_EMBED_CHUNK_SIZE": 2048,
    "LITELLM_EMBED_REQUEST_DELAY": 0,
    "LITELLM_API_KEYS": {
        "GEMINI_API_KEY": "",
        "OPENAI_API_KEY": "",
        "ANTHROPIC_API_KEY": "",
    },
}


def get_file_path(path, filename):
    expanded_path = expanduser(path)
    makedirs(expanded_path, exist_ok=True)
    return join(expanded_path, filename)


def save_config(config_dict):
    with open(get_file_path(CONFIG_PATH, CONFIG_FILENAME), "w") as config_file:
        toml.dump(config_dict, config_file)


def check_defaults(config_dict, defaults_dict):
    for key, value in defaults_dict.items():
        if key not in config_dict.keys():
            config_dict[key] = value
    return config_dict


def clear_config():
    """Clear the current config while preserving model information"""
    config_file_path = get_file_path(CONFIG_PATH, CONFIG_FILENAME)
    existing_config = {}
    
    # Try to read existing config to preserve model information
    try:
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as f:
                existing_config = toml.load(f)
                print(f"Existing config loaded: {existing_config}")  # Debug logging
    except Exception as e:
        print(f"Error reading existing config: {e}")
        pass
    
    # Create new config with defaults
    new_config = {"CODESEARCH_AI": CONFIG_DEFAULTS.copy()}
    
    # Preserve existing model paths and files if they exist
    if "CODESEARCH_AI" in existing_config:
        model_keys = ["MODELS_PATH", "LLM_MODEL", "EMBED_MODEL", 
                     "ACTIVE_MODEL_IS_LOCAL", "ACTIVE_EMBED_IS_LOCAL"]
        for key in model_keys:
            if key in existing_config["CODESEARCH_AI"]:
                new_config["CODESEARCH_AI"][key] = existing_config["CODESEARCH_AI"][key]
                print(f"Preserved {key}: {new_config['CODESEARCH_AI'][key]}")  # Debug logging
    
    # Verify model files exist
    models_path = get_file_path(new_config["CODESEARCH_AI"]["MODELS_PATH"], "")
    llm_model = new_config["CODESEARCH_AI"]["LLM_MODEL"]
    embed_model = new_config["CODESEARCH_AI"]["EMBED_MODEL"]
    
    llm_path = join(models_path, llm_model)
    embed_path = join(models_path, embed_model)
    
    print(f"Checking LLM model path: {llm_path}")
    print(f"Checking Embedding model path: {embed_path}")
    
    if not os.path.exists(llm_path):
        print(f"Warning: LLM model not found at {llm_path}")
    if not os.path.exists(embed_path):
        print(f"Warning: Embedding model not found at {embed_path}")
    
    # Save the new config
    save_config(new_config)
    print(f"Configuration has been reset to defaults while preserving model information at: {config_file_path}")
    return new_config


def config(args, config_dict):
    # List the current configuration
    config_file_path = get_file_path(CONFIG_PATH, CONFIG_FILENAME)
    print(f"Configuration file: {config_file_path}\n")
    print(toml.dumps(config_dict))


def config_clear(args):
    """Clear the configuration file and return to defaults"""
    return clear_config()


def config_open(args):
    config_file_path = get_file_path(CONFIG_PATH, CONFIG_FILENAME)
    editor = (
        getenv("VISUAL") or getenv("EDITOR") or "nano"
    )  # Default to nano if EDITOR not set
    run([editor, config_file_path])


def load_config():
    """Load configuration from file, with support for dynamic updates"""
    config_file_path = get_file_path(CONFIG_PATH, CONFIG_FILENAME)
    
    try:
        # If config file doesn't exist, create it with defaults while preserving models
        if not os.path.exists(config_file_path):
            print(f"Config file not found at {config_file_path}, creating new one")  # Debug logging
            return clear_config()
            
        # Read the current config file
        config_object = Dynaconf(settings_files=[config_file_path])
        config_dict = config_object.as_dict()
        
        # Create a fresh config with our new defaults
        new_config = {"CODESEARCH_AI": CONFIG_DEFAULTS.copy()}
        
        # Preserve model-related settings if they exist
        if "CODESEARCH_AI" in config_dict:
            model_keys = [
                "MODELS_PATH", "LLM_MODEL", "EMBED_MODEL",
                "ACTIVE_MODEL_IS_LOCAL", "ACTIVE_EMBED_IS_LOCAL"
            ]
            for key in model_keys:
                if key in config_dict["CODESEARCH_AI"]:
                    new_config["CODESEARCH_AI"][key] = config_dict["CODESEARCH_AI"][key]
                    print(f"Preserved {key}: {new_config['CODESEARCH_AI'][key]}")
        
        # Verify model paths
        models_path = get_file_path(new_config["CODESEARCH_AI"]["MODELS_PATH"], "")
        llm_model = new_config["CODESEARCH_AI"]["LLM_MODEL"]
        embed_model = new_config["CODESEARCH_AI"]["EMBED_MODEL"]
        
        llm_path = join(models_path, llm_model)
        embed_path = join(models_path, embed_model)
        
        print(f"Verifying model paths:")
        print(f"LLM model path: {llm_path}")
        print(f"Embedding model path: {embed_path}")
        
        if not os.path.exists(llm_path):
            print(f"Warning: LLM model not found at {llm_path}")
        if not os.path.exists(embed_path):
            print(f"Warning: Embedding model not found at {embed_path}")
        
        # Save the updated config
        save_config(new_config)
        print(f"Updated configuration saved to: {config_file_path}")
                
        return new_config
        
    except Exception as e:
        print(f"Error loading config: {str(e)}. Using defaults while preserving model information.")
        return clear_config()
