import os
import subprocess
import shutil
import pytest
import hashlib
import platform

def test_cli_help():
    result = subprocess.run(["ath", "--help"], capture_output=True, text=True)
    assert "usage" in result.stdout.lower()

@pytest.fixture(autouse=True)
def cleanup_test_files():
    yield
    for file in os.listdir("."):
        if file.endswith(".txt") or file.endswith(".ath"):
            os.remove(file)

def test_cli_archive_and_extract(tmp_path):
    file1 = tmp_path / "testfile.txt"
    file1.write_text("CLI Testing")

    archive_path = tmp_path / "cli_test.ath"

    subprocess.run(["ath", str(file1), "-o", str(archive_path)], check=True)

    assert archive_path.exists()

    subprocess.run(["ath", "-e", str(archive_path)], check=True)

    assert (tmp_path / "testfile.txt").exists()


def test_cli_wildcard_matching(tmp_path):
    for i in range(3):
        (tmp_path / f"file{i}.txt").write_text(f"Content {i}")

    archive_path = tmp_path / "wildcard_test.ath"
    subprocess.run(["ath", *map(str, tmp_path.glob("*.txt")), "-o", str(archive_path)], check=True)

    assert archive_path.exists()

    extracted_path = tmp_path / "extracted"
    extracted_path.mkdir()
    shutil.move(str(archive_path), str(extracted_path))
    subprocess.run(["ath", "-e", str(extracted_path / "wildcard_test.ath")], cwd=str(extracted_path), check=True)

    for i in range(3):
        assert (extracted_path / f"file{i}.txt").exists()

def test_cli_nested_directories(tmp_path):
    nested_dir = tmp_path / "parent" / "child"
    nested_dir.mkdir(parents=True)

    (nested_dir / "nested_file.txt").write_text("Nested content")
    (tmp_path / "root_file.txt").write_text("Root content")

    archive_path = tmp_path / "nested_test.ath"
    subprocess.run(["ath", str(tmp_path / "parent"), str(tmp_path / "root_file.txt"), "-o", str(archive_path)], check=True)

    assert archive_path.exists()

    extracted_path = tmp_path / "extracted"
    extracted_path.mkdir()
    shutil.move(str(archive_path), str(extracted_path))
    subprocess.run(["ath", "-e", str(extracted_path / "nested_test.ath")], cwd=str(extracted_path), check=True)

    assert (extracted_path / "parent" / "child" / "nested_file.txt").exists()
    assert (extracted_path / "root_file.txt").exists()

def test_cli_empty_folders(tmp_path):
    empty_dir = tmp_path / "empty_folder"
    empty_dir.mkdir()

    archive_path = tmp_path / "empty_test.ath"

    subprocess.run(["ath", str(empty_dir), "-o", str(archive_path)], check=True)
    assert archive_path.exists()

    extracted_path = tmp_path / "extracted"
    extracted_path.mkdir()
    subprocess.run(["ath", "-e", str(archive_path)], cwd=str(extracted_path), check=True)

    assert (extracted_path / "empty_folder").exists()
    assert (extracted_path / "empty_folder").is_dir()

@pytest.mark.skipif(platform.system() == "Windows", reason="Symlink tests are unreliable on Windows without admin privileges")
def test_cli_symlinks(tmp_path):
    target_file = tmp_path / "target.txt"
    target_file.write_text("This is the original file.")

    symlink = tmp_path / "symlink.txt"
    symlink.symlink_to(target_file)

    archive_path = tmp_path / "symlink_test.ath"

    subprocess.run(["ath", str(symlink), "-o", str(archive_path)], check=True)
    assert archive_path.exists()

    extracted_path = tmp_path / "extracted"
    extracted_path.mkdir()
    subprocess.run(["ath", "-e", str(archive_path)], cwd=str(extracted_path), check=True)

    extracted_symlink = extracted_path / "symlink.txt"

    assert extracted_symlink.exists()

    if extracted_symlink.is_symlink():
        assert extracted_symlink.resolve() == target_file.resolve()

def test_cli_hidden_files(tmp_path):
    hidden_file = tmp_path / ".hidden_file"
    hidden_file.write_text("This is a hidden file.")

    archive_path = tmp_path / "hidden_test.ath"

    subprocess.run(["ath", str(hidden_file), "-o", str(archive_path)], check=True)
    assert archive_path.exists()

    extracted_path = tmp_path / "extracted"
    extracted_path.mkdir()
    subprocess.run(["ath", "-e", str(archive_path)], cwd=str(extracted_path), check=True)

    assert (extracted_path / ".hidden_file").exists()

def generate_large_file(file_path, size_mb):
    with open(file_path, "wb") as f:
        f.write(os.urandom(size_mb * 1024 * 1024))

def hash_file(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

@pytest.mark.slow
def test_cli_large_file(tmp_path):
    large_file = tmp_path / "large_test.bin"
    generate_large_file(large_file, size_mb=500)

    original_hash = hash_file(large_file)
    archive_path = tmp_path / "large_test.ath"

    subprocess.run(["ath", str(large_file), "-o", str(archive_path)], check=True)
    assert archive_path.exists()

    extracted_path = tmp_path / "extracted"
    extracted_path.mkdir()
    subprocess.run(["ath", "-e", str(archive_path)], cwd=str(extracted_path), check=True)

    extracted_file = extracted_path / "large_test.bin"
    assert extracted_file.exists()
    assert hash_file(extracted_file) == original_hash
