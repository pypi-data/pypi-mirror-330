import os
import inspect

def paste_code_in_importing_file():
    """Detects the script where this package is imported and pastes `code.py` content into it."""
    
    # Get the absolute path of `code.py` inside the package
    package_dir = os.path.dirname(__file__)
    code_file_path = os.path.join(package_dir, "code.py")

    # Read `code.py` content
    with open(code_file_path, "r") as code_file:
        code_content = code_file.read()

    # Get the script that imported this package
    frame = inspect.stack()[-1]  # Get the last stack frame (original caller script)
    importing_script = os.path.abspath(frame.filename)  # Get the file name

    # Ensure the script is not inside the package itself (to avoid modifying `__init__.py`)
    if importing_script != os.path.abspath(__file__):
        with open(importing_script, "a") as target_file:
            target_file.write("\n\n# --- Pasted Code from sklearnPra ---\n")
            target_file.write(code_content)
            target_file.write("\n# --- End of Pasted Code ---\n")

# Auto-execute on import
paste_code_in_importing_file()
