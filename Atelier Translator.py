"""
This is the main translation tool.
It unpacks the EBM files of Gust games and decodes the json files on them to then get the text of the game and use Open AI Chat GPT 3.5 turbo model
to translate it to any language you wish, then it creates a new json file with the translated text that Chat GPT returned and builds it again into an EBM file.

[Note]: Due to the font that the game uses there is a high chance that some languages won't display correctly or will show white squares, i might release something
to change the font of the game.

How to use it:

1) Open or create a file called settings.env and place the following code:

OPENAI_API_KEY=YOUR-OPENAI-KEY-HERE # replace YOUR-OPENAI-KEY-HERE with the key you can find in https://platform.openai.com/account/api-keys (make sure you still have the free balance or create a new account to get free 5$ -> https://platform.openai.com/account/usage)
GUST_EBM_PATH=PATH-TO-GUST-EBM # Replace PATH-TO-GUST-EBM with the path of your gust ebm. Example: C:/Users/Ferra/Desktop/gust_tools/gust_ebm.exe (Download it here: https://github.com/VitaSmith/gust_tools/releases)
EVENT_FOLDER=YOUR-UNPACKED-GAME-EVENT-PATH # Replace YOUR-UNPACKED-GAME-EVENT-PATH with the event_en / any event_ folder found on the unpacked game files (guide will be included in next steps) Example: C:/Users/Ferra/Desktop/Sophie 2 unpack/event/event_en
CUSTOMDUMPER=True/False # Replace True/False with True if you wanna use the tool for Ryza 3 or a more recent game, False for older games than Ryza 3
DEBUGER=False # Put True if you know what you are doing, but you probably wanna keep this at False.

2) Scroll down on this file and in promp change Spanish to the language you wanna translate to.

3) Go to your game files, go to data folder of the game, copy "PACK01.PAK" and paste it on a new folder that you can create on your desktop.

4) Drag the PACK01.PAK that you have on the folder you created to gust_pak.exe (Download it here: https://github.com/VitaSmith/gust_tools/releases)

5) Now you will see some folders and files, go to event, then event_en (This is the folder path you have to put on YOUR-UNPACKED-GAME-EVENT-PATH)

6) Open the Microsoft store

7) Search "Python 3.11" and install it

8) Now open cmd (windows key + R and type cmd, then click enter)

9) Put the following commands one by one on the cmd (only needed the first time):
        pip install openai
        pip install pyperclip
        pip install colorama
        pip install python-dotenv

10) Now enter this command replace <PATH_WHERE_YOU_HAVE_ATELIER_TRANSLATOR> with the path to the atelier translator folder, example: C:/Users/Ferra/Desktop/Atelier Translator:
        cd "<PATH_WHERE_YOU_HAVE_ATELIER_TRANSLATOR>"

11) Now run the program by entering this command:
        python "Atelier Translator.py"

12) Enjoy.

[!] If you get an error because Chat GPT fucked up check instructions on Manual Fixer.py
[?] If you don't understand too much this look for a tutorial on Youtube as ill upload one.
"""

from functions import *

local_folder = os.path.dirname(os.path.abspath(__file__)) + "/"

load_dotenv(local_folder + "settings.env")

openai.api_key = os.getenv("OPENAI_API_KEY")

# Start Logo and Credits
start()

if os.getenv("DEBUGER") == "True":
    DEBUGER = True
elif os.getenv("DEBUGER") == "False":
    DEBUGER = False
else:
    print(Fore.RED + "Error: DEBUGER is not True/False in settings.env" +  Fore.RESET)
    exit()

if os.getenv("CUSTOMDUMPER") == "True":
    CUSTOMDUMPER = True
elif os.getenv("CUSTOMDUMPER") == "False":
    CUSTOMDUMPER = False
else:
    print(Fore.RED + "Error: CUSTOMDUMPER is not True/False in settings.env" +  Fore.RESET)
    exit()

gust_ebm = os.getenv("GUST_EBM_PATH")
gust_ebm = gust_ebm.replace("\\", "/")

ebm_folder_key = "PLACEHOLDER"

event_folder = os.getenv("EVENT_FOLDER")
event_folder = event_folder.replace("\\", "/")

a24_ebm = local_folder + "Custom Dumper/Dumper.exe"
output_path = local_folder + "output.txt"

promp = """
You are now going to be an English to Spanish translator. You must only reply the translated sentences, nothing else.

When you see a //, consider it to be the end of a sentence and start a new sentence in Spanish.

Don't leave blank/empty lines!

For example, if I give you this:
I have witnessed countless dreams.//I am all alone,//... I can't stop ... Not until I find Plachta.

You should return:

He presenciado innumerables sueños.
Estoy completamente sola,
... No puedo parar ... No hasta encontrar a Plachta.
"""

print(Fore.YELLOW + "ENV Settings:\n" + Fore.RESET)
print("CUSTOMDUMPER: ", CUSTOMDUMPER)
print("DEBUGER: ", DEBUGER)
if DEBUGER: print("OPENAI_API_KEY: ", os.getenv("OPENAI_API_KEY"))
else:  print("OPENAI_API_KEY: ", Fore.RED + "Censured" + Fore.RESET)
print("GUST_EBM_PATH: ", gust_ebm)
print("EVENT_FOLDER: ", event_folder + "\n")

ebm_folders_num = 0
current_ebm_folder_num = 0


