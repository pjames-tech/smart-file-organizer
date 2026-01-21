# Smart File Organizer

A Python utility that automatically organizes files into categorized folders based on their file types.

## Features

- 📁 Automatically categorizes files by type (Images, Documents, Videos, Audio, etc.)
- ⚙️ Customizable file categories and extensions
- 🔄 Handles duplicate filenames automatically
- 📊 Provides summary statistics after organization

## Installation

1. Clone this repository or download the files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the organizer with default settings:

```bash
python organizer.py
```

### How it Works

1. **Run the script** - You'll see a welcome banner
2. **Source directory prompt** - Press **Enter** to use default (Downloads), or type a custom path
3. **Destination directory prompt** - Press **Enter** for default, or type a custom path
4. **Automatic organization** - Files are moved into category folders (Images, Documents, Videos, etc.)
5. **Summary** - Shows how many files were moved, skipped, or had errors

**Example session:**

```
==================================================
Smart File Organizer
==================================================
Source directory [C:\Users\Victor\Downloads]:          <- Press Enter
Destination directory [C:\Users\Victor\Downloads\Organized]:   <- Press Enter

Organizing files...
Moved: photo.jpg -> Images/
Moved: report.pdf -> Documents/

==================================================
Summary:
  Files moved: 2
  Skipped (directories): 0
  Errors: 0
==================================================
```

### Custom Directories

You'll be prompted to enter:

- **Source directory**: Where your unorganized files are located (default: Downloads)
- **Destination directory**: Where organized folders will be created

## Configuration

Edit `config.py` to customize:

- **DEFAULT_SOURCE_DIR**: Default source directory
- **DEFAULT_DEST_DIR**: Default destination directory
- **FILE_CATEGORIES**: Dictionary mapping category names to file extensions

### Default Categories

| Category    | Extensions                                 |
| ----------- | ------------------------------------------ |
| Images      | .jpg, .jpeg, .png, .gif, .bmp, .svg, etc.  |
| Documents   | .pdf, .doc, .docx, .txt, .xls, .xlsx, etc. |
| Videos      | .mp4, .mkv, .avi, .mov, .wmv, etc.         |
| Audio       | .mp3, .wav, .flac, .aac, .ogg, etc.        |
| Archives    | .zip, .rar, .7z, .tar, .gz, etc.           |
| Code        | .py, .js, .html, .css, .java, etc.         |
| Executables | .exe, .msi, .bat, .sh, etc.                |
| Fonts       | .ttf, .otf, .woff, .woff2                  |

## License

MIT License
