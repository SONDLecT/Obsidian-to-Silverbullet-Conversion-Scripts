import os

def prepend_hashtags_to_file(file_path, hashtags):
    """Prepends hashtags to the given file."""
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        file.seek(0, 0)
        file.write(hashtags + '\n' + content)

def add_hashtags_based_on_subdir(root_dir):
    """Walks through the directory, adding hashtags to files based on their subdirectory names."""
    for root, dirs, files in os.walk(root_dir):
        # Exclude the root directory from tag generation
        if root != root_dir:
            subdirs = root.replace(root_dir, '').strip(os.sep).split(os.sep)
            # Convert subdirectory names to lowercase and replace spaces with underscores
            subdirs = [subdir.lower().replace(' ', '_') for subdir in subdirs]
            hashtags = ' '.join(['#' + subdir for subdir in subdirs])
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    prepend_hashtags_to_file(file_path, hashtags)

if __name__ == "__main__":
    vault_root_dir = './Personal Notes'  # Adjust this path to your vault's root directory
    add_hashtags_based_on_subdir(vault_root_dir)
