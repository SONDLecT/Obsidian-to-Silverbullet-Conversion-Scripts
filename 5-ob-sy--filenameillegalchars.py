import os
import re

def sanitize_filename(filename):
    """Removes illegal characters from filenames and enforces naming rules."""
    illegal_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '?', '/']
    filename = re.sub(f"[{''.join(re.escape(char) for char in illegal_chars)}]", '', filename)
    filename = re.sub(r'^\.', '', filename)
    filename = re.sub(r'[@$]', '', filename)
    if re.search(r'\.[a-zA-Z]+\.[a-zA-Z]+$', filename):
        filename = re.sub(r'\.[a-zA-Z]+\.[a-zA-Z]+$', '.md', filename)
    return filename

def remove_unwanted_content(content):
    """Removes empty brackets, [""] or "[]", summary: [""], aliases, and any `: []` from file content."""
    patterns_to_remove = [
        r'\[\[\]\]', r'\[\]', r'""', r'\[""\]',
        r'^summary: \[""\]$', r'^summary: \[\]$',  # Matches `summary: []`
        r'^.*: \[\]$',  # Matches any line ending with `: []`
    ]
    # Remove patterns
    for pattern in patterns_to_remove:
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    # Remove aliases and alias lines
    content = re.sub(r'^aliases?::?\s*(\[.*?\])?\s*$', '', content, flags=re.MULTILINE)
    return content

def process_files_in_vault(root_dir):
    """Processes files in the vault, renaming and cleaning content according to rules."""
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.md'):
                sanitized_name = sanitize_filename(filename)
                original_path = os.path.join(root, filename)
                new_path = os.path.join(root, sanitized_name)
                if sanitized_name != filename:
                    os.rename(original_path, new_path)
                    print(f"Renamed: {filename} -> {sanitized_name}")
                    filename = sanitized_name  # Update filename for content processing
                
                file_path = os.path.join(root, filename)  # Updated to handle potential renaming
                
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                updated_content = remove_unwanted_content(content)
                
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(updated_content)
                print(f"Processed: {filename}")

if __name__ == "__main__":
    vault_root_dir = './Personal Notes'  # Adjust this path to your vault's root directory
    process_files_in_vault(vault_root_dir)
    print("Completed processing files.")
