# Migrating from Obsidian to Silverbullet: A Practical Guide

This guide is for those of us who've decided to make the jump from Obsidian to Silverbullet. If you're like me, you've amassed a significant collection of notes in Obsidian, only to realize that transitioning to Silverbullet comes with its own set of challenges. 

During my attempt to migrate over 3,000 notes, I encountered several issues with my notes that either caused rendering, indexing or just plain aesthetic issues in Silverbullet. Here's a rundown of the problems and the scripts I developed to tackle them:

- **Wikilinks**: Obsidian's wikilinks don't include folder structure, leading to broken links in Silverbullet. The scripts modify links to include the full path.
- **Image Embeds**: Images in Obsidian are not automatically compatible with Silverbullet. The scripts adjust image links to the `[](relative location.ext)` format required by Silverbullet.
- **Embeds and Sections**: Silverbullet lacks Obsidian's `!` embed feature. The scripts convert embeds to a compatible format and simplify section links to standard wikilinks.
- **Admonitions/Callouts**: Silverbullet only recognizes "note" and "warning" types with enhanced visibility. The scripts transform Obsidian callouts to a compatible format.
- **Dataview Queries**: Unsupported in Silverbullet, the scripts remove Dataview tables and inline references.
- **Frontmatter Issues**: Excessive or invalid frontmatter can cause indexing issues in Silverbullet. A less elegant but effective solution is to remove YAML frontmatter entirely.
- **Subdirectory Tags**: To leverage Silverbullet's tagging system for organization, the scripts generate tags based on a note's subdirectory location.

Each script addresses specific formatting or compatibility issues, ensuring a smoother transition from Obsidian's feature-rich environment to Silverbullet's streamlined platform. While not perfect, these solutions helped me migrate my vault with minimal loss of functionality. Hopefully, they can assist you too or inspire better solutions down the line.

# Obsidian to Silverbullet Conversion Scripts:

## Dependencies
These scripts are written in Python and utilize standard libraries included with Python: `os` for file and directory operations, `re` for regular expression matching, and `urllib.parse` for encoding URLs. Ensure Python 3 is installed on your system. No external dependencies are required.

## Preparing Your Environment
1. **Install Python**: Verify that Python 3 is installed by running `python --version` or `python3 --version` in your terminal or command prompt. You should see a version number that starts with 3.
2. **Download the Scripts**: Clone or download the Python scripts from the GitHub repository to a directory on your computer.
3. **Adjust the Vault Path**: Before running the scripts, modify the path to your Obsidian vault within each script. Look for the line that sets `vault_root_dir`, which will typically be near the end of the script:
   ```python
   vault_root_dir = './Personal Notes'  # Adjust this path to your vault's root directory

Replace './Personal Notes' with the actual path to your Obsidian vault, ensuring it is correctly formatted for your operating system.

## Running the Scripts

Open a terminal or command prompt, navigate to the directory containing the scripts, and run each script individually with the command python script_name.py, substituting script_name.py with the name of the script you wish to run. For example:
 `python 1-ob-sy--imageembeds.py`

## Order of Execution:
Scripts 1-5 should be run in order to avoid formatting errors. Scripts 6, 7 and 8 are all optional but may be necessary for your use if you encounter indexing issues when importing your vault. 

### 1. 1-ob-sy--imageembeds.py - Embedded Images are not handled Correctly:
This script updates embedded image links within markdown files to the standard markdown image syntax appropriate for Silverbullet. It corrects the paths of images referenced in Obsidian-style ![[Image Name.ext]] format, ensuring they point to the correct relative path within the vault. The script generates a map of all images in the vault, then iterates over markdown files to update the links, making images display correctly in Silverbullet.

### 2. 2-ob-sy--embededlinks.py - Embedded Links and Link sections:
This script addresses the handling of embedded links and sections within notes. It transforms Obsidian embeds (![[note]] and ![[note#section]]) into a format recognizable by Silverbullet. Full note embeds are converted into a [[template/embed]] structure, while section links are simplified to standard wikilinks. This ensures seamless integration with Silverbullet's navigation and referencing capabilities.

### 3. 3-ob-sy--fullpathlinks.py - Expand Wikilink filenames:
To address the flat structure of wikilinks in Obsidian, this script augments wikilinks with the full path relative to the root directory, excluding the file extension. By doing so, it preserves the integrity of links during the migration to systems like Silverbullet that may interpret wikilinks differently. This script ensures that each link accurately points to its corresponding file within the vault's nested folder structure.

### 4. 4-ob-sy--decallout.py - De-Callout/Admonition:
This script converts Obsidian callouts and admonitions into a simplified format recognized by Silverbullet, specifically focusing on the conversion to the "note" and "warning" types that are supported with enhanced visibility. It's an essential step for those migrating content from Obsidian to Silverbullet, ensuring that important highlighted information retains its emphasis.

### 5. 5-ob-sy--filenameillegalchars.py - Filenames with illegal characters:
To prevent indexing issues in Silverbullet, this script scans the vault for filenames containing characters that might cause errors (e.g., !, @, #). It sanitizes these filenames by removing illegal characters, thereby ensuring smooth integration and accessibility within Silverbullet. It's a crucial cleanup step for a seamless transition between the two platforms.

### 6. 6-ob-sy--dedataview.py - Remove Dataview and Inline Fields:
This script eliminates Dataview blocks and inline field references (=) from markdown files, which are not compatible with Silverbullet. Removing these elements helps in avoiding rendering issues and ensures that the content within Silverbullet is clean and free from unsupported syntax that might lead to confusion or errors during indexing.

### 7. 7-ob-sy--hailmaryYAMLremoval.py - Remove YAML Frontmatter:
YAML frontmatter, while useful in Obsidian for metadata and settings, can interfere with Silverbullet's processing if a note contains invalid frontmatter. This optional script strips the YAML frontmatter from markdown files, ensuring that the content is compatible with Silverbullet's indexing and rendering processes. It's an aggressive approach to compatibility but can be necessary for those looking to streamline their notes for Silverbullet's environment.

### 8. 8-ob-sy--tagsfordirectories.py - Auto-tagging Based on Subdirectories:
To enhance organization and findability within Silverbullet, this script auto-tags markdown files based on their subdirectory paths within the vault. It generates tags from each level of the directory structure (converting spaces to underscores and making lowercase), appending these tags to the top of the respective markdown files. This feature allows for a richer, more navigable structure within Silverbullet, leveraging the organizational hierarchy present in the Obsidian vault.
