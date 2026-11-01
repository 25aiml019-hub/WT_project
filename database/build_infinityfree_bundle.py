import os
import zipfile
import hashlib

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUNDLE_NAME = "studenthub_infinityfree_bundle.zip"
ZIP_PATH = os.path.join(PROJECT_ROOT, BUNDLE_NAME)

INCLUDE_DIRS = ["admin", "api", "app", "public", "student"]
ROOT_FILES = [
    ".htaccess",
    "index.php",
    "index.html",
    "process-logout.php",
    "csrf-token.php",
    "process-login.php",
    "serve-poster.php",
    ".env.infinityfree.example",
    "README.md",
    "docs/INFINITYFREE_DEPLOYMENT_GUIDE.md",
    "docs/INFINITYFREE_COMPATIBILITY_REPORT.md",
    "docs/INFINITYFREE_SECURITY_AUDIT.md"
]

STORAGE_DIRS = [
    "storage/data",
    "storage/logs",
    "storage/uploads/posters",
    "storage/uploads/marksheets"
]

MIGRATION_SOURCE = os.path.join(PROJECT_ROOT, "database", "verified_backups", "studenthub_infinityfree_migration.sql")
MIGRATION_IN_ZIP = "database/studenthub_infinityfree_migration.sql"

EXCLUDE_EXTS = {".pyc", ".log", ".tmp"}
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db", ".env"}

print(f"Building InfinityFree production bundle: {BUNDLE_NAME}...")

if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)

file_count = 0
total_size = 0

with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 1. Root files
    for fname in ROOT_FILES:
        fpath = os.path.join(PROJECT_ROOT, fname)
        if os.path.exists(fpath):
            zipf.write(fpath, fname)
            file_count += 1
            total_size += os.path.getsize(fpath)
            print(f"  + Added root file: {fname}")

    # 2. Application directories
    for dname in INCLUDE_DIRS:
        dir_full = os.path.join(PROJECT_ROOT, dname)
        for root, dirs, files in os.walk(dir_full):
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

    # 3. Storage directory structure with .htaccess and .gitkeep
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
                    print(f"  + Added storage anchor: {rel_path}")

    # 4. Verified portable database migration
    if os.path.exists(MIGRATION_SOURCE):
        zipf.write(MIGRATION_SOURCE, MIGRATION_IN_ZIP)
        file_count += 1
        total_size += os.path.getsize(MIGRATION_SOURCE)
        print(f"  + Added database migration: {MIGRATION_IN_ZIP} ({os.path.getsize(MIGRATION_SOURCE):,} bytes)")

bundle_size = os.path.getsize(ZIP_PATH)

sha256 = hashlib.sha256()
with open(ZIP_PATH, "rb") as f:
    for chunk in iter(lambda: f.read(65536), b""):
        sha256.update(chunk)
checksum = sha256.hexdigest()

print("\n" + "=" * 80)
print("INFINITYFREE PRODUCTION BUNDLE CREATED SUCCESSFULLY")
print(f"Location:  {ZIP_PATH}")
print(f"Zip Size:  {bundle_size:,} bytes ({bundle_size / (1024*1024):.2f} MB)")
print(f"Files:     {file_count} files included")
print(f"SHA-256:   {checksum}")
print("=" * 80)
