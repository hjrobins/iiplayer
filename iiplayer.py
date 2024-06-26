import os
import sys
import subprocess
import json
import argparse

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

def get_size(selected_file):
    #size_in_bytes = os.path.getsize(selected_file)
    #size_mb = size_in_bytes / (1024 * 1024)  # Convert bytes to megabytes
    #size_mb *= 1.05  # Add a 5% buffer
    
    ffprobe_cmd = f'ffprobe -hide_banner -v error -select_streams v:0 -show_entries stream=bit_rate -print_format json "{selected_file}"'
    process = subprocess.Popen(ffprobe_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=False)
    print(selected_file)
    out, err =  process.communicate()
    if len(out)>0: # ** if result okay
        print("==========output==========")
        result = json.loads(out)
        bitrate = result["streams"][0]["bit_rate"]
        print(bitrate)
    else:
        result = {}
    if err:
        print("========= error ========")
        print(err)
    return f"-b:v {int(bitrate)/1000}k"
   
    
def generate_ffmpeg_command(selected_file, bitrate, ffmpeg_output, extension, two_pass, interlaced, invert):
    output_file = selected_file.replace(".mp4", f"_new.{extension}")
    if two_pass == False:
        return (
              f'ffmpeg -hide_banner -i "{selected_file}" -filter_complex "'+f"[0:v]select='mod(n-1,2)'[top],[0:v]select='not(mod(n-1,2))'[bottom],[{invert[0]}]field=top[t],[{invert[1]}]field=bottom[b],[t][b]vstack,il=l=i:c=i"+f'{interlaced[0]}" -r 25 {ffmpeg_output} {bitrate} {interlaced[1]} "{output_file}"'
        )
    else:
        one = f'ffmpeg -hide_banner -i "{selected_file}" -filter_complex "'+f"[0:v]select='mod(n-1,2)'[top],[0:v]select='not(mod(n-1,2))'[bottom],[{invert[0]}]field=top[t],[{invert[1]}]field=bottom[b],[t][b]vstack,il=l=i:c=i"+f'{interlaced[0]}" -r 25 {ffmpeg_output} {bitrate} {interlaced[1]} -pass 1 -f null /dev/null && '
        two = f'ffmpeg -hide_banner -i "{selected_file}" -filter_complex "'+f"[0:v]select='mod(n-1,2)'[top],[0:v]select='not(mod(n-1,2))'[bottom],[{invert[0]}]field=top[t],[{invert[1]}]field=bottom[b],[t][b]vstack,il=l=i:c=i"+f'{interlaced[0]}" -r 25 {ffmpeg_output} {bitrate} {interlaced[1]} -pass 2 "{output_file}"'
        return (one+two)

def main():
    parser = argparse.ArgumentParser(description="A little tool to convert iPlayer 50p files to 25i/p")
    parser.add_argument("input_string", help="Add the PID or filename")
    parser.add_argument("-interlaced", action="store_true", help="Enable interlaced output TFF")
    parser.add_argument("-interlacedbff", action="store_true", help="Enable interlaced output BFF")
    parser.add_argument("-invert", action="store_true", help="Swaps to even frames for bottom fields etc")
    args = parser.parse_args()
    
    inverted = args.invert
    
    input_string = args.input_string
    invert = []
    
    if inverted == True:
        invert = ["bottom", "top"]
        print("invert is true")
    else:
        invert = ["top", "bottom"]
        print("invert is false")


    if args.interlaced == True:
        print("Interlace is True TFF")
        interlaced = [",setfield=tff", "-flags +ildct"]
    elif args.interlacedbff == True:
        interlaced = [",setfield=bff", "-flags +ildct"]
        print("Interlace is True BFF")
    else:
        interlaced = ["",""]    
    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "iiplayer.bat")
    print(file_path)
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                folder_path = lines[0].strip().split("; ", 1)[1]
                folder_path = os.path.expandvars(folder_path)
                ffmpeg_output = lines[1].strip().split("; ", 1)[1]
                keep_bitrate = lines[2].strip().split("; ", 1)[1]
                extension = lines[3].strip().split("; ", 1)[1]
                two_pass = lines[4].strip().split("; ", 1)[1]
                
                if keep_bitrate.lower() == "true":
                    keep_bitrate = True
                else:
                    keep_bitrate = False
                    
                if two_pass.lower() == "true":
                    two_pass = True
                elif two_pass.lower() == "false":
                    two_pass = False
                else:
                    print("two_pass not set")
    
                print(f"Folder path: {folder_path}")
                print(f"FFmpeg output command: {ffmpeg_output}")
                print(f"Keep original bitrate: {keep_bitrate}")
                print(f"Output extension: {extension}")
                print(f"Output extension: {two_pass}")
            else:
                print("default file needs five lines. iPlayer recording folder. ffmpeg command. Keep Bitrate. File extension. Two pass")
    except FileNotFoundError:
        print("You're not running this using iiplayer.bat")
    

    found_files = search_files(input_string, folder_path)
    display_matching_files(found_files)
    
    if found_files:
        if len(found_files) == 1:
            selected_file = found_files[0]
            
            if keep_bitrate == True:
                bitrate = get_size(selected_file)
            else:
                bitrate = ""
        
            ffmpeg_cmd = generate_ffmpeg_command(selected_file, bitrate, ffmpeg_output, extension, two_pass, interlaced, invert)
            print(f"ffmpeg command:\n{ffmpeg_cmd}")
            subprocess.run(ffmpeg_cmd, shell=True)
        else:
            try:
                choice = int(input("Enter the number corresponding to the desired file: "))
                if 1 <= choice <= len(found_files):
                    selected_file = found_files[choice - 1]
                    bitrate = get_size(selected_file)

                    ffmpeg_cmd = generate_ffmpeg_command(selected_file, bitrate, ffmpeg_output, extension, two_pass, interlaced, invert)
                    print(f"ffmpeg command:\n{ffmpeg_cmd}")
                    subprocess.run(ffmpeg_cmd, shell=True)
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
