import os
import shutil
import time
import argparse

def delete_directories(root_dir, target_dir_name):
    """
    Recursively finds and deletes directories with the specified name.
    
    Args:
        root_dir (str): The root directory to start searching from.
        target_dir_name (str): The name of the directory to delete (e.g., 'node_modules').
    """
    if not os.path.exists(root_dir):
        print(f"Error: Directory '{root_dir}' does not exist.")
        return

    print(f"Scanning '{root_dir}' for '{target_dir_name}' directories...")
    
    found_dirs = []
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if target_dir_name in dirnames:
            full_path = os.path.join(dirpath, target_dir_name)
            found_dirs.append(full_path)
            # Prevent os.walk from entering the directory we're about to delete
            dirnames.remove(target_dir_name)

    if not found_dirs:
        print(f"No '{target_dir_name}' directories found.")
        return

    print(f"Found {len(found_dirs)} directories to delete.")
    
    for i, dir_to_delete in enumerate(found_dirs, 1):
        print(f"[{i}/{len(found_dirs)}] Deleting: {dir_to_delete} ... ", end="", flush=True)
        try:
            # Measure time for feedback
            start_time = time.time()
            
            # Use shutil.rmtree to delete the directory tree
            # on_error handler can be added for permission issues on Windows
            shutil.rmtree(dir_to_delete, ignore_errors=False, onerror=handle_remove_readonly)
            
            elapsed = time.time() - start_time
            print(f"Done ({elapsed:.2f}s)")
        except Exception as e:
            print(f"Failed! Error: {e}")

    print("\nOperation completed successfully.")

def handle_remove_readonly(func, path, exc):
    """
    Error handler for shutil.rmtree to handle read-only files on Windows.
    """
    import stat
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == 13: # 13 is Permission denied
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively delete directories with a specific name.")
    parser.add_argument("root_dir", help="The root directory to scan.")
    parser.add_argument("--target", default="node_modules", help="The directory name to delete (default: node_modules)")
    
    args = parser.parse_args()
    
    delete_directories(args.root_dir, args.target)
