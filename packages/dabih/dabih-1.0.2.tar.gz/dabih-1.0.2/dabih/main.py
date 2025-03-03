import click
import sys
from .config import *
from .helpers import *
from dabih.logger import setup_logger, dbg, error, warn, log

@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx, verbose):
    setup_logger(verbose)
    client, pem_files = get_client()
    if not healthy_func(client):
        error("Dabih server not healthy")
        dbg(f"client: {client}")
        sys.exit(0)
    else:
        dbg("Dabi server healthy")

    key_files, *_ = get_user_info(client)
    if pem_files:
        pem_files = get_user_key_files(key_files, pem_files)
    ctx.obj = {}
    ctx.obj["client"] = client
    ctx.obj["pem_files"] = pem_files
    return None


@click.command(
    short_help="Check if your current token is valid", 
    help="This command verifies if the current token is valid. If the token is invalid, check for typos, the expiration date of the token at dabih.com/profile, or consult your administrator.\n Usage: dabih token-val"
)
@click.pass_context
def token_val(ctx):
    client = ctx.obj["client"]
    answer = check_token_validity(client)
    if answer:
        log("Token is valid")
    else:
        warn("Token is not valid")
    return None


@click.command(
    short_help="Get current token's scope information",
    help="This command returns the user and role (scope) associated with the current token.\nUsage: dabih token-info"
)
@click.pass_context
def token_info(ctx):
    client = ctx.obj["client"]
    get_token_info(client)
    return None

@click.command(
    short_help="Check user credentials including token and available key files", 
    help="This command verifies the validity of your base URL, token, config.yaml, and key files. This is recommended after setup. See README.md for further assistance.\nUsage: dabih check"
)
@click.pass_context
def check(ctx):
    client = ctx.obj["client"]
    pem_files = ctx.obj["pem_files"]
    check_user_credentials(client, pem_files)
    return None


@click.command(
    short_help="List all files in user's home directory",
    help="This command displays all files and folders in your Dabih home directory, along with the mnemonic for each file and folder.\n Usage: dabih list-home"
)
@click.pass_context
def list_home(ctx):
    client = ctx.obj["client"]
    list_home_func(client)
    return None

@click.command(
    short_help="List all files in specific dabih folder",
    help="This command lists all files in a specified dabih folder. Enter the folder-mnemonic e.g. 'dabih list-files <folder_mnemonic' to see a list of files in that folder",
)
@click.pass_context
@click.argument("mnemonic")
def list_files(ctx, mnemonic):
    client = ctx.obj["client"]
    list_files_func(mnemonic, client)


@click.command(
    short_help="Upload a file to the Dabih server: dabih upload <path_to_file>", 
    help="This command uploads a file to the Dabih server. You can optionally specify a target directory by providing the mnemonic of the Dabih target directory."
)
@click.pass_context
@click.argument("file_path")
@click.argument("target_directory", required=False, default=None)
def upload_command(ctx, file_path, target_directory):
    client = ctx.obj["client"]
    try:
        upload_func(file_path, client, target_directory)
    except FileNotFoundError as e:
        error(f"File at path: {file_path} not found. Please check the path.")
        dbg(f"Error: {e}")
        sys.exit(0)
    except Exception as e:
        error("Unexpected error")
        dbg(f"Error: {e}")
        sys.exit(0)

@click.command(
    short_help="Download a file from the Dabih server: dabih download <mnemonic>",
    help="This command downloads a file from the Dabih server. You can optionally specify a target directory to download the file to. A private key saved in a specified directory is required to download files (see README.md)."
)
@click.pass_context
@click.argument("mnemonic")
@click.argument("target_directory", required=False, default=None)
def download_command(ctx, mnemonic, target_directory):
    client = ctx.obj["client"]
    if not ctx.obj["pem_files"]:
        error("No valid key files found; you need a private key to download files")
        sys.exit(0)
    download_func(mnemonic, client, ctx.obj["pem_files"], target_directory)

@click.command(
    short_help="Search for a file or folder", 
    help="This command will return all search results for the specified query including filename, mnemonic and author.\nUsage: dabih search <query>"
)
@click.pass_context
@click.argument("query")
def search(ctx, query):
    client = ctx.obj["client"]
    search_func(client, query)


main.add_command(token_info)
main.add_command(token_val)
main.add_command(check)
main.add_command(list_home)
main.add_command(list_files)
main.add_command(upload_command, name="upload")
main.add_command(download_command, name="download")
main.add_command(search)


if __name__ == "__main__":
    main()

