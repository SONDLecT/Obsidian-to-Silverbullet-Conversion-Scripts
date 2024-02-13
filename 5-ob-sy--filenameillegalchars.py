import os
import re

def sanitize_filename(filename):
    """Removes illegal characters from filenames."""
    # Define illegal characters that you want to remove from filenames
    illegal_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '?', '/']
    for char in illegal_chars:
        filename = filename.replace(char, '')
    return filename

def rename_files_in_vault(root_dir):
    """Renames files in the vault to remove illegal characters."""
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.md'):
                sanitized_name = sanitize_filename(filename)
                if sanitized_name != filename:
                    original_path = os.path.join(root, filename)
                    new_path = os.path.join(root, sanitized_name)
                    os.rename(original_path, new_path)
                    print(f"Renamed: {filename} -> {sanitized_name}")

if __name__ == "__main__":
    vault_root_dir = './Personal Notes'  # Adjust this path to your vault's root directory
    rename_files_in_vault(vault_root_dir)
    print("Completed renaming files with illegal characters.")
