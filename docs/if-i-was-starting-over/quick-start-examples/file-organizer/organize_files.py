#!/usr/bin/env python3
"""
File Organizer Script
--------------------
This script organizes files in your Downloads folder by moving them into
category-specific folders based on their file types.

How it works:
1. Looks at each file in your Downloads folder
2. Checks the file type (extension)
3. Creates a folder for that type if it doesn't exist
4. Moves the file into the appropriate folder

Feel free to modify the CATEGORY_MAPPING to add your own categories!
"""

import os
import shutil
from pathlib import Path

# This maps file extensions to folder names
# Add or modify categories as needed!
CATEGORY_MAPPING = {
    # Images
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    
    # Documents
    '.pdf': 'Documents',
    '.doc': 'Documents',
    '.docx': 'Documents',
    '.txt': 'Documents',
    
    # Audio
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.m4a': 'Audio',
    
    # Video
    '.mp4': 'Video',
    '.mov': 'Video',
    '.avi': 'Video',
    
    # Archives
    '.zip': 'Archives',
    '.rar': 'Archives',
    '.7z': 'Archives',
    
    # Code
    '.py': 'Code',
    '.js': 'Code',
    '.html': 'Code',
    '.css': 'Code',
}

def organize_downloads():
    """
    Main function that organizes your Downloads folder.
    """
    # Get the path to the Downloads folder
    # This works on Windows, Mac, and Linux
    downloads_path = str(Path.home() / "Downloads")
    
    # Print a welcome message
    print("🗂️  Starting to organize your Downloads folder...")
    print(f"📁 Looking in: {downloads_path}")
    
    # Keep track of what we do
    files_moved = 0
    folders_created = 0
    
    # Go through each file in the Downloads folder
    for filename in os.listdir(downloads_path):
        # Get the full path to the file
        file_path = os.path.join(downloads_path, filename)
        
        # Skip if it's a folder
        if os.path.isdir(file_path):
            continue
        
        # Get the file extension (like .pdf, .jpg, etc.)
        # Convert to lowercase to match our mapping
        file_extension = os.path.splitext(filename)[1].lower()
        
        # Figure out which category folder to use
        category = CATEGORY_MAPPING.get(file_extension, 'Other')
        
        # Create the category folder if it doesn't exist
        category_path = os.path.join(downloads_path, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            print(f"📁 Created new folder: {category}")
            folders_created += 1
        
        # Move the file to its category folder
        try:
            # Create the destination path
            destination = os.path.join(category_path, filename)
            
            # If a file with this name already exists, add a number to the filename
            if os.path.exists(destination):
                base, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(destination):
                    new_filename = f"{base}_{counter}{extension}"
                    destination = os.path.join(category_path, new_filename)
                    counter += 1
            
            # Move the file
            shutil.move(file_path, destination)
            print(f"✅ Moved: {filename} → {category}")
            files_moved += 1
            
        except Exception as e:
            print(f"❌ Error moving {filename}: {str(e)}")
    
    # Print a summary of what we did
    print("\n📊 Summary:")
    print(f"Files organized: {files_moved}")
    print(f"New folders created: {folders_created}")
    print("\n✨ All done! Your Downloads folder is now organized!")

if __name__ == "__main__":
    # This is where the script starts running
    try:
        organize_downloads()
    except KeyboardInterrupt:
        print("\n\n🛑 Organization stopped by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
    
    # Wait for user input before closing
    input("\nPress Enter to exit...")
