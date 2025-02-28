import os
import struct

def archive(paths, output_filename):
    file_entries = []

    for path in paths:
        path = os.path.normpath(path)
        if not os.path.exists(path):
            print(f"Warning: {path} does not exist, skipping.")
            continue

        if os.path.isdir(path):
            has_files = False
            for root, _, files in os.walk(path):
                for file in files:
                    has_files = True
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, start=os.path.dirname(path))
                    file_entries.append((rel_path, full_path, False))
            if not has_files:
                rel_path = os.path.relpath(path, start=os.path.dirname(path))
                file_entries.append((rel_path, path, True))
        else:
            rel_path = os.path.basename(path)
            file_entries.append((rel_path, path, False))

    with open(output_filename, "wb") as archive_file:
        archive_file.write(struct.pack(">I", len(file_entries)))

        for rel_path, full_path, is_empty_dir in file_entries:
            name_bytes = rel_path.encode("utf-8")
            archive_file.write(struct.pack(">I", len(name_bytes)))
            archive_file.write(name_bytes)
            archive_file.write(struct.pack(">Q", 0 if is_empty_dir else os.path.getsize(full_path)))
            archive_file.write(struct.pack(">B", 1 if is_empty_dir else 0))

        for _, full_path, is_empty_dir in file_entries:
            if not is_empty_dir:
                with open(full_path, "rb") as f:
                    archive_file.write(f.read())
