import os
import struct

def extract(archive_filename):
    with open(archive_filename, "rb") as archive_file:
        num_files = struct.unpack(">I", archive_file.read(4))[0]
        file_metadata = []

        for _ in range(num_files):
            name_len = struct.unpack(">I", archive_file.read(4))[0]
            name = archive_file.read(name_len).decode("utf-8")
            size = struct.unpack(">Q", archive_file.read(8))[0]
            is_empty_dir = struct.unpack(">B", archive_file.read(1))[0] == 1
            file_metadata.append((name, size, is_empty_dir))

        for (name, size, is_empty_dir) in file_metadata:
            if is_empty_dir:
                os.makedirs(name, exist_ok=True)
            else:
                dir_name = os.path.dirname(name)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                with open(name, "wb") as f:
                    f.write(archive_file.read(size))
