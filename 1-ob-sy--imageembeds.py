import os
import re
import urllib.parse  # For URL encoding

def build_file_path_map(root_dir):
    file_path_map = {}
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith((".jpg", ".png", ".webp")):
                full_path = os.path.join(root, file)
                # Use the full, normalized path as the key to ensure unique matches
                file_path_map[os.path.normcase(full_path)] = os.path.relpath(full_path, start=root_dir)
    return file_path_map

def update_image_links(file_path, file_path_map):
    modified = False
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    def replace_link(match):
        embedded_image_filename = match.group(1)  # Extract just the filename
        # Attempt to find the relative path for each image based on its filename
        for full_image_path, relative_image_path in file_path_map.items():
            if os.path.basename(full_image_path).lower() == embedded_image_filename.lower():
                # Calculate relative path from the current markdown file to the image file
                relative_path_from_note_to_image = os.path.relpath(full_image_path, start=os.path.dirname(file_path))
                web_safe_relative_path = urllib.parse.quote(relative_path_from_note_to_image)
                # Construct the markdown image link
                return f"![]({web_safe_relative_path})"
        print(f"Image not found in map: {embedded_image_filename}")
        return match.group(0)

    # This regex matches Obsidian-style embedded image links
    new_content = re.sub(r'!\[\[([^\]]+?\.(jpg|png|webp))\]\]', lambda match: replace_link(match), content, flags=re.IGNORECASE)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        modified = True

    return modified

def process_markdown_files(root_dir):
    file_path_map = build_file_path_map(root_dir)
    total_files_processed = 0
    total_files_updated = 0

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                if update_image_links(full_path, file_path_map):
                    print(f"Updated image links in: {os.path.basename(file)}")
                    total_files_updated += 1
                total_files_processed += 1

    print(f"Processed {total_files_processed} files, updated {total_files_updated} files.")

if __name__ == "__main__":
    vault_root_dir = './Personal Notes'  # Adjust this path to your vault's root directory
    process_markdown_files(vault_root_dir)
