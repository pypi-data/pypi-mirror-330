import inspect

def paste_code():
    # Jis file ne import kiya hai, uska filename nikalna
    frame = inspect.stack()[1]
    caller_filename = frame.filename

    # `code.py` ka content read karna
    with open(__file__.replace("__init__.py", "code.py"), "r") as code_file:
        code_content = code_file.read()

    # Importing file me code paste karna
    with open(caller_filename, "a") as caller_file:
        caller_file.write("\n\n# Pasted from sklearnPra\n" + code_content + "\n")

    print(f"✅ Code pasted into {caller_filename}")

# Jab package import hoga, yeh function chalega
paste_code()
