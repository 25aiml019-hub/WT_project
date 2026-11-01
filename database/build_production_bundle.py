import os
import zipfile
import hashlib
import sys

BUNDLE_NAME = "studenthub_production_bundle.zip"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Directories to include fully
INCLUDE_DIRS = [
    "admin",
    "api",
    "app",
    "public",
    "student"
]

# Specific files to include from root
ROOT_FILES = [
    ".htaccess",
    "index.php",
    "index.html",
    "process-logout.php",
    "csrf-token.php",
    "process-login.php",
    "serve-poster.php",
    ".env.production.example",
    "README.md"
]

# Storage structure to include
STORAGE_DIRS = [
    "storage/data",
    "storage/logs",
    "storage/uploads/posters",
    "storage/uploads/marksheets"
]

# Database files to include
DATABASE_FILES = [
    "database/production_complete_migration.sql"
]

# Files/extensions to exclude
EXCLUDE_EXTS = {".pyc", ".log", ".tmp"}
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db", ".env"}

print(f"Building production bundle: {BUNDLE_NAME}...")

zip_path = os.path.join(PROJECT_ROOT, BUNDLE_NAME)
if os.path.exists(zip_path):
    os.remove(zip_path)

file_count = 0
total_size = 0

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 1. Add ROOT_FILES
    for fname in ROOT_FILES:
        fpath = os.path.join(PROJECT_ROOT, fname)
        if os.path.exists(fpath):
            zipf.write(fpath, fname)
            file_count += 1
            total_size += os.path.getsize(fpath)
            print(f"  + Added: {fname}")

    # 2. Add INCLUDE_DIRS
    for dname in INCLUDE_DIRS:
        dir_full = os.path.join(PROJECT_ROOT, dname)
        for root, dirs, files in os.walk(dir_full):
            # Exclude __pycache__
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in EXCLUDE_EXTS or file in EXCLUDE_NAMES:
                    continue
                file_full = os.path.join(root, file)
                rel_path = os.path.relpath(file_full, PROJECT_ROOT).replace("\\", "/")
                zipf.write(file_full, rel_path)
                file_count += 1
                total_size += os.path.getsize(file_full)

    # 3. Add STORAGE_DIRS (.gitkeep, .htaccess)
    for sdir in STORAGE_DIRS:
        sdir_full = os.path.join(PROJECT_ROOT, sdir)
        if os.path.exists(sdir_full):
            for file in os.listdir(sdir_full):
                file_full = os.path.join(sdir_full, file)
                if os.path.isfile(file_full) and (file.startswith(".htaccess") or file.startswith(".gitkeep")):
                    rel_path = os.path.relpath(file_full, PROJECT_ROOT).replace("\\", "/")
                    zipf.write(file_full, rel_path)
                    file_count += 1
                    total_size += os.path.getsize(file_full)
                    print(f"  + Added: {rel_path}")

    # 4. Add DATABASE_FILES
    for db_file in DATABASE_FILES:
        db_full = os.path.join(PROJECT_ROOT, db_file)
        if os.path.exists(db_full):
            rel_path = db_file.replace("\\", "/")
            zipf.write(db_full, rel_path)
            file_count += 1
            total_size += os.path.getsize(db_full)
            print(f"  + Added: {rel_path} ({os.path.getsize(db_full):,} bytes)")

bundle_size = os.path.getsize(zip_path)

# Calculate SHA256 checksum
sha256 = hashlib.sha256()
with open(zip_path, "rb") as f:
    for chunk in iter(lambda: f.read(65536), b""):
        sha256.update(chunk)
checksum = sha256.hexdigest()

print("\n" + "=" * 70)
print(f"PRODUCTION BUNDLE SUCCESSFULLY CREATED!")
print(f"Location:  {zip_path}")
print(f"Zip Size:  {bundle_size:,} bytes ({bundle_size / (1024*1024):.2f} MB)")
print(f"Files:     {file_count} files included")
print(f"Raw Size:  {total_size:,} bytes ({total_size / (1024*1024):.2f} MB)")
print(f"SHA-256:   {checksum}")
print("=" * 70)
