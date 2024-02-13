---
tag: project obsidian
---
# Goal:
Create python script that when run alongside an obsidian vault will prune the .md files to make indexing in Silverbullet more friendly.
Where available, don’t reinvent the wheel and recommend/use community plugins.




# Issues with Obsidian notes:
* [x] Wikilinks are flat and don’t include folder structure. This means every link is a broken link
* [x] Images are not displayed the same in SB. instead must be formatted as `[](absolute location.ext)`
* [x] Silverbullet does not have an embed feature with ! . Any embedded note will need to be replaced with the [[template/embed]] template structure
* [x] Silverbullet does not allow embedding of sections of notes. When scripts detect an embedded note that links to a subsection of a note, it should convert the interrobang wikilink to a normal wikilink. 
* [x] Admonitions/Callouts are not going to look pretty. Only note and warning are colorful and recognized in Silverbullet.Any admonitions should be converted to Obsidian callouts, and any Obsidian callouts should be converted to the note admonition format that Silverbullet renders correctly.

---
# Obsidian to Silverbullet Conversion Scripts:

## 1. Embedded Images are not handled Correctly:
This is the first script to run, to handle updating embedded image links within markdown files to use standard markdown image syntax. It looks for embedded links pointing to images (identified by `.jpg`, `.png`, `.webp` file extensions) and converts them into a markdown-friendly format that specifies the image's full path.

### Key Points:
*   The script extends the file path map to include image files, capturing both their titles and extensions.
*   It searches for embedded image links within markdown files, updating them to the correct markdown image link format, ensuring images are properly displayed in Silverbullet.
```python
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

```


## 2. Embedded Links and Link sections
This is the second script to run, it updates embedded links (now that the images are already handled). For full notes that are embedded it uses the [[template/embed]] template. For notes linking to sections it turns it into a simple wikilink.
```python
import os
import re

def process_markdown_file(file_path):
    """Processes a single markdown file to update embedded links."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # This pattern matches both full note embeds (![[note]]) and section-specific embeds (![[note#section]])
    pattern = re.compile(r'(!\[\[([^\]]+?)\]\])')

    def replacement_function(match):
        full_match = match.group(1)
        link_content = match.group(2)

        # If the link contains a section-specific part (denoted by '#'), convert to standard wikilink by removing '!'
        if '#' in link_content:
            return full_match.replace('!', '', 1)  # Remove the first occurrence of '!' only

        # For full note embeds, replace with the specified template format
        else:
            # To handle the placement within lists or callouts correctly, check for preceding characters
            prefix = '\n' if full_match.startswith(('* ', '> ')) else ''
            return f'{prefix}```template\npage: "[[{link_content}]]"\n```{prefix}'

    modified_content = re.sub(pattern, replacement_function, content)

    # Write the modified content back to the file if changes were made
    if modified_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)

def update_embedded_links_in_vault(root_dir):
    """Walks through the vault and updates embedded links in all markdown files."""
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                process_markdown_file(file_path)
                print(f"Processed {file_path}")

if __name__ == "__main__":
    vault_root_dir = './Personal Notes'  # Adjust this path to the root directory of your Obsidian vault
    update_embedded_links_in_vault(vault_root_dir)


```



## 3. Wikilinks are Flat:
This script checks all markdown files within a specified directory (and its subdirectories), updating wikilinks to include the full path relative to the root directory, minus the file extension. It's designed to maintain the integrity of links when migrating between systems that handle wikilinks differently, ensuring each link points to its correct file location within a nested folder structure

### Key Points:
*   It builds a map of all markdown files, associating file titles (in lowercase for case-insensitive matching) with their relative paths.
*   It then scans each markdown file for wikilinks, updating them to their full paths using the map.
*   Links are updated without the `.md` extension, matching the specified format.

```python
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
# adjust for your vault dir
    vault_root_dir = './Personal Notes' 
    update_wikilinks(vault_root_dir)
```

## 4. De-Callout/Admonition
The Admonition plugin has a “convert to callouts” feature in the settings. First use that to convert any admonition blocks to callouts. Then run the following:

```python

import os
import re

def reformat_callouts_in_file(file_path):
    modified = False
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Adjust the regex pattern to account for an optional space between ">" and "[!"
    callout_pattern = re.compile(
        r"^>\s*\[\!(hint|info|abstract|example|failure|missing|danger|error|bug|cite|tldr|todo|tip|important||to-do|question|faq|check||warning|danger|faq|quote|note|ad-quote)(\+|-)?\s*.*?](.*?)(?=\n|$)",
        re.MULTILINE
    )

    def replace_callout(match):
        # Directly replace the callout tag with "> **note**", preserving the rest of the line.
        preserved_text = match.group(3).strip()  # Capture and preserve any text following the callout tag.
        return f"> **note** {preserved_text}"

    # Apply the updated regex pattern to replace callouts with "> **note**", keeping subsequent text.
    new_content = re.sub(callout_pattern, replace_callout, content)

    if new_content != content:
        modified = True
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

    return modified

def update_callouts(root_dir):
    total_files_processed = 0
    total_files_updated = 0

    print("Updating callouts in files...")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                if reformat_callouts_in_file(file_path):
                    print(f"Updated callouts in {file}")
                    total_files_updated += 1
                total_files_processed += 1

    print(f"Completed updating callouts. Total files processed: {total_files_processed}. Total files updated: {total_files_updated}")

if __name__ == "__main__":
    # adjust for your vault dir
    vault_root_dir = './Personal Notes'
    update_callouts(root_dir=vault_root_dir)

```


## 5. Filenames with illegal characters
Finally, if there are Obsidian notes with, e.g., exclamation points in the filename, then Silverbullet will have an error in indexing the vault. As a final gesture, run the following:

```python
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

```
