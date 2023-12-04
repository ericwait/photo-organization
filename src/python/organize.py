import argparse
import logging
from datetime import datetime
from pathlib import Path
import exifread
import os
from logging.handlers import RotatingFileHandler

def setup_logging(log_file='organize.log', level=logging.INFO, max_size=10485760, backups=3):
    # Create a rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backups)

    # Set formatter for the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Get the root logger and set the level
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Add handler to the logger
    root_logger.addHandler(handler)

    # Optional: Add console handler to also print logs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

def is_image(file_path):
    # Define a set of common image file extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.dng'}

    # Check if the file extension is in the set of image extensions
    return file_path.suffix.lower() in image_extensions


def organize_photos(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        # Skip directories with '@' in the name
        if '@' in root:
            continue

        for filename in files:
            file_path = Path(root) / filename
            if is_image(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        tags = exifread.process_file(file)
                        if date_taken := tags.get('EXIF DateTimeOriginal'):
                            # Format the date and create new directory path
                            date_obj = datetime.strptime(str(date_taken), '%Y:%m:%d %H:%M:%S')
                            file_extension = file_path.suffix.lower()
                            new_file_name = date_obj.strftime('%Y-%m-%d_%H-%M-%S')
                            new_dir = output_dir / date_obj.strftime('%Y/%m/%d')
                            new_dir.mkdir(parents=True, exist_ok=True)

                            # Check for duplicate file names
                            new_file_path = new_dir / new_file_name
                            counter = 1
                            while new_file_path.exists():
                                new_file_path = new_dir / f"{new_file_name}_{counter:03}{file_extension}"
                                counter += 1

                            file_path.rename(new_file_path)

                            # Log the file move
                            logging.info(f'Moved file from {file_path} to {new_file_path}')
                except PermissionError as e:
                    logging.error(f'Permission denied for {file_path}: {e}')
                except FileNotFoundError as e:
                    logging.error(f'File not found: {file_path}: {e}')
                except Exception as e:
                    logging.error(f'Error processing {file_path}: {e}')


def cleanup_empty_dirs(base_dir):
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            if not os.listdir(dir_path):
                dir_path.rmdir()
                logging.info(f'Removed empty directory: {dir_path}')


def main():
    # Set up logging
    setup_logging('organize.log')

    logging.info("Starting photo organization...")

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Organize photos based on EXIF data.")
    parser.add_argument('source_path', type=str, help="Source directory containing photos")
    parser.add_argument('destination_path', type=str, help="Destination directory for organized photos")
    parser.add_argument('--reorg_path', type=str, default=None, help="Optional directory for unrecognized files")

    args = parser.parse_args()

    # Call the main photo organizing function
    organize_photos(Path(args.source_path), Path(args.destination_path))

    # Optionally, clean up empty directories in the source after reorganizing
    cleanup_empty_dirs(Path(args.source_path))

    print("Photo organization complete.")


if __name__ == "__main__":
    main()
