import os
import inspect

def get_importing_script():
    """Find the actual script that imports this package, avoiding IDLE's run.py."""
    for frame in reversed(inspect.stack()):
        filename = os.path.abspath(frame.filename)

        # Skip internal Python files
        if "idlelib" in filename or "run.py" in filename:
            continue

        # Return the first valid user script
        return filename
    return None  # Fallback if no valid script found

def paste_code_in_importing_file():
    """Detects the script that imports this package and pastes `code.py` content into it."""

    # Get package directory and `code.py`
    package_dir = os.path.dirname(__file__)
    code_file_path = os.path.join(package_dir, "code.py")

    # Read the content of `code.py`
    with open(code_file_path, "r") as code_file:
        code_content = code_file.read()

    # Detect the actual user script where `sklearnPra` was imported
    importing_script = get_importing_script()

    if importing_script and importing_script != os.path.abspath(__file__):
        with open(importing_script, "a") as target_file:
            target_file.write("\n\n# --- Pasted Code from sklearnPra ---\n")
            target_file.write(code_content)
            target_file.write("\n# --- End of Pasted Code ---\n")
        print(f"✅ Code pasted successfully into {importing_script}")

# Auto-execute when imported
paste_code_in_importing_file()
