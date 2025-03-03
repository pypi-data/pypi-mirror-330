### Dabih Python Package

A Command Line Interface tool to interact with the API of the Dabih Data Storage platform published by the Spang Lab (https://github.com/spang-lab/dabih).

The dabih python package allows you to upload, download, search and list files from the Dabih Data Storage platform, directly from the command line. 

#### Installation

**Install from PyPI:**

```bash
pip install dabih
```

**Or install in editable mode:**

After cloning this library, you can install the dabih python package via: 

```bash
pip install -e .
```

#### Set Up Guide

Create a folder named dabih at either ~/.config (create ~/.config if necessary) or at your default XDG_CONFIG_HOME location. In the dabih folder, create a config.yaml file with the following format:

```yaml
base_url: "http://localhost:3000"
token: "your token"
```

Save any dabih private keys (.pem files) in that dabih folder as well. The .pem files should have 'dabih' at some point in their file name or they won't be recognised as dabih private keys.

After completing the setup, run: 
```bash
dabih check
```
to test for URL, token and key-files being valid.

#### Example usage: 

To see all available commands and options:
```bash
dabih
```
Example for uploading or downloading a file:
```bash
dabih upload <path_to_file>
dabih upload <path_to_file> <target_folder_mnemonic>
dabih download <mnemonic>
dabih download <mnemonic> <path_to_target_folder>
```
If no target folder is specified upon upload, the file will be saved in your dabih home directory.
If no target folder is specified upon download, the file will be saved in your current directory.

For additional help, use --help, e.g.:
```bash
dabih download --help
```

For debugging, use -v, e.g.:
```bash
dabih -v token-info
```