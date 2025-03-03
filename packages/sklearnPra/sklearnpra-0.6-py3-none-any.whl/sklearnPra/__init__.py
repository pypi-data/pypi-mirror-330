import os
import inspect

def paste_code_in_importing_file():
    """Detect the script where this package is imported and append `code.py` content into it."""

    # Get the absolute path of `code.py` inside the package
    package_dir = os.path.dirname(__file__)
    code_file_path = os.path.join(package_dir, "code.py")

    # Ensure `code.py` exists before proceeding
    if not os.path.exists(code_file_path):
        print("⚠️ Error: `code.py` not found in package directory.")
        return

    # Read the content of `code.py`
    with open(code_file_path, "r", encoding="utf-8") as code_file:
        code_content = code_file.read()

    # Find the script that imported this package
    importing_script = None
    for frame in reversed(inspect.stack()):
        if frame.filename and os.path.isfile(frame.filename):
            importing_script = os.path.abspath(frame.filename)
            break

    if not importing_script:
        print("⚠️ Warning: Could not detect the importing script.")
        return

    # Ensure it does not modify itself
    if importing_script != os.path.abspath(__file__):
        with open(importing_script, "a", encoding="utf-8") as target_file:
            target_file.write("\n\n# --- Pasted Code from sklearnPra ---\n")
            target_file.write(code_content)
            target_file.write("\n# --- End of Pasted Code ---\n")

        print(f"✅ Code from `code.py` pasted into {importing_script}")

# Auto-execute on import
paste_code_in_importing_file()