if CUSTOMDUMPER == True:
    for ebm_folder in get_subfolder_paths(event_folder):
        ebm_folders_num += 1
    for ebm_folder in get_subfolder_paths(event_folder):
        ebm_folder_key = get_last_folder_name(ebm_folder)
        current_ebm_folder_num += 1
        print(Fore.GREEN + "Starting Folder " + ebm_folder_key + " -> " + str(current_ebm_folder_num) + " / " + str(ebm_folders_num) + Fore.RESET)
        for file_path in get_files_with_extension(ebm_folder, ".ebm"):
            if DEBUGER: print(Fore.BLUE + "1 Starting: " + file_path)
            subprocess.run([a24_ebm, "--extract-strings", file_path], cwd=local_folder)
            if DEBUGER: print("2 ->", os.path.basename(file_path))
            with open(local_folder + "extracted-strings.txt", "r", encoding="utf-8") as file:
                extracted_strings = file.read()
        
            if DEBUGER: print("3", extracted_strings)

            extracted_strings = extracted_strings.replace("\n", "//")
            extracted_strings = extracted_strings.replace("<CR>", " ")
            if DEBUGER: print("4", extracted_strings)

            print(Fore.BLUE + "Starting Translation..." + Fore.RESET)
            output = request_translation(promp, extracted_strings, file_path)
            if output == "Error":
                exit()
            print(Fore.GREEN + "Finished Translating" + Fore.RESET)

            if DEBUGER: print("5", output)

            output = remove_empty_lines(output)
            if DEBUGER: print("6", output)

            with open(output_path, "w", encoding="utf-8") as file:
                file.write("\n".join(output))
    
            if count_lines(local_folder + "output.txt") == count_lines(local_folder + "extracted-strings.txt"):
                if DEBUGER: print("Seems OK")
                subprocess.run([a24_ebm, "--replace-strings", file_path, local_folder + "output.txt"], cwd=local_folder)
                print("New EBM created")
                move_file(local_folder + "modified.ebm", local_folder + "Translated/" + ebm_folder_key + "/modified.ebm")
                rename_file(local_folder + "Translated/" + ebm_folder_key + "/modified.ebm", local_folder + "Translated/" + ebm_folder_key + "/" + os.path.basename(file_path))
            else:
                print(Fore.RED + "Chat GPT fucked up, you will manually need to fix this file later." + Fore.RESET)
                move_file(local_folder + 'extracted-strings.txt', local_folder + "Errors/" + "extracted-strings-" + os.path.splitext(os.path.basename(file_path))[0] + ".txt")
                move_file(local_folder + 'output.txt', local_folder + "Errors/" + "output-" + os.path.splitext(os.path.basename(file_path))[0] + ".txt")
else:
    for ebm_folder in get_subfolder_paths(event_folder):
        ebm_folders_num += 1
    for ebm_folder in get_subfolder_paths(event_folder):
        ebm_folder_key = get_last_folder_name(ebm_folder)
        current_ebm_folder_num += 1
        print(Fore.GREEN + "Starting Folder " + str(ebm_folder_key) + " -> " + str(current_ebm_folder_num) + " / " + ebm_folders_num + Fore.RESET)
        for file_path in get_files_with_extension(ebm_folder, ".ebm"):
            subprocess.run([gust_ebm, file_path])
            remove_file(file_path)
        for json_file in get_files_with_extension(ebm_folder, ".json"):
            with open(json_file, "r", encoding="utf-8") as file:
                file_contents = file.read()

            replaced_json = re.sub(r'0x([0-9a-fA-F]+)', replace_hex_values, file_contents)
            decoded_json = json.loads(replaced_json)
        
            msg_strings = [message['msg_string'] for message in decoded_json['messages']]
            extracted_strings = ""
            with open(local_folder + 'extracted-strings.txt', 'w', encoding="utf-8") as output_file:
                for msg_string in msg_strings:
                    extracted_strings = extracted_strings + msg_string + '\n'
                    output_file.write(msg_string + '\n')
        
            extracted_strings = extracted_strings.replace("\n", "//")
            extracted_strings = extracted_strings.replace("<CR>", " ")

            print(Fore.BLUE + "Starting Translation..." + Fore.RESET)

            output = request_translation(promp, extracted_strings, json_file)
            if output == "Error":
                exit()
            print(Fore.GREEN + "Finished Translating" + Fore.RESET)

            output = remove_empty_lines(output)

            Failed = False

            with open(output_path, "w", encoding="utf-8") as file:
                file.write("\n".join(output))

            try:
                for i, linea in enumerate(output):
                    decoded_json['messages'][i]['msg_string'] = linea.strip()
            except:
                print(Fore.RED + "Chat GPT fucked up, you will manually need to fix this file later." + Fore.RESET)
                move_file(local_folder + 'extracted-strings.txt', local_folder + "Errors/" + "extracted-strings-" + os.path.basename(json_file) + ".txt")
                move_file(local_folder + 'output.txt', local_folder + "Errors/" + "output-" + os.path.basename(json_file) + ".txt")
                Failed = True
            
            if Failed:
                print("Skipping...")
            else:
                MATCH_ALL_XYZ = r'(?<![a-zA-Z\"])(?![\"])(\b\d+)'

                with open(json_file, "w", encoding="utf-8") as file:
                    file.write(re.sub(MATCH_ALL_XYZ, replace_decimal_values, json.dumps(decoded_json, ensure_ascii=False)))
    
                move_file(json_file, local_folder + "Translated/" + ebm_folder_key + "/" + os.path.basename(json_file))
                subprocess.run([gust_ebm, local_folder + "Translated/" + ebm_folder_key + "/" + os.path.basename(json_file)])
                remove_file(local_folder + "Translated/" + ebm_folder_key + "/" + os.path.basename(json_file))
                print(Fore.GREEN + "Finished: " + json_file + Fore.RESET)

print(Fore.GREEN + "\nI'm done :D" + Fore.RESET)
