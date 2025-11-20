import os
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'sistema-calificaciones-backend.zip')

EXCLUDE_DIRS = {'.venv', '.git', '__pycache__', 'venv', '.venv\Scripts'}
EXCLUDE_FILES = {'.DS_Store'}

def should_exclude(path):
    parts = set(path.split(os.sep))
    if parts & EXCLUDE_DIRS:
        return True
    name = os.path.basename(path)
    if name in EXCLUDE_FILES:
        return True
    if name.endswith('.pyc'):
        return True
    return False

with zipfile.ZipFile(OUT, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for foldername, subfolders, filenames in os.walk(ROOT):
        # Skip excluded dirs by mutating subfolders in-place
        subfolders[:] = [d for d in subfolders if not should_exclude(os.path.join(foldername, d))]
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            relpath = os.path.relpath(filepath, ROOT)
            if should_exclude(relpath):
                continue
            # Do not include the output zip itself if re-run
            if relpath == os.path.basename(OUT):
                continue
            zf.write(filepath, relpath)

print(f"Created {OUT}")
