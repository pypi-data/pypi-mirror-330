from typing import List, Any
from grabit.models import File


def generate_file_table(files: List[File]) -> str:
    """Generates a formatted table showing file info including paths, sizes and git history."""
    if not files:
        return "No files found"

    # Get the last commit info for each file
    last_commits = []
    for file in files:
        if file.git_history:
            # Git history format is: hash | author | date | message
            last_commit = file.git_history.split("\n")[0].split(" | ")
            last_commits.append({"author": last_commit[1], "date": last_commit[2]})
        else:
            last_commits.append({"author": "Unknown", "date": "Unknown"})

    # Calculate column widths
    path_width = max(len("File Path"), max(len(file.path) for file in files))
    size_width = max(
        len("Size (chars)"), max(len(str(len(file.contents))) for file in files)
    )
    tokens_width = max(len("Tokens"), max(len(str(file.tokens)) for file in files))
    author_width = max(
        len("Last Modified By"), max(len(commit["author"]) for commit in last_commits)
    )
    date_width = max(len("Date"), max(len(commit["date"]) for commit in last_commits))

    # Calculate total width including borders and padding
    total_width = (
        path_width
        + size_width
        + tokens_width
        + author_width
        + date_width
        + 12  # For the " | " separators
    )

    # Create border lines
    top_bottom_border = "+" + "-" * (total_width + 2) + "+"

    # Create header
    header = (
        f"| {'File Path':<{path_width}} | "
        f"{'Size (chars)':>{size_width}} | "
        f"{'Tokens':>{tokens_width}} | "
        f"{'Last Modified By':<{author_width}} | "
        f"{'Date':<{date_width}} |"
    )
    separator = "|" + "-" * (total_width + 2) + "|"

    # Create table rows
    rows = []
    for file, commit in zip(files, last_commits):
        row = (
            f"| {file.path:<{path_width}} | "
            f"{len(file.contents):>{size_width}} | "
            f"{file.tokens:>{tokens_width}} | "
            f"{commit['author']:<{author_width}} | "
            f"{commit['date']:<{date_width}} |"
        )
        rows.append(row)

    # Combine all parts with borders
    table = "\n".join(
        [top_bottom_border, header, separator] + rows + [top_bottom_border]
    )
    return table
