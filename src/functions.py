# This file stores the UI and CustomFileSystem functions used on Atelier Transaltor.

import json
import re
import openai
import subprocess
import shutil
import time
import os
import pyperclip
import tkinter as tk
from tkinter import filedialog
import colorama
from colorama import Fore, Style
colorama.init()
from dotenv import load_dotenv, dotenv_values, set_key, find_dotenv

model = "gpt-3.5-turbo"

local_folder = os.path.dirname(os.path.abspath(__file__)) + "/"

original_prompt = """You are now going to be an English to Spanish translator. You must only reply the translated sentences, nothing else.

When you see a //, consider it to be the end of a sentence and start a new sentence in Spanish.

Don't leave blank/empty lines!

For example, if I give you this:
I have witnessed countless dreams.//I am all alone,//... I can't stop ... Not until I find Plachta.

You should return:

He presenciado innumerables sueños.
Estoy completamente sola,
... No puedo parar ... No hasta encontrar a Plachta."""

global prompt

def read_prompt_file(file_name='prompt.txt'):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file '{file_name}' does not exist."
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"
    
def replace_hex_values(match):
    hex_value = match.group(1)
    return str(int(hex_value, 16))

def replace_decimal_values(match):
    decimal_value = match.group(1)
    return hex(int(decimal_value))

