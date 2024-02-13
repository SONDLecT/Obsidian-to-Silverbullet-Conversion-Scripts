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
    vault_root_dir = './Personal Notes'
    update_callouts(root_dir=vault_root_dir)
