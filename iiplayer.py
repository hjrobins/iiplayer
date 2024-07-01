import os
import sys
import subprocess

def search_files(input_string, folder_path):
    matching_files = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if input_string in filename and filename.lower().endswith(".mp4"):
                matching_files.append(os.path.join(root, filename))
    return matching_files
    
def display_matching_files(matching_files):
    if not matching_files:
        print(f"No files matching the input string found in the folder.")
        return

    print("Matching files:")
    for i, file_path in enumerate(matching_files, start=1):
        print(f"{i}. {file_path}")

def get_size(file_location):
    size_in_bytes = os.path.getsize(file_location)
    size_mb = size_in_bytes / (1024 * 1024)  # Convert bytes to megabytes
    size_mb *= 1.05  # Add a 5% buffer
    return int(size_mb)

def generate_staxrip_command(selected_file, size_mb):
    return (
        f'"C:\\Program Files\\StaxRip\\StaxRip.exe" '
        f'-LoadTemplate:"iPlayer Interlace" "{selected_file}" -SetSize:{size_mb} -StartEncoding -ExitWithoutSaving'
    )

def delete_files(selected_file):
    selected_file = os.path.splitext(selected_file)[0]
    try:
        shutil.rmtree(selected_file)  # Remove the entire directory tree
    except FileNotFoundError:
        # Handle the case where the directory does not exist
        pass
    try:
        os.remove(selected_file + ".mp4")  # Remove the .mp4 file
    except FileNotFoundError:
        # Handle the case where the .mp4 file does not exist
        pass
    try:
        os.rename(selected_file + "_new.mp4", selected_file + ".mp4")
        return f"File renamed to {selected_file}.mp4""
    except FileNotFoundError:
        return "File not found"
        
        
        
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_string>")
        sys.exit(1)

    input_string = sys.argv[1]
    folder_path = r"C:\Users\Harry\Desktop\iPlayer Recordings"

    found_files = search_files(input_string, folder_path)
    display_matching_files(found_files)

    if found_files:
        if len(found_files) == 1:
            selected_file = found_files[0]
            size_mb = get_size(selected_file)
            print(f"Size: {size_mb:.2f} MB")

            stax_cmd = generate_staxrip_command(selected_file, size_mb)
            print(f"StaxRip command:\n{stax_cmd}")
            subprocess.run(stax_cmd, shell=True)
            delete_files(selected_file)
        else:
            try:
                choice = int(input("Enter the number corresponding to the desired file: "))
                if 1 <= choice <= len(found_files):
                    selected_file = found_files[choice - 1]
                    size_mb = get_size(selected_file)
                    print(f"Size: {size_mb:.2f} MB")

                    stax_cmd = generate_staxrip_command(selected_file, size_mb)
                    print(f"StaxRip command:\n{stax_cmd}")
                    subprocess.run(stax_cmd, shell=True)
                    delete_files(selected_file)
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
