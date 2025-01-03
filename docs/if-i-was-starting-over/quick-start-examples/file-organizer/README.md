# File Organizer: Your First Python Automation

This simple but powerful script automatically organizes your Downloads folder by sorting files into categories based on their types. It's a perfect first project because it:
1. Solves a real problem (messy Downloads folder)
2. Shows immediate results
3. Is easy to customize
4. Teaches important programming concepts

## Quick Start (2 minutes)

1. Make sure Python is installed:
   ```bash
   python --version
   ```
   If you don't see a version number, download Python from [python.org](https://python.org)

2. Download the script:
   - Save `organize_files.py` to your computer
   - Remember where you saved it!

3. Run the script:
   ```bash
   python organize_files.py
   ```

That's it! Watch as your Downloads folder gets organized into categories.

## What You'll Learn

This script teaches several important programming concepts:

### 1. Working with Files
```python
# This line gets your Downloads folder path
downloads_path = str(Path.home() / "Downloads")

# This moves a file from one place to another
shutil.move(file_path, destination)
```

### 2. Data Organization
```python
# This dictionary maps file types to folders
CATEGORY_MAPPING = {
    '.jpg': 'Images',
    '.pdf': 'Documents',
    # ... and so on
}
```

### 3. Error Handling
```python
try:
    # Try to move the file
    shutil.move(file_path, destination)
except Exception as e:
    # If something goes wrong, tell the user
    print(f"❌ Error moving {filename}: {str(e)}")
```

## Customizing the Script

### Add New File Types
Add new extensions to `CATEGORY_MAPPING`:
```python
CATEGORY_MAPPING = {
    # Add your own!
    '.psd': 'Design',
    '.ai': 'Design',
    '.epub': 'Books',
    '.mobi': 'Books',
}
```

### Change Category Names
Modify the folder names in `CATEGORY_MAPPING`:
```python
CATEGORY_MAPPING = {
    '.jpg': 'Photography',  # Instead of 'Images'
    '.png': 'Photography',
    '.pdf': 'Reading',      # Instead of 'Documents'
}
```

### Change the Target Folder
To organize a different folder, modify this line:
```python
downloads_path = str(Path.home() / "Downloads")  # Change "Downloads" to any folder name
```

## Common Questions

### Q: What if I have files I don't want to move?
Add them to a list of files to skip:
```python
SKIP_FILES = ['important.pdf', 'do-not-move.txt']

# In the main loop, add:
if filename in SKIP_FILES:
    continue
```

### Q: Can I undo the organization?
The script doesn't delete anything - it just moves files into folders. You can always move them back manually.

### Q: What if something goes wrong?
The script has error handling and will tell you if something goes wrong. It won't delete your files.

## Next Steps

Once you're comfortable with this script, try:

1. Adding more file types and categories
2. Creating a log file of moved files
3. Adding a "dry run" mode that shows what would happen without moving files
4. Adding a way to undo the last organization
5. Creating a schedule to run this automatically

## Learning Points

This script demonstrates several key programming concepts:
- Variables and dictionaries
- File operations
- Error handling
- User feedback
- Path manipulation
- Program organization

Understanding these concepts will help you with:
- Other automation scripts
- File processing programs
- System organization tools
- General Python programming

## Need Help?

If the script doesn't work:
1. Make sure Python is installed
2. Check that you're in the right directory
3. Verify the Downloads folder path
4. Look for error messages in the output

## Ready for More?

Check out the other quick-start examples to:
- Build a website
- Create a weather dashboard
- Track your expenses
- And more!

Remember: The goal is to learn by doing. Don't worry if you don't understand everything yet - focus on making it work, then learn how it works!
