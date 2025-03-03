from dabih.dabih_client.dabih_api_client import AuthenticatedClient

import os
import sys
import yaml
import httpx
import glob
from pathlib import Path
from dabih.logger import dbg, error, warn

__all__ = ["get_client", "find_pem_files", "get_token_and_base_url"]


# Default location for config.yaml file
DEFAULT_CONFIG_DIR = Path.home() / ".config" / "dabih"


def get_config_directory():
    xdg_config_home = os.getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        config_dir = Path(xdg_config_home) / "dabih"
    else:
        config_dir = DEFAULT_CONFIG_DIR

    if not config_dir.exists():
        error(f"The config directory does not exist: {config_dir}; please create it. Default config_dir is home/.config/dabih or XDG_CONFIG_HOME/dabih (see README.md)")
        sys.exit(0)

    dbg(f"Using config directory: {config_dir}")
    return config_dir


def find_pem_files(config_dir):
    pem_files = glob.glob(str(config_dir / "**" / "*dabih*.pem"), recursive=True)
    if not pem_files:
        warn(f"No dabih PEM files found in config directory: {config_dir}\n Private key is required for downloading files.")
        pem_files = glob.glob(str(config_dir / "**" / "**.pem"), recursive=True)
        dbg(pem_files)
        if pem_files:
            warn(f"Found non-dabih PEM files: {pem_files}. Dabih private keys should contain 'dabih' in filename")
            del pem_files[:]
    else:
        dbg(f"Found PEM files: {pem_files}")
    return pem_files


def load_config(config_dir):
    config_file = config_dir / "config.yaml"
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
                return config
        except yaml.YAMLError as e:
            error(f"Error parsing config file: {e}. Plese check the config file at path: {config_file}")
            sys.exit(0)
    else:
        error(f"Config file does not exist: {config_file} at path: {config_dir}; please create a config.yaml as described in README.md")
        sys.exit(0)


def get_token_and_base_url(config):
    try:
        base_url = config.get("base_url")
        token = config.get("token")
    except KeyError as e:
        error(f"Missing key in config file: {e}")
        sys.exit(0)
    return base_url, token

def get_client(test=None):
    config_dir = get_config_directory()
    config = load_config(config_dir)
    base_url, token = get_token_and_base_url(config)
    if not "/api/v1" in base_url:
        base_url = base_url+"/api/v1"
    pem_files = find_pem_files(config_dir)

    client = AuthenticatedClient(base_url=base_url, token=token)
    return client, pem_files
