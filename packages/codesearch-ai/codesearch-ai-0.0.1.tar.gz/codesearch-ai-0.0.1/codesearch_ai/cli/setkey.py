from codesearch_ai.cli.config import save_config


def setkey(args, config_dict):
    config_dict["CODESEARCH_AI"]["LITELLM_API_KEYS"][args.api_name] = args.api_key
    save_config(config_dict)
    print(f"Set {args.api_name} API key successfully.")
