import os
import time
import pytest
from athanasius.archiver import archive
from athanasius.extractor import extract

@pytest.fixture
def setup_test_files(tmp_path):
    dir1 = tmp_path / "dir1"
    dir1.mkdir()

    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file1.write_text("Hello, World!")
    file2.write_text("Python Testing")

    return file1, file2, dir1

def test_archive_and_extract(setup_test_files, tmp_path):
    file1, file2, dir1 = setup_test_files
    archive_path = tmp_path / "test.ath"

    archive([str(file1), str(file2), str(dir1)], str(archive_path))

    assert archive_path.exists()

    extract(str(archive_path))

    assert (tmp_path / "file1.txt").exists()
    assert (tmp_path / "file2.txt").exists()
    assert (tmp_path / "dir1").exists()

def test_metadata_preservation(setup_test_files, tmp_path):
    file1, _, _ = setup_test_files
    archive_path = tmp_path / "meta_test.ath"

    file1.chmod(0o755)
    mtime = time.time() - 10000
    os.utime(file1, (mtime, mtime))

    archive([str(file1)], str(archive_path))

    extract(str(archive_path))

    extracted_file = tmp_path / "file1.txt"
    assert extracted_file.stat().st_mode & 0o777 == 0o755
    assert abs(extracted_file.stat().st_mtime - mtime) < 2
