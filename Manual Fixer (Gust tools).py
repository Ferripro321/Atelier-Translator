"""
This tool is made for specific cases where Chat GPT won't output correctly and you can't manage to fix it with the promp.

How to use it:

1) Run Atelier Translator.py
 -> [WARNING] Only continue if you get an error because Chat GPT Fucked up.
2) Manually fix output.txt (Check ExtractedStrings.txt to check original file strings)
 -> [TIP] Both files must have the same lines, this is usually the problem. Make sure Chat GPT didn't jump lines by accident on output.txt
3) Change file_to_fix to the name of the json you wanna fix
4) Change file_to_fix_folder to the name of the folder where the json you wanna fix is
5) Run the program and it will output the translated json in folder_initial/JSON/T

Enjoy (;
"""

from functions import *

file_to_fix_folder = "" # Example: mm04
file_to_fix = "" # Example event_message_mm04_260.json

local_folder = os.path.dirname(os.path.abspath(__file__)) + "/"
load_dotenv(local_folder + "settings.env")


event_folder = os.getenv("EVENT_FOLDER")
event_folder = event_folder.replace("\\", "/")

extracted_strings_path = local_folder + "Errors/extracted-strings-" + file_to_fix + ".txt"
output_path = local_folder + "Errors/output-" + file_to_fix + ".txt"

ebm_folder = event_folder + "/" + file_to_fix_folder

gust_ebm = os.getenv("GUST_EBM_PATH")
gust_ebm = gust_ebm.replace("\\", "/")


print(count_lines(output_path))
print(count_lines(extracted_strings_path))

if count_lines(output_path) == count_lines(extracted_strings_path): 
    print("Seems OK")
    with open(output_path, "r", encoding="utf-8") as file:
            output = file.read()
    output = remove_empty_lines(output)

    with open(ebm_folder + "/" + file_to_fix, "r", encoding="utf-8") as file:
            file_contents = file.read()

    replaced_json = re.sub(r'0x([0-9a-fA-F]+)', replace_hex_values, file_contents)
    decoded_json = json.loads(replaced_json)
    for i, linea in enumerate(output):
                decoded_json['messages'][i]['msg_string'] = linea.strip()
    MATCH_ALL_XYZ = r'(?<![a-zA-Z\"])(?![\"])(\b\d+)'

    with open(ebm_folder + "/" + file_to_fix, "w", encoding="utf-8") as file:
        file.write(re.sub(MATCH_ALL_XYZ, replace_decimal_values, json.dumps(decoded_json, ensure_ascii=False)))

    move_file(ebm_folder + "/" + file_to_fix, local_folder + "Translated/" + file_to_fix_folder + "/" + file_to_fix)
    subprocess.run([gust_ebm, local_folder + "Translated/" + file_to_fix_folder + "/" + file_to_fix])
    print("New EBM created")
    remove_file(local_folder + "Translated/" + file_to_fix_folder + "/" + file_to_fix)
    remove_file(output_path)
    remove_file(extracted_strings_path)
    print("Done")
else: 
    print("File isn't fixed")

