import os
import sys
import fnmatch

DEFAULT_IGNORE_PATTERNS = [
    "*.pyc", "*.pyo", "*.egg-info", "*.log", "*.tmp", "old*", "*old.py"
]
DEFAULT_IGNORE_EXACT = [
    "__pycache__", "build", "dist", ".git", ".idea", ".vscode", "lessons", ".ipynb_checkpoints", 
    "jupyter_notebooks", "data", ".pytest_cache", "__init__.py", ".gitignore"
]

# Emoji and Padding Dictionaries
DIRECTORY_EMOJIS = {
    "tests": "🧪 ",
    "utils": "🔧 ",
    "mindgraph": "🛸 "
}
FILE_EMOJIS = {
    "setup.py": "🐍 ",
    "test_": "",
    ".py": "",
    "README.md": "📜 ",
    "DIRECTORY_TREE.md": "📜 ",
    "LICENSE": "🦀 "  # Special emoji for files with no extension
}
DIRECTORY_PADDING = {}
FILE_PADDING = {
    "test_": "~ ",
    #".py": "~ ",
    #"": "~ "  # Special padding for files with no extension
}

# FILES TO BE SHOWN IN THE TREE
FILE_EXTENSIONS = ['.md', '', '.py']

# Emoji constants
ROOT_FOLDER_EMOJI = "🧠 "
FOLDER_EMOJI = "📂 "
MODULE_FOLDER_EMOJI = "🚀 "
TEST_FOLDER_EMOJI = "🧪 "
FILE_EMOJI = ""

# Customization for tree formatting
CONNECTOR_CHAR = "─"  # Option for customizing the tree branch character
FOLDER_NAME_PADDING = " "  # Default padding between the tree branch and folder names
FILE_NAME_PADDING = "─── "  # Default padding between the tree branch and file names
ROOT_FOLDER_PADDING = ""  # Adjustable padding for the root folder

# Output file for markdown
OUTPUT_FILE = 'DIRECTORY_TREE.md'  # Set the default output file to None, can be overridden by CLI argument

def is_test_folder(path):
    """Check if a folder contains at least one test_*.py file."""
    return any(f.startswith("test_") and f.endswith(".py") for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)))

def get_file_extension(file_name):
    """Returns the file extension or 'NO_EXT' if there is none."""
    return os.path.splitext(file_name)[1] if os.path.splitext(file_name)[1] else ""

def generate_directory_tree(directory="../", prefix="", ignore_patterns=None, ignore_exact=None, file_extensions=None, output_file=OUTPUT_FILE, is_root=True):
    """Recursively generates a tree structure of the given directory with sorting and filtering options."""
    if ignore_patterns is None:
        ignore_patterns = DEFAULT_IGNORE_PATTERNS
    if ignore_exact is None:
        ignore_exact = DEFAULT_IGNORE_EXACT
    
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    tree_output = []
    
    if is_root:
        tree_output.append(f"{ROOT_FOLDER_EMOJI}{ROOT_FOLDER_PADDING}{os.path.basename(directory)}/")
    
    entries = sorted(
        (e for e in os.listdir(directory) if e not in ignore_exact and not any(fnmatch.fnmatch(e, p) for p in ignore_patterns)),
        key=lambda x: (x[0].islower(), x.lstrip("_").lower())
    )
    
    sorted_entries = sorted(entries, key=lambda e: (os.path.isdir(os.path.join(directory, e)), FILE_EXTENSIONS.index(get_file_extension(e)) if get_file_extension(e) in FILE_EXTENSIONS else len(FILE_EXTENSIONS), e.lstrip("_").lower()))
    
    if file_extensions:
        sorted_entries = [e for e in sorted_entries if os.path.isdir(os.path.join(directory, e)) or any(e.endswith(ext) and not e.endswith(ext + "_") for ext in file_extensions) or get_file_extension(e) == "NO_EXT"]
    
    for index, entry in enumerate(sorted_entries):
        path = os.path.join(directory, entry)
        is_last = index == len(sorted_entries) - 1
        connector = f"└{CONNECTOR_CHAR}" if is_last else f"├{CONNECTOR_CHAR}"
        
        if os.path.isdir(path):
            folder_emoji = DIRECTORY_EMOJIS.get(entry, MODULE_FOLDER_EMOJI if "__init__.py" in os.listdir(path) else FOLDER_EMOJI)
            folder_padding = DIRECTORY_PADDING.get(entry, FOLDER_NAME_PADDING)
            tree_output.append(f"{prefix}{connector}{folder_padding}{folder_emoji}{entry}/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_output.extend(generate_directory_tree(path, new_prefix, ignore_patterns, ignore_exact, file_extensions, output_file, is_root=False))
        else:
            file_ext = get_file_extension(entry)
            file_emoji = FILE_EMOJIS.get(entry, FILE_EMOJIS.get(file_ext, FILE_EMOJI))
            file_padding = FILE_PADDING.get(entry, FILE_PADDING.get(file_ext, FILE_NAME_PADDING))
            tree_output.append(f"{prefix}{connector}{file_padding}{file_emoji}{entry}")
    
    if is_root:
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("## Project Directory Structure\n\n````java\n\n" + "\n".join(tree_output) + "\n````\n")
        else:
            print("\n".join(tree_output))
    
    return tree_output

def main():
    """Runs the tree generator as a script or CLI command."""
    global OUTPUT_FILE
    directory = "../mindgraph"  # Default to mindgraph if no argument is provided
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    if len(sys.argv) > 2:
        OUTPUT_FILE = sys.argv[2] if sys.argv[2].endswith(".md") else None
    
    ignore_patterns = DEFAULT_IGNORE_PATTERNS
    ignore_exact = DEFAULT_IGNORE_EXACT
    file_extensions = FILE_EXTENSIONS
    
    for arg in sys.argv[3:]:
        if arg.startswith("--ext="):
            file_extensions = arg[6:].split(",")
    
    generate_directory_tree(directory, ignore_patterns=ignore_patterns, ignore_exact=ignore_exact, file_extensions=file_extensions, output_file=OUTPUT_FILE)

if __name__ == "__main__":
    main()
