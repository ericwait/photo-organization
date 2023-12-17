import os
import magic
import argparse


def guess_extension(file_path):
    mime_type = magic.from_file(file_path, mime=True)
    if mime_type == "image/jpeg":
        return ".jpg"
    elif mime_type in ["image/x-adobe-dng", "image/tiff"]:
        return ".dng"
    else:
        raise ValueError(f"Unknown file format for '{file_path}' with mime type '{mime_type}'")


def main():
    parser = argparse.ArgumentParser(description="Rename files without extensions based on content.")
    parser.add_argument("root_dir", help="The directory containing files to rename.")

    args = parser.parse_args()

    # Walk through the root directory and rename files
    for root, _, files in os.walk(args.root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.splitext(file_path)[1]:  # Check if file has no extension
                try:
                    extension = guess_extension(file_path)

                    # Remove trailing "_001" before adding extension
                    base_name, _ = os.path.splitext(file)
                    if base_name.endswith("_001"):
                        base_name = base_name[:-4]

                    new_name = f"{base_name}{extension}"
                    os.rename(file_path, os.path.join(root, new_name))
                    print(f"Renamed '{file}' to '{new_name}'")
                except ValueError as e:
                    print(f"Error guessing extension for '{file_path}': {e}")

if __name__ == "__main__":
    main()

