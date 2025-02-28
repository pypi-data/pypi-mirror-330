import pytest
from athanasius.extractor import extract

def test_extract_invalid_archive(tmp_path):
    archive_path = tmp_path / "non_existent.ath"

    with pytest.raises(FileNotFoundError):
        extract(str(archive_path))
