"""
This tool is made for specific cases where Chat GPT won't output correctly and you can't manage to fix it with the promp.

How to use it:

1) Run Atelier Translator.py
 -> [WARNING] Only continue if you get an error because Chat GPT Fucked up.
2) Manually fix output.txt (Check ExtractedStrings.txt to check original file strings)
 -> [TIP] Both files must have the same lines, this is usually the problem. Make sure Chat GPT didn't jump lines by accident on output.txt
3) Change file_to_fix to the name of the json you wanna fix
4) Change file_to_fix_folder to the name of the folder where the json you wanna fix is
5) Run the program and it will fix the file

Enjoy (;
"""

from functions import *


file_to_fix_folder = "" # Example: mm01
file_to_fix = "" # Example: event_message_mm01_140.ebm

local_folder = os.path.dirname(os.path.abspath(__file__)) + "/"

load_dotenv(local_folder + "settings.env")

event_folder = os.getenv("EVENT_FOLDER")
event_folder = event_folder.replace("\\", "/")
ebm_folder = event_folder + "/" + file_to_fix_folder

a24_ebm = local_folder + "/Custom Dumper/Dumper.exe"

extracted_strings_path = local_folder + "Errors/extracted-strings-" + file_to_fix + ".txt"
output_path = local_folder + "Errors/output-" + file_to_fix + ".txt"

print(count_lines(output_path))
print(count_lines(extracted_strings_path))

if count_lines(output_path) == count_lines(extracted_strings_path): 
    print("Seems OK")
    subprocess.run([a24_ebm, "--replace-strings", ebm_folder + "/" + file_to_fix, output_path], cwd=local_folder)
    print("New EBM created")
    move_file(local_folder + "modified.ebm", local_folder + "Translated/" + file_to_fix_folder + "/modified.ebm")
    rename_file(local_folder + "Translated/" + file_to_fix_folder + "/modified.ebm", local_folder + "Translated/" + file_to_fix_folder + "/" + file_to_fix)
    print("Done")
else: 
    print("File isn't fixed")

