import os
import re

def build_file_path_map(root_dir):
    file_path_map = {}
    file_count = 0
    print("Building file path map...")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith((".md", ".jpg", ".png", ".webp")):
                relative_path = os.path.relpath(os.path.join(root, file), start=root_dir).replace("\\", "/")
                # Create a key for direct filename reference, ignoring subdirectory paths
                filename_key = os.path.basename(file).lower()
                if filename_key not in file_path_map:  # Avoid overwriting if duplicate filenames exist in different dirs
                    file_path_map[filename_key] = relative_path
                file_count += 1
    print(f"Total markdown files and images found: {file_count}")
    return file_path_map

def replace_image_links_in_file(file_path, file_path_map):
    modified = False
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex to find embedded image links like ![[image.ext]]
    embedded_image_links = re.findall(r'!\[\[(.+?\.(jpg|png|webp))\]\]', content, re.IGNORECASE)
    for image_link in embedded_image_links:
        image_filename_key = os.path.basename(image_link[0]).lower()  # Use basename for matching
        if image_filename_key in file_path_map:
            # Replace with markdown image link syntax
            new_link = f"[]({file_path_map[image_filename_key]})"
            content = content.replace(f"![[{image_link[0]}]]", new_link)
            modified = True
        else:
            print(f"Path not found in map: {image_link[0]}")

    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    return modified

def update_image_links(root_dir):
    file_path_map = build_file_path_map(root_dir)
    total_files_processed = 0
    total_files_updated = 0

    print("Updating image links in files...")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                if replace_image_links_in_file(file_path, file_path_map):
                    print(f"Updated image links in {file}")
                    total_files_updated += 1
                total_files_processed += 1

    print(f"Completed updating image links. Total files processed: {total_files_processed}. Total files updated: {total_files_updated}")

if __name__ == "__main__":
    vault_root_dir = './Personal Notes'
    update_image_links(vault_root_dir)