class CustomFileSystem:
    def get_files_in_folder(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                yield file_path
    
    def read_text_from_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            return file_contents

    def save_text_to_file(file_path, text_to_save):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_to_save)
            return f"Text saved to '{file_path}' successfully."
        except Exception as e:
            return f"An error occurred while saving the file: {str(e)}"
    
    def get_text_after_specific_text(file_path, specific_text):
        file_name = os.path.basename(file_path)

        if specific_text in file_name:
            text_position = file_name.index(specific_text)

            text_after_specific = file_name[text_position + len(specific_text):]
            return text_after_specific
        else:
            return None
        
    def get_files_with_extension(folder_path, extension):
        matching_files = []
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(extension):
                    file_path = os.path.join(root, file_name)
                    matching_files.append(file_path)
        return matching_files

    def remove_empty_lines(text):
        try:
            return [line for line in text.split("\n") if line.strip() != ""]
        except:
            print(Fore.YELLOW + "Empty Lines Remover Failed")
            return text

    def create_folder(path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(Fore.GREEN + f"Folder '{path}' created successfully." + Fore.RESET)
        else:
            print(Fore.RED + f"Folder '{path}' already exists." + Fore.RESET)

    def count_file_lines(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                line_count = sum(1 for _ in file)
                return line_count
        except FileNotFoundError:
            return 0
        except Exception as e:
            return "Something failed: " + str(e)
    
    def count_lines(input_string):
        lines = input_string.split('\n')
        
        line_count = len(lines)
        
        return line_count
    
    def remove_folder(folder_path):
        if not os.path.exists(folder_path):
            print("Folder not found.") 
        try:
            shutil.rmtree(folder_path)
            print("Folder successfully removed.") 
        except Exception as e:
            print(f"Error removing folder: {e}") 

    def rename_file(current_name, new_name):
        try:
            os.rename(current_name, new_name)
            print(f"File '{current_name}' renamed to '{new_name}' successfully.")
        except FileNotFoundError:
            print(f"File '{current_name}' not found.")
        except FileExistsError:
            print(f"A file named '{new_name}' already exists.")
        except Exception as e:
            print(f"An error occurred while renaming the file: {str(e)}")

    def move_file(source, destination):
        try:
            destination_folder = os.path.dirname(destination)
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(source, destination)
            print(f"File '{source}' moved to '{destination}' successfully.")
        except FileNotFoundError:
            print(f"File '{source}' not found.")
        except shutil.Error as e:
            print(f"An error occurred while moving the file: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def copy_file(source_path, destination_path):
        try:
            destination_directory = os.path.dirname(destination_path)
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)
            shutil.copy(source_path, destination_path)
            print(f"File copied from {source_path} to {destination_path}")
        except FileNotFoundError:
            print("Source file not found.")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def copy_folder(source_path, destination_path):
        if not shutil.os.path.exists(destination_path):
            shutil.os.makedirs(destination_path)
        shutil.copytree(source_path, shutil.os.path.join(destination_path, shutil.os.path.basename(source_path)))

    def remove_file(file_path):
        try:
            os.remove(file_path)
            print(f"File '{file_path}' removed successfully.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except PermissionError:
            print(f"Permission denied. Unable to remove '{file_path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_subfolder_paths(folder_path):
        subfolder_paths = []
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            if os.path.isdir(full_path):
                subfolder_paths.append(full_path)
        return subfolder_paths

    def get_last_folder_name(path):
        path = os.path.normpath(path)
        directories = path.split(os.sep)
        last_folder_name = directories[-1]
        return last_folder_name


class UI:
    def load_original_file(file):
        extracted_event_path = local_folder + "Errors/extracted-strings-" + file
        return CustomFileSystem.read_text_from_file(extracted_event_path)

    def load_file_to_edit(file):
        output_event_path = local_folder + "Errors/output-" + file
        return CustomFileSystem.read_text_from_file(output_event_path)
    
    def update_prompt(new_prompt):
        global prompt
        prompt = new_prompt
        prompt_path = local_folder + "/prompt.txt"
        try:
            CustomFileSystem.save_text_to_file(prompt_path, new_prompt)
            print(Fore.GREEN + "Saved" + Fore.RESET)
            return "Saved"
        except:
            print(Fore.GREEN + "There was an error... (Check console logs)" + Fore.RESET)
            return "There was an error... (Check console logs)"
        
    def reset_prompt():
        prompt_path = local_folder + "/prompt.txt"
        try:
            CustomFileSystem.save_text_to_file(prompt_path, original_prompt)
            print(Fore.GREEN + "Saved" + Fore.RESET)
            return original_prompt
        except:
            print(Fore.GREEN + "There was an error... (Check console logs)" + Fore.RESET)
            return "There was an error... (Check console logs)"
    
    def update_model(new_model):
        global model
        model = new_model
        try:
            env_file_path = find_dotenv("settings.env")
            env_values = dotenv_values(env_file_path)
            env_values['MODEL'] = new_model
            for key, value in env_values.items():
                set_key(env_file_path, key, value)
            print(Fore.GREEN + "Updated Model!" + Fore.RESET)
            return "Updated Model!"
        except:
            print(Fore.GREEN + "There was an error saving the data" + Fore.RESET)
            return "There was an error saving the data"    
        
    def load_model():
        global model
        try:
            model = UI.get_env_variable("MODEL", "settings.env")
            return model
        except:
            return "Error"
        
    def load_prompt():
        global prompt
        if os.path.isfile(os.path.join(local_folder, "prompt.txt")):
            prompt = CustomFileSystem.read_text_from_file(os.path.join(local_folder, "prompt.txt"))
            return prompt

    def prompt_test():
        print(Fore.YELLOW + "Current loaded prompt =\n" + Fore.RESET + read_prompt_file())

    def model_test():
        global model
        print(Fore.YELLOW + "Current model = " + Fore.RESET + model)

    def save_output_file(text, to_fix):
        save_path = local_folder + "Errors/output-" + to_fix
        return CustomFileSystem.save_text_to_file(save_path, text)

    def delete_translated_folder(): 
        CustomFileSystem.remove_folder(os.path.join(local_folder, "Translated"))
        print(Fore.GREEN + "Deleted 'Translated' folder" + Fore.RESET)
        return "Deleted 'Translated' folder"

    def delete_unpack_folder():
        CustomFileSystem.remove_folder(os.path.join(local_folder, "Unpack"))
        print(Fore.GREEN + "Deleted 'Unpack' folder" + Fore.RESET)
        return "Deleted 'Unpack' folder"

    def delete_errors_folder():
        CustomFileSystem.remove_folder(os.path.join(local_folder, "Errors"))
        print(Fore.GREEN + "Deleted 'Errors' folder" + Fore.RESET)
        return "Deleted 'Errors' folder"

    def unpack_pak(game_path, gust_pak_path):
        gust_pak_path = gust_pak_path.replace("\\", "/")
        game_path = game_path.replace("\\", "/")
        try:
            pak_path = game_path + "/Data/PACK01.PAK"
            print(pak_path)
            CustomFileSystem.copy_file(pak_path, os.path.join(local_folder, "Unpack", "PACK01.PAK"))
            subprocess.run([gust_pak_path + "/gust_pak.exe", os.path.join(local_folder, "Unpack", "PACK01.PAK")], cwd=local_folder)
            print(Fore.GREEN + "Done" + Fore.RESET)
            return "Done"
        except:
            print(Fore.RED + "There was an error..." + Fore.RESET)
            return "There was an error..."
        
    def repack_game(gust_tools_path):
        gust_tools_path = gust_tools_path.replace("\\", "/")
        try: 
            event_folder = os.path.join(local_folder, "Unpack", "event", "event_en")
            translated_folder = os.path.join(local_folder, "Translated")
            gust_pak = os.path.join(gust_tools_path, "gust_pak.exe") 
            pack_json = os.path.join(local_folder, "Unpack", "PACK01.json")
            for subfolder in CustomFileSystem.get_subfolder_paths(event_folder):
                for file in CustomFileSystem.get_files_in_folder(subfolder):
                    return "Found files on Unpack folder, please make sure you finished translating the game and you used fixer to fix the possible errors that were left..."
            for subfolder in CustomFileSystem.get_subfolder_paths(event_folder):
                CustomFileSystem.remove_folder(subfolder)
            for translated_subfolder in CustomFileSystem.get_subfolder_paths(translated_folder):
                CustomFileSystem.copy_folder(translated_subfolder, event_folder)
            subprocess.run([gust_pak, pack_json]) 
            CustomFileSystem.move_file(os.path.join(local_folder, "Unpack", "PACK01.pak"), os.path.join(local_folder, "Output", "PACK01.PAK"))
            print(Fore.GREEN + "The new .pak has been created (Go to the Output folder, and inside you will find the new PACK01.PAK)" + Fore.RESET)
            return "The new .pak has been created (Go to the Output folder, and inside you will find the new PACK01.PAK)"
        except:
            print(Fore.RED + "There was an error" + Fore.RESET)
            return "There was an error"
            

    def save_settings(OPENAI_API_KEY, GUST_TOOLS_PATH, GAME_PATH, CUSTOMDUMPER):   
        GAME_PATH = GAME_PATH.replace("\\", "/")
        GUST_TOOLS_PATH = GUST_TOOLS_PATH.replace("\\", "/")
        try:
            env_file_path = find_dotenv("settings.env")

            env_values = dotenv_values(env_file_path)

            env_values['OPENAI_API_KEY'] = OPENAI_API_KEY
            env_values['GUST_TOOLS_PATH'] = GUST_TOOLS_PATH
            env_values['GAME_PATH'] = GAME_PATH
            if CUSTOMDUMPER:
                env_values['CUSTOMDUMPER'] = "True"
            else:
                env_values['CUSTOMDUMPER'] = "False"
    
            for key, value in env_values.items():
                set_key(env_file_path, key, value)

            return "Updated Settings!"
        except:
            return "There was an error saving the data"
    
    def find_path():
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        folder_path = filedialog.askdirectory(parent=root)

        if folder_path:
            folder_path = folder_path.replace("\\", "/")
            return folder_path
        else:
            return "No folder selected"

    def find_file():
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        file_path = filedialog.askopenfilename()

        if file_path:
            file_path = file_path.replace("\\", "/")
            return file_path
        else:
            return "No file selected"
        
    def get_env_variable(variable_name, file_path=".env"):
        try:
            env_values = dotenv_values(file_path)
            return env_values.get(variable_name)
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            return None
    
    def gust_tools_create_mod_folder(gust_tools_path):
        gust_tools_path = gust_tools_path.replace("\\", "/")
        path = local_folder + "Translated"
        gust_ebm = gust_tools_path + "/gust_ebm.exe"
        sub_folders = CustomFileSystem.get_subfolder_paths(path)
        try:
            for folder in sub_folders:
                print(Fore.YELLOW + folder + Fore.RESET)
                ebm_folder = CustomFileSystem.get_files_with_extension(folder, ".ebm")
                for file in ebm_folder:
                    print(Fore.GREEN + file + Fore.RESET)
                    subprocess.run([gust_ebm, file])
                json_files = CustomFileSystem.get_files_with_extension(folder, ".json")
                CustomFileSystem.create_folder(folder + "/JSON")
                for json_file in json_files:
                    CustomFileSystem.move_file(json_file, folder + "/JSON/" + os.path.basename(json_file))
                need_extraction = CustomFileSystem.get_files_with_extension(folder + "/JSON", ".json")
                ebm_name = (need_extraction[0]).split("_")[2]
                CustomFileSystem.create_folder(local_folder + "Output/MOD/" + ebm_name)
                for cute_json in need_extraction:
                    with open(cute_json, "r", encoding="utf-8") as file:
                        file_contents = file.read()
                    replaced_json = re.sub(r'0x([0-9a-fA-F]+)', replace_hex_values, file_contents)
                    decoded_json = json.loads(replaced_json)
                    msg_strings = [message['msg_string'] for message in decoded_json['messages']]
                    with open(os.path.splitext(local_folder + "Output/MOD/" + ebm_name + "/" + os.path.basename(cute_json))[0] + ".txt", 'w', encoding="utf-8") as output_file:
                        for msg_string in msg_strings:
                            output_file.write(msg_string + '\n')

            for folder in sub_folders:
                for folder2 in CustomFileSystem.get_subfolder_paths(folder):
                    CustomFileSystem.remove_folder(folder2)
            print(Fore.GREEN + "Done creating MOD folder, check Output folder" + Fore.RESET)
            return "Done creating MOD folder, check Output folder"
        except:
            print(Fore.RED + "Something went wrong" + Fore.RESET)
            return "Something went wrong"
        
    
    def custom_dumper_create_mod_folder(gust_tools_path):
        gust_tools_path = gust_tools_path.replace("\\", "/")
        a24_ebm = local_folder + "Custom Dumper/Dumper.exe"
        path = local_folder + "Translated"
        try:
            for folder in CustomFileSystem.get_subfolder_paths(path):
                ebm_folder_key = CustomFileSystem.get_last_folder_name(folder)
                for ebm in CustomFileSystem.get_files_with_extension(folder, ".ebm"):
                    subprocess.run([a24_ebm, "--extract-strings", ebm], cwd=local_folder)
                    CustomFileSystem.move_file(local_folder + "extracted-strings.txt", local_folder + "Output/MOD/" + ebm_folder_key + "/" + os.path.splitext(os.path.basename(ebm))[0] + ".txt")
                    print(Fore.GREEN + "Done: " + ebm + Fore.RESET)
            print(Fore.GREEN + "Done creating MOD folder, check Output folder" + Fore.RESET)
            return "Done creating MOD folder, check Output folder" 
        except:
            print(Fore.RED + "Something went wrong" + Fore.RESET)
            return "Something went wrong"
    
    def fix_mod(fix):
        try:
            replacement_rules = [rule.strip().split('=') for rule in fix.split(',') if '=' in rule]
            
            sub_folders = CustomFileSystem.get_subfolder_paths(local_folder + "Output/MOD/")

            for folder in sub_folders:
                files = CustomFileSystem.get_files_with_extension(folder, ".txt")
                for file in files:
                    print("Starting: " + file)
                    with open(file, 'r', encoding='utf-8') as file_name:
                        content = file_name.read()
                    
                    for old_char, new_char in replacement_rules:
                        content = content.replace(old_char, new_char)

                    print("Finished: " + file)
                    with open(file, 'w', encoding='utf-8') as file_name:
                        file_name.write(content)
            print(Fore.GREEN + "Done fixing mod folder" + Fore.RESET)
            return "Done fixing mod folder"
        except:
            print(Fore.RED + "There was an error" + Fore.RESET)
            return "There was an error"
