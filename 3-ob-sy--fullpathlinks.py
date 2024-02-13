import os
import re

def build_file_path_map(root_dir):
    file_path_map = {}
    file_count = 0
    print("Building file path map...")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                # Get the relative path and remove the file extension
                relative_path = os.path.relpath(os.path.join(root, file), start=root_dir)
                relative_path_no_ext = os.path.splitext(relative_path)[0]  # Remove .md extension
                note_title = os.path.splitext(file)[0]
                # Use lowercase for matching and store path without .md extension
                file_path_map[note_title.lower()] = relative_path_no_ext.replace("\\", "/")
                file_count += 1
    print(f"Total markdown files found: {file_count}")
    return file_path_map

def replace_wikilinks_in_file(file_path, file_path_map):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    original_content = content  # Keep the original content for comparison
    wikilinks = re.findall(r'\[\[([^\]\|]+)(\|[^\]]+)?\]\]', content)
    link_changes = 0  # Track the number of links changed

    for wikilink, alias in wikilinks:
        wikilink_key = wikilink.lower()  # Match case-insensitively
        if wikilink_key in file_path_map:
            # No need to remove .md here, already handled in file_path_map
            full_path_link = f'[[{file_path_map[wikilink_key]}]]'
            content = content.replace(f'[[{wikilink}{alias}]]', full_path_link)
            link_changes += 1

    if content != original_content:  # Only write back if changes were made
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    return link_changes

def update_wikilinks(root_dir):
    file_path_map = build_file_path_map(root_dir)
    total_files_processed = 0
    total_links_changed = 0

    print("Updating wikilinks in files...")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                link_changes = replace_wikilinks_in_file(file_path, file_path_map)
                total_files_processed += 1
                if link_changes > 0:
                    print(f"Updated {link_changes} links in {file}")
                total_links_changed += link_changes

    print(f"Completed updating wikilinks. Total files processed: {total_files_processed}. Total links changed: {total_links_changed}")

if __name__ == "__main__":
    vault_root_dir = './Personal Notes'
    update_wikilinks(vault_root_dir)