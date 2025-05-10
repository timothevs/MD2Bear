import os
import argparse # Added for command-line argument parsing

def create_tag_from_path(file_path, base_dir):
    """
    Creates a tag based on the file's directory relative to the base directory.
    Example: /base/foo/bar/note.md -> #foo/bar
    Returns None if the file is directly in base_dir or if path calculations fail.
    """
    try:
        parent_dir = os.path.dirname(file_path)

        # Ensure base_dir is a prefix of parent_dir, and they are absolute for clean comparison
        abs_parent_dir = os.path.abspath(parent_dir)
        abs_base_dir = os.path.abspath(base_dir)

        if not abs_parent_dir.startswith(abs_base_dir):
            # This case should ideally not be hit if files are correctly filtered from os.walk
            print(f"Warning: File {file_path} seems to be outside the base directory {base_dir}.")
            return None

        relative_dir = os.path.relpath(parent_dir, base_dir)

        # If the file is directly in the base_dir, relpath returns "."
        if relative_dir == ".":
            return None  # No subfolder, so no tag based on folder structure

        # Process directory components for CamelCase if they contain spaces
        path_components = relative_dir.split(os.sep)
        processed_components = []
        for component in path_components:
            if ' ' in component:
                # Split by space, capitalize each part, then join
                camel_case_component = "".join(word.capitalize() for word in component.split(' '))
                processed_components.append(camel_case_component)
            else:
                processed_components.append(component)

        # Ensure forward slashes for tags, consistent with the example #Ubuntu Apps/Concrete5
        tag_content = "/".join(processed_components)
        return f"#{tag_content}"
    except ValueError as e:
        print(f"Error creating tag for {file_path}: {e}")
        return None

def add_tag_to_file(file_path, tag):
    """
    Appends the given tag to the end of the specified file,
    preserving original access and modification timestamps.
    Ensures the tag is on a new line.
    """
    if tag is None:
        return False
    try:
        # 1. Record original timestamps
        stat_info = os.stat(file_path)
        original_atime = stat_info.st_atime
        original_mtime = stat_info.st_mtime

        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.read()

            # Ensure two linespaces before the tag and one after
            prefix = ""
            if not content:  # Empty file
                prefix = "\n\n"
            elif content.endswith("\n\n"):
                prefix = ""
            elif content.endswith("\n"):
                prefix = "\n"
            else:  # content does not end with a newline
                prefix = "\n\n"

            tag_to_append = prefix + tag + "\n"

            f.write(tag_to_append)

        # 2. Restore timestamps
        # Note: os.utime can take float seconds for higher precision if supported by the OS
        os.utime(file_path, (original_atime, original_mtime))

        print(f"Added tag '{tag}' to {file_path} and preserved timestamps.")
        return True
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False

def process_directory(base_dir):
    """
    Scans the base_dir recursively for .md files and adds tags to them.
    """
    if not os.path.isdir(base_dir):
        print(f"Error: Directory '{base_dir}' not found.")
        return

    print(f"Starting to process directory: {base_dir}")
    tagged_files_count = 0
    processed_files_count = 0

    for root, _, files in os.walk(base_dir):
        for file_name in files:
            if file_name.lower().endswith(".md"):
                processed_files_count += 1
                file_path = os.path.join(root, file_name)

                # Skip files that are symlinks to avoid potential issues or redundant processing
                if os.path.islink(file_path):
                    print(f"Skipping symlink: {file_path}")
                    continue

                tag = create_tag_from_path(file_path, base_dir)

                if tag:
                    if add_tag_to_file(file_path, tag):
                        tagged_files_count += 1
                # else:
                #    print(f"No tag generated for {file_path} (likely in base directory or error).")

    print(f"\nFinished processing.")
    print(f"Total Markdown files found: {processed_files_count}")
    print(f"Files successfully tagged: {tagged_files_count}")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Recursively find markdown files in a specified directory and add folder-based tags to them, preserving timestamps.")
    parser.add_argument("target_directory",
                        help="The target directory to scan for markdown files.")

    args = parser.parse_args()

    # Use the directory from command-line arguments
    target_directory = args.target_directory
    abs_target_directory = os.path.abspath(os.path.normpath(target_directory))

    process_directory(abs_target_directory)
