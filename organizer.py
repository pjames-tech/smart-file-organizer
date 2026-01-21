"""
Smart File Organizer
Automatically organizes files in a directory based on their types.
"""

import os
import shutil
from pathlib import Path
from config import FILE_CATEGORIES, DEFAULT_SOURCE_DIR, DEFAULT_DEST_DIR


def get_category(file_extension: str) -> str:
    """
    Determine the category of a file based on its extension.
    
    Args:
        file_extension: The file extension (e.g., '.pdf', '.jpg')
    
    Returns:
        The category name or 'Other' if not found.
    """
    ext = file_extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"


def organize_files(source_dir: str = None, dest_dir: str = None) -> dict:
    """
    Organize files from source directory into categorized folders.
    
    Args:
        source_dir: Directory containing files to organize
        dest_dir: Directory where organized folders will be created
    
    Returns:
        Dictionary with statistics about organized files.
    """
    source = Path(source_dir or DEFAULT_SOURCE_DIR)
    destination = Path(dest_dir or DEFAULT_DEST_DIR)
    
    if not source.exists():
        raise FileNotFoundError(f"Source directory not found: {source}")
    
    stats = {"moved": 0, "skipped": 0, "errors": 0}
    
    for file_path in source.iterdir():
        if file_path.is_file():
            try:
                category = get_category(file_path.suffix)
                category_dir = destination / category
                category_dir.mkdir(parents=True, exist_ok=True)
                
                dest_path = category_dir / file_path.name
                
                # Handle duplicate filenames
                if dest_path.exists():
                    base = file_path.stem
                    ext = file_path.suffix
                    counter = 1
                    while dest_path.exists():
                        dest_path = category_dir / f"{base}_{counter}{ext}"
                        counter += 1
                
                shutil.move(str(file_path), str(dest_path))
                print(f"Moved: {file_path.name} -> {category}/")
                stats["moved"] += 1
                
            except Exception as e:
                print(f"Error moving {file_path.name}: {e}")
                stats["errors"] += 1
        else:
            stats["skipped"] += 1
    
    return stats


def main():
    """Main entry point for the file organizer."""
    print("=" * 50)
    print("Smart File Organizer")
    print("=" * 50)
    
    source = input(f"Source directory [{DEFAULT_SOURCE_DIR}]: ").strip() or None
    dest = input(f"Destination directory [{DEFAULT_DEST_DIR}]: ").strip() or None
    
    print("\nOrganizing files...")
    stats = organize_files(source, dest)
    
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Files moved: {stats['moved']}")
    print(f"  Skipped (directories): {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
