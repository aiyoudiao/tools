import shutil
import os
import sys

def copy_directory(source_path, dest_path, ignore_dirs=None):
    """
    Copy a directory structure from source_path to dest_path with progress indication.
    If dest_path exists, it merges the content.
    ignore_dirs: List of directory names to exclude from copying.
    """
    if ignore_dirs is None:
        ignore_dirs = ['node_modules']

    # Check if source directory exists
    if not os.path.exists(source_path):
        print(f"Error: Source directory '{source_path}' does not exist.")
        return

    try:
        # 1. Calculate total files for progress bar
        print("Scanning source directory to calculate total files...")
        total_files = 0
        for root, dirs, files in os.walk(source_path):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            total_files += len(files)

        if total_files == 0:
            print("No files found to copy.")
            return

        print(f"Total files to copy: {total_files}")
        print(f"Copying from: {source_path}")
        print(f"To:           {dest_path}")
        print(f"Ignoring:     {', '.join(ignore_dirs)}")
        print("-" * 50)

        # 2. Copy files manually to track progress
        copied_count = 0

        for root, dirs, files in os.walk(source_path):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            # Calculate destination directory path
            relative_path = os.path.relpath(root, source_path)
            current_dest_dir = os.path.join(dest_path, relative_path)

            # Ensure destination directory exists
            if not os.path.exists(current_dest_dir):
                os.makedirs(current_dest_dir)

            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(current_dest_dir, file)

                try:
                    # copy2 preserves metadata (timestamps, etc.)
                    shutil.copy2(src_file, dst_file)
                    copied_count += 1

                    # Update progress display
                    percent = (copied_count / total_files) * 100
                    # Create a simple progress bar
                    bar_length = 30
                    filled_length = int(bar_length * copied_count // total_files)
                    bar = '█' * filled_length + '-' * (bar_length - filled_length)

                    # Truncate filename if too long
                    display_name = file if len(file) < 25 else file[:22] + "..."

                    # \r returns cursor to start of line to overwrite previous output
                    sys.stdout.write(f"\r[{bar}] {percent:.1f}% ({copied_count}/{total_files}) {display_name:<25}")
                    sys.stdout.flush()

                except Exception as e:
                    print(f"\nError copying {src_file}: {e}")

        print("\n" + "-" * 50)
        print(f"Successfully copied {copied_count} files.")

    except Exception as e:
        print(f"\nAn error occurred during the copy operation: {e}")

if __name__ == "__main__":
    # Check for correct number of arguments
    if len(sys.argv) < 3:
        print("Usage: python copy_frontend.py <source_path> <destination_path>")
        print("Example: python copy_frontend.py c:\\source\\path c:\\dest\\path")
        sys.exit(1)

    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    # Normalize paths
    source_dir = os.path.normpath(source_dir)
    dest_dir = os.path.normpath(dest_dir)

    copy_directory(source_dir, dest_dir)
