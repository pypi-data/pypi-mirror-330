import os
import inspect

def paste_code_in_importing_file():
    """Detects the script where this package is imported and pastes `code.py` content into it."""
    
    # Get the absolute path of `code.py` inside the package
    package_dir = os.path.dirname(__file__)
    code_file_path = os.path.join(package_dir, "code.py")

    # Read `code.py` content
    with open(code_file_path, "r", encoding="utf-8") as code_file:
        code_content = code_file.read()

    # Find the script that imported this package
    importing_script = None
    for frame in reversed(inspect.stack()):
        if frame.filename not in ["<string>", "<stdin>", None]:  # Skip interactive environments
            importing_script = os.path.abspath(frame.filename)
            break

    if not importing_script:
        print("⚠️ Could not detect a valid script file. Skipping pasting.")
        return

    # Ensure not modifying the package itself
    if importing_script != os.path.abspath(__file__):
        with open(importing_script, "a", encoding="utf-8") as target_file:
            target_file.write("\n\n# --- Pasted Code from sklearnPra ---\n")
            target_file.write(code_content)
            target_file.write("\n# --- End of Pasted Code ---\n")

# Auto-execute on import
paste_code_in_importing_file()
