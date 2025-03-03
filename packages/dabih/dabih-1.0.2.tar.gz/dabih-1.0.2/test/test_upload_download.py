import pytest
from click.testing import CliRunner
from dabih.main import main

@pytest.fixture
def runner():
    return CliRunner()

def test_upload_with_invalid_file(runner):
    result = runner.invoke(main, ['upload', 'non_existent_file.txt'])
    print(result.output)
    assert 'File at path: non_existent_file.txt not found. Please check the path.' in result.output

def test_upload_with_invalid_folder(runner):
    result = runner.invoke(main, ['upload', r'dabih\test\test.txt', 'invalid_folder_mnemonic'])
    print(result.output)
    assert 'Requested dabih file/folder not found: Inode invalid_folder_mnemonic not found.' in result.output

def test_download_with_invalid_mnemonic(runner):
    result = runner.invoke(main, ['download', 'invalid_mnemonic'])
    print(result.output)
    assert 'Requested dabih file/folder not found: No file found for mnemonic invalid_mnemonic.' in result.output

def test_download_invalid_folder(runner):
    result = runner.invoke(main, ['download', 'brachypterous_mysty'])
    print(result.output)
    assert 'Requested dabih file/folder not found: No file found for mnemonic brachypterous_mysty. Only files, not folders, can be downloaded.' in result.output
