# This file stores functions used on Atelier Transaltor.

import json
import re
import openai
import subprocess
import shutil
import time
import os
import pyperclip
import colorama
from colorama import Fore, Style
colorama.init()
from dotenv import load_dotenv


def start():
    text1 = """
 ________  _________        ___      ___  _____     
|\   __  \|\___   ___\     |\  \    /  /|/ __  \    
\ \  \|\  \|___ \  \_|     \ \  \  /  / /\/_|\  \   
 \ \   __  \   \ \  \       \ \  \/  / /\|/ \ \  \  
  \ \  \ \  \   \ \  \       \ \    / /      \ \  \ 
   \ \__\ \__\   \ \__\       \ \__/ /        \ \__|
    \|__|\|__|    \|__|        \|__|/          \|__|

"""
    text2 = """
--------------------------------------------
By Ferripro & MisterGunXD
--------------------------------------------
"""
    print(Fore.RESET + text1)
    print(text2)
    #time.sleep(5)

def get_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            yield file_path

def get_files_with_extension(folder_path, extension):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(extension):
                file_path = os.path.join(root, file_name)
                yield file_path

def replace_hex_values(match):
    hex_value = match.group(1)
    return str(int(hex_value, 16))

def replace_decimal_values(match):
    decimal_value = match.group(1)
    return hex(int(decimal_value))

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

def count_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            line_count = sum(1 for _ in file)
            return line_count
    except FileNotFoundError:
        return 0
    except Exception as e:
        return "Something failed: " + str(e)

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

def request_translation(promp, translate, path):
    max_retries = 3
    retry_delay = 30 # in seconds (:

    retry_count = 0
    while retry_count < max_retries:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", # gpt-3.5-turbo-0613
                messages=[
                    {"role": "system", "content": promp},
                    {"role": "user", "content": translate}
                ])
            text = completion.choices[0].message["content"]
            text = text.replace("//", "\n")
            return text
        except:
            print(Fore.RED + "There was an error with the OpenAI API, retrying in 30 seconds" + Fore.RESET)
            time.sleep(retry_delay)
            print(Fore.YELLOW + "Retrying...")
            retry_count += 1

    if retry_count == max_retries:
        print(Fore.RED + "Maximum number of retries reached. Unable to complete the API call for: " + path + Fore.RESET)
        time.sleep(1.5)
        print(Fore.BLUE + "Exiting...")
        return "Error"