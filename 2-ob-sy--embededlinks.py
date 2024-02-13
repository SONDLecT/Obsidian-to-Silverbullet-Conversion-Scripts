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
