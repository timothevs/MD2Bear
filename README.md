# Markdown Folder Tagger

A Python script to recursively scan a directory for Markdown files (`.md`) and append a tag to each file based on its parent folder structure. The script preserves the original modification and access timestamps of the files.

## Motivation

This script is particularly useful for users of applications like [Bear](https://bear.app/). When importing Markdown files, Bear does not preserve the existing folder structure for organization. Instead, it relies heavily on tags. This script automates the process of creating tags based on your folder hierarchy, making the transition or bulk import into Bear (or similar apps) much smoother.

**Important Bear App Note:** When importing notes into Bear, ensure you **deselect** the option `Escape Involuntary Tags` (or a similarly named option that might alter tag formatting) in Bear's import settings. This will ensure the tags generated by this script (e.g., `#Folder/Subfolder`) are imported correctly without being escaped (e.g., as `#Folder\/Subfolder`).

## Features

-   Recursively scans a specified directory for `.md` files.
-   Generates a tag based on the relative path of the file's containing folder (e.g., a file in `Notes/Projects/Alpha` would get the tag `#Projects/Alpha`).
-   Appends the tag to the end of each Markdown file, ensuring two newlines before the tag and one after.
-   Preserves the original access and modification timestamps of the processed files.
-   Command-line interface to specify the target directory.

## Prerequisites

-   Python 3.x

No external libraries are required beyond the Python standard library.

## Usage

1.  Clone the repository or download the `tag_markdown_notes.py` script.
2.  Open your terminal or command prompt.
3.  Navigate to the directory where you saved the script.
4.  Run the script by providing the path to the directory you want to process:

    ```bash
    python3 tag_markdown_notes.py /path/to/your/markdown_notes
    ```

    Replace `/path/to/your/markdown_notes` with the actual path to your notes directory.

    For example:

    ```bash
    python3 tag_markdown_notes.py ~/Documents/MyNotes
    ```

    If your directory path contains spaces, make sure to enclose it in quotes:

    ```bash
    python3 tag_markdown_notes.py "/path/to/your/markdown notes with spaces"
    ```

5.  The script will print the name of each file it processes and a summary at the end.

**Important:** It is highly recommended to **back up your notes directory** before running the script for the first time, especially if you have a large number of files. You might also want to test it on a small subset of your notes first.

## How Tagging Works

-   A file like `/Users/Me/Notes/Work/Meetings/2023-10-26.md` processed with `/Users/Me/Notes` as the base directory will receive the tag `#Work/Meetings`.
-   Files directly within the base directory will not be tagged as they have no relative parent folder structure to derive a tag from.
-   Tags use forward slashes (`/`) as separators, regardless of the operating system.

## Contributing

Contributions, issues, and feature requests are welcome. Please feel free to fork the repository and submit a pull request.
