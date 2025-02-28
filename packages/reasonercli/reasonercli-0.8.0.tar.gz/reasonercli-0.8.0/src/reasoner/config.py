import os
from pathlib import Path


def config_file_path():
    return Path.home() / ".reasoner"


def read_config_file():
    reasoner_dir = config_file_path()
    reasoner_dir.mkdir(exist_ok=True)
    config_file = reasoner_dir / "config"

    config_data = {}
    if config_file.exists():
        with open(config_file) as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config_data[key] = value

    return config_data


def write_config_file(config_data):
    reasoner_dir = config_file_path()
    reasoner_dir.mkdir(exist_ok=True)
    config_file = reasoner_dir / "config"

    with open(config_file, "w") as f:
        for key, value in config_data.items():
            f.write(f"{key}={value}\n")


def clear_config_file():
    config_file = config_file_path() / "config"
    if config_file.exists():
        config_file.unlink()


def get_env():
    env_file = config_file_path() / ".env"

    env_data = {}
    
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    env_data[key] = value

    return {
        "CLIENT_ID": os.environ.get("CLIENT_ID") or env_data.get("CLIENT_ID") or "client_01GPECHM1J9DMY7WQNKTJ195P6",
        "AUTHORIZATION_URL": os.environ.get("AUTHORIZATION_URL") or env_data.get("AUTHORIZATION_URL") or "https://api.workos.com/user_management/authorize",
        "REASONER_UI_BASE_URL": os.environ.get("REASONER_UI_BASE_URL") or env_data.get("REASONER_UI_BASE_URL") or "https://console.reasoner.com",
        "REASONER_API_BASE_URL":  os.environ.get("REASONER_API_BASE_URL") or env_data.get("REASONER_API_BASE_URL") or "https://api.reasoner.com",
        "REDIRECT_URI": os.environ.get("REDIRECT_URI") or env_data.get("REDIRECT_URI") or "https://console.reasoner.com/auth/callback"
    }
