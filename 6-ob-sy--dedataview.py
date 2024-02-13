import os
import re

def remove_dataview_and_inline_fields(file_path):
    """Remove Dataview queries and inline field references from markdown files."""
    modified = False
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Pattern to match Dataview blocks, including those not properly closed, and entire lines with inline field references.
    patterns_to_remove = [
        # Matches Dataview blocks, properly closed or ending at the document's end.
        r"```dataview[\s\S]*?(?:```|$)",
        # Matches entire lines containing inline references, starting with `=`.
        r"^.*`=\s*[^`\n]*`.*$\n?"
    ]

    # Combining patterns and applying multiline mode for accurate line-by-line matching.
    combined_pattern = re.compile('|'.join(patterns_to_remove), re.MULTILINE)

    # Removing matched patterns from the content.
    new_content, num_subs = re.subn(combined_pattern, '', content)

    # If modifications were made, flag as modified and update the file.
    if num_subs > 0:
        modified = True
        print(f"Removed Dataview queries and inline fields from: {file_path}")

    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

def process_all_markdown_files(root_dir):
    """Process all markdown files in the directory and subdirectories to remove Dataview queries and inline field references."""
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                remove_dataview_and_inline_fields(file_path)

if __name__ == "__main__":
    vault_root_dir = './Personal Notes'  # Adjust this path to your vault's root directory
    process_all_markdown_files(vault_root_dir)
