
# Goal:
Create python script that when run alongside an obsidian vault will prune the .md files to make indexing in Silverbullet more friendly.
Where available, don’t reinvent the wheel and recommend/use community plugins.




# Issues with Obsidian notes more or less addressed by these scripts:
* [x] Wikilinks are flat and don’t include folder structure. This means every link is a broken link. Links should be updated to include the full path of a vault.
* [x] Images are not displayed the same in SB. Instead must be formatted as `[](relative location.ext)`
* [x] Silverbullet does not have an embed feature with ! . Any embedded note will need to be replaced with the template codeblock
* [x] Silverbullet does not allow embedding of sections of notes. When scripts detect an embedded note that links to a subsection of a note, it should convert the interrobang wikilink to a normal wikilink. 
* [x] Admonitions/Callouts are not going to look pretty. Only note and warning are colorful and recognized in Silverbullet.Any admonitions should be converted to Obsidian callouts, and any Obsidian callouts should be converted to the note admonition format that Silverbullet renders correctly.
* [x] Dataview tables and inline references won't work in SB. While there are better ways of handling this, one way of "fixing" the issue is to just remove those references.
* [x] Maybe you're an idiot, like me, and have lots of invalid frontmatter in your Obsidian notes and never realized it. That's going to break indexing in Silverbullet for now. One particularly inelegant solution is to delete any YAML, which you could take, I guess. If you're an idiot, like me.
* [x] If you've done the above, you may want to tag notes based on their subdirectory location. E.g., a note in /project 1/meetings/meeting-today.md will be tagged #project1 and #meeting.
---

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
