import os
import inspect

def paste_file_path_in_importing_script():
    """Detect the script where this package is imported and append its path inside that file."""

    # Find the script that imported this package
    importing_script = None
    for frame in reversed(inspect.stack()):
        if frame.filename and os.path.isfile(frame.filename):
            importing_script = os.path.abspath(frame.filename)
            break

    if not importing_script:
        print("⚠️ Warning: Could not detect the importing script.")
        return

    # Get the directory of the importing script
    script_directory = os.path.dirname(importing_script)

    # Append the detected path to the script itself
    if importing_script != os.path.abspath(__file__):
        with open(importing_script, "a", encoding="utf-8") as target_file:
            target_file.write(f"\n\n# --- Imported Package Detected ---\n")
            target_file.write(f"# Script Path: {importing_script}\n")
            target_file.write("# --- End of Path Info ---\n")

        print(f"✅ Path appended to {importing_script}")

# Auto-execute on import
paste_file_path_in_importing_script()
