import os
import platform
import argparse
import subprocess
from pathlib import Path
import re
from typing import List, Set, Tuple
from grabit.models import File
from datetime import datetime
from grabit.present import generate_file_table


def copy_to_clipboard(text: str):
    """Copies text to clipboard based on OS."""
    system = platform.system()
    if system == "Windows":
        process = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
        process.communicate(input=text.encode("utf-8"))
    elif system == "Darwin":  # macOS
        process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        process.communicate(input=text.encode("utf-8"))


def read_gitignore(directory: str) -> Tuple[Set[str], str]:
    """
    Reads a .grabit file (if present) and returns:
    - A set of patterns as re.compile objects to ignore
    - A custom message to prepend to the context (if specified)
    """
    gitignore_path = Path(directory) / ".grabit"
    ignore_patterns = set()
    custom_message = (
        "Below is a list of related files, their contents and git history.\n\n"
    )

    if gitignore_path.exists():
        print("--- Found .grabit ---")
        current_section = None
        message_lines = []

        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("## "):
                    current_section = line[3:].lower()
                    continue

                if not line or line.startswith(
                    "//"
                ):  # Skip comments and empty lines
                    continue

                if current_section == "exclude":
                    ignore_patterns.add(re.compile(line))
                elif current_section == "message":
                    message_lines.append(line)

        if message_lines:
            custom_message = "\n".join(message_lines) + "\n\n"

    print("--- ignore patterns ---")
    print(ignore_patterns)
    return ignore_patterns, custom_message


def get_git_data(file_path: str) -> Tuple[str, datetime, str] | None:
    """
    Gets the git history of the provided file path, and extracts associated data.
    """
    git_log_cmd = [
        "git",
        "log",
        "--follow",
        "--pretty=format:%h | %an | %ad | %s",  # Gets the author name, and author date
        "--date=short",
        file_path,
    ]

    try:
        result = subprocess.run(
            git_log_cmd, capture_output=True, text=True, check=True
        )
        history = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e}")
        return None

    if history == "":
        return None

    # If history is not None, get the data
    last_modified_string = history.split("\n")[0].split("|")[2].strip()
    last_modified = datetime.strptime(last_modified_string, "%Y-%m-%d")

    last_author = history.split("\n")[0].split("|")[1].strip()

    return (history, last_modified, last_author)


def is_ignored(
    file_path: str, ignore_patterns: Set[str], base_path: str
) -> bool:
    """Checks if a file matches a regex pattern from the .grabit config."""
    for pattern in ignore_patterns:
        found = pattern.match(file_path)
        if found is not None:
            return True

    return False


def recursive_files(
    path: str,
    ignore_patterns: Set[str],
    data: List[File] = [],
) -> List[File]:
    """Recursively gets all file paths and contents in a directory, respecting .gitignore."""
    directories = [
        d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))
    ]
    files = [
        f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
    ]

    for file in files:
        file_path = os.path.join(path, file)

        if is_ignored(file_path, ignore_patterns, path):
            print(f"Skipping ignored file: {file_path}")
            continue

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                contents = f.read()

            # Used to improve presentation on the command line
            git_data = get_git_data(file_path)

            if git_data is None:
                git_history = None
                last_author = None
                last_modified = None
            else:
                git_history, last_modified, last_author = git_data

            data.append(
                File(
                    path=file_path,
                    contents=contents,
                    chars=len(contents),
                    tokens=len(contents) // 4,
                    git_history=git_history,
                    last_author=last_author,
                    last_modified=last_modified,
                )
            )

            print(f"Found: {file_path}")
        except Exception as e:
            print(f"Skipping {file_path}: {e}")

    for directory in directories:
        recursive_files(os.path.join(path, directory), ignore_patterns, data)

    return data


def prepare_context(path: str, output: str = None, to_clipboard: bool = False):
    """Prepares a context string for AI to read, optionally saves or copies it."""
    ignore_patterns, custom_message = read_gitignore(path)
    files = recursive_files(path, ignore_patterns)

    # The context string builds the message for the LLM
    # It starts with a default message.
    context = (
        "Below is a list of related files, their contents and git history.\n\n"
    )

    if custom_message is not None:
        context = custom_message

    for file in files:
        unix_style_path = file.path.replace("\\", "/")
        context += f"## `{unix_style_path}`:\n### Git History:\n{file.git_history}\n### Contents:\n```\n{file.contents}\n```\n\n"

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(context)
        print(f"Context saved to {output}")

    if to_clipboard:
        print("Context copied to clipboard.")
        copy_to_clipboard(context)

    if not output and not to_clipboard:
        print(context)
        print("\nUse the `-c` flag to copy this context to clipboard.")
        print("Use the `-o <your-file-name>` flag to save it to a file.")

    print(f"\nPrompt Size: {len(context)} Chars")
    print(f"Prompt Size: {round(len(context)/4)} Tokens (Rough estimate).")
    print(f"Total files: {len(files)}")
    print(generate_file_table(files))

    return context


from grabit.initialisation import init_command


def main():
    """Command-line interface for the script."""
    parser = argparse.ArgumentParser(
        description="Recursively scan a directory, extract file contents, and save/copy them, respecting .gitignore."
    )

    subparser = parser.add_subparsers(dest="command", help="Available commands")

    # Parser for initialising a .grabit file
    init_parser = subparser.add_parser(
        "init", help="Initialize a standard .grabit file in current directory"
    )

    # Parser for scanning files
    scan_parser = subparser.add_parser(
        "scan", help="Scan a directory and save/copy the context"
    )
    scan_parser.add_argument(
        "directory", type=str, help="The directory to scan"
    )
    scan_parser.add_argument(
        "-o", "--output", type=str, help="File to save extracted content"
    )
    scan_parser.add_argument(
        "-c",
        "--clipboard",
        action="store_true",
        help="Copy output to clipboard",
    )

    args = parser.parse_args()

    if args.command == "init":
        init_command()
    elif args.command == "scan":
        prepare_context(
            args.directory, output=args.output, to_clipboard=args.clipboard
        )


if __name__ == "__main__":
    main()
