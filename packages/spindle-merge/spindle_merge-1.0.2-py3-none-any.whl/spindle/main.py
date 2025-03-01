import os
import glob
import argparse
import sys

try:
    import pyperclip
except ImportError:
    print("Error: The pyperclip module is required. Please run 'pip install pyperclip'.")
    sys.exit(1)


def load_file_paths(file_list_path):
    """
    Read the specified file list (SpindleLists.txt).
    - Ignore blank lines and comment lines starting with '#'.

    Parameters:
        file_list_path (str): Path to SpindleLists.txt

    Returns:
        list: List of valid file paths
    """
    try:
        with open(file_list_path, 'r', encoding='utf-8') as file:
            paths = []
            for line in file:
                stripped = line.strip()
                # Skip blank lines or comment lines
                if not stripped or stripped.startswith("#"):
                    continue
                paths.append(stripped)
            return paths
    except Exception as e:
        print(f"Error loading file list: {e}")
        return []


def merge_files(file_paths, output_path):
    """
    Merge multiple files into one output file.
    Insert a header with the file name before the content of each file,
    and copy the final result to the clipboard.

    Parameters:
        file_paths (list): List of file paths to merge
        output_path (str): Path to the output file
    """
    separator = "=" * 79  # Separator
    merged_content = ""   # For copying to clipboard
    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for path in file_paths:
                # Perform user expansion (~, etc.)
                expanded_path = os.path.expanduser(path)
                # Enable recursive search by specifying recursive=True
                matched_files = glob.glob(expanded_path, recursive=True)

                if not matched_files:
                    print(f"Warning: No files matched: {expanded_path}")
                    continue

                for file in matched_files:
                    if os.path.isfile(file):
                        try:
                            header = separator + "\n" + f"File: {file}\n" + separator + "\n\n"
                            outfile.write(header)
                            merged_content += header

                            with open(file, 'r', encoding='utf-8') as infile:
                                content = infile.read()
                                outfile.write(content)
                                merged_content += content
                                outfile.write("\n")
                                merged_content += "\n"
                            print(f"Merged: {file}")
                        except Exception as e:
                            print(f"Error reading {file}: {e}")
                    elif os.path.isdir(file):
                        # Ignore directories without warning
                        continue
                    else:
                        print(f"Warning: Not a valid file: {file}")
        print(f"All files have been merged into {output_path}")

        # Copy the merged result to the clipboard
        pyperclip.copy(merged_content)
        print("Merged content has been copied to clipboard.")
    except Exception as e:
        print(f"Error writing to {output_path}: {e}")


def main():
    """
    Merge files based on SpindleLists.txt located in the execution directory.
    """
    parser = argparse.ArgumentParser(
        description="Spindle: Merge files listed in SpindleLists.txt."
    )
    parser.add_argument(
        "-o", "--output",
        default="spindle_output.txt",
        help="Path to the output file. Default is 'spindle_output.txt'."
    )
    args = parser.parse_args()

    file_list_path = "SpindleLists.txt"
    if not os.path.exists(file_list_path):
        # print(f"Error: '{file_list_path}' が存在しません。")
        print(f"Error: '{file_list_path}' does not exist.")
        sys.exit(1)

    file_paths = load_file_paths(file_list_path)
    if file_paths:
        merge_files(file_paths, os.path.expanduser(args.output))
    else:
        print("Error: No valid file paths found.")


if __name__ == "__main__":
    main()
