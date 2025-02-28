import os

def generate_archive_name():
    counter = 1
    filename = "archive.ath"
    while os.path.exists(filename):
        counter += 1
        filename = f"archive-{counter}.ath"

    return filename
