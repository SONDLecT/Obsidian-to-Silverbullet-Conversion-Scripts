import os
import re

def remove_frontmatter_from_file(file_path):
    """Removes YAML frontmatter from a markdown file."""
    modified = False
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern to match YAML frontmatter
    frontmatter_pattern = re.compile(r'^---\s*\n[\s\S]*?\n---\s*\n', re.MULTILINE)
    
    # Remove the frontmatter
    new_content, count = re.subn(frontmatter_pattern, '', content, 1)
    
    if count > 0:
        modified = True
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Removed frontmatter from: {file_path}")
    
    return modified

def process_all_markdown_files(root_dir):
    """Processes all markdown files in the directory and subdirectories to remove frontmatter."""
    total_files_processed = 0
    total_files_modified = 0
    
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                if remove_frontmatter_from_file(file_path):
                    total_files_modified += 1
                total_files_processed += 1

    print(f"Processed {total_files_processed} files. Removed frontmatter from {total_files_modified} files.")

if __name__ == "__main__":
    vault_root_dir = './Personal Notes'  # Adjust this path to your vault's root directory
    process_all_markdown_files(vault_root_dir)
