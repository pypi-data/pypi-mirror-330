import os
import inspect

def paste_code_in_file():
    """Detects the file where this package is imported and pastes `code.py` content into it."""
    
    # Get path of `code.py` inside the package
    package_dir = os.path.dirname(__file__)
    code_file_path = os.path.join(package_dir, "code.py")

    # Read `code.py` content
    with open(code_file_path, "r") as code_file:
        code_content = code_file.read()

    # Detect the Python script where `import sklearnPra` was written
    frame = inspect.stack()[-1]  # Get the last frame (original caller script)
    caller_script = os.path.abspath(frame.filename)

    # Ensure not modifying itself
    if caller_script != os.path.abspath(__file__):
        with open(caller_script, "a") as caller_file:
            caller_file.write("\n\n# --- Pasted Code from sklearnPra ---\n")
            caller_file.write(code_content)
            caller_file.write("\n# --- End of Pasted Code ---\n")

# Auto-execute on import
paste_code_in_file()
