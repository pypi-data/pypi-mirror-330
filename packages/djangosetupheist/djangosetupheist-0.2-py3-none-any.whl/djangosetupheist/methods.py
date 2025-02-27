import re

def get_settings_folder(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    match = re.search(r'os\.environ\.setdefault\("DJANGO_SETTINGS_MODULE",\s*["\'](.+?)\.settings["\']\)', content)
    return match.group(1) if match else None