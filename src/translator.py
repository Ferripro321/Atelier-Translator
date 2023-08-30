# This file stores the functions related to the translator

from functions import *

output_path = local_folder + "output.txt"

def request_translation(prompt, translate, path, gpt_model):
    max_retries = 3
    retry_delay = 30

    retry_count = 0
    while retry_count < max_retries:
        try:
            completion = openai.ChatCompletion.create(
                model=gpt_model,
                messages=[
                    {"role": "system", "content": prompt},
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


def gust_tools_translator_handler(gust_ebm, prompt, model):
    ebm_folders_num = 0
    current_ebm_folder_num = 0

    for ebm_folder in CustomFileSystem.get_subfolder_paths(local_folder + "Unpack/event/event_en"):
        ebm_folders_num += 1
    for ebm_folder in CustomFileSystem.get_subfolder_paths(local_folder + "Unpack/event/event_en"):
        ebm_folder_key = CustomFileSystem.get_last_folder_name(ebm_folder)
        current_ebm_folder_num += 1
        print(Fore.GREEN + "Starting Folder " + ebm_folder_key + " -> " + str(current_ebm_folder_num) + " / " + str(ebm_folders_num) + Fore.RESET)
        for file_path in CustomFileSystem.get_files_with_extension(ebm_folder, ".ebm"):
            subprocess.run([gust_ebm + "/gust_ebm.exe", file_path])
            CustomFileSystem.remove_file(file_path)
        for json_file in CustomFileSystem.get_files_with_extension(ebm_folder, ".json"):
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

            output = request_translation(prompt, extracted_strings, json_file, model)
            if output == "Error":
                exit()
            print(Fore.GREEN + "Finished Translating" + Fore.RESET)

            output = CustomFileSystem.remove_empty_lines(output)

            Failed = False

            with open(output_path, "w", encoding="utf-8") as file:
                file.write("\n".join(output))

            try:
                for i, linea in enumerate(output):
                    decoded_json['messages'][i]['msg_string'] = linea.strip()
            except:
                print(Fore.RED + "Chat GPT fucked up, you will manually need to fix this file later." + Fore.RESET)
                CustomFileSystem.move_file(local_folder + 'extracted-strings.txt', local_folder + "Errors/" + "extracted-strings-" + os.path.basename(json_file) + ".txt")
                CustomFileSystem.move_file(local_folder + 'output.txt', local_folder + "Errors/" + "output-" + os.path.basename(json_file) + ".txt")
                Failed = True
            
            if Failed:
                print("Skipping...")
            else:
                MATCH_ALL_XYZ = r'(?<![a-zA-Z\"])(?![\"])(\b\d+)'

                with open(json_file, "w", encoding="utf-8") as file:
                    file.write(re.sub(MATCH_ALL_XYZ, replace_decimal_values, json.dumps(decoded_json, ensure_ascii=False)))
    
                CustomFileSystem.move_file(json_file, local_folder + "Translated/" + ebm_folder_key + "/" + os.path.basename(json_file))
                subprocess.run([gust_ebm + "/gust_ebm.exe", local_folder + "Translated/" + ebm_folder_key + "/" + os.path.basename(json_file)])
                CustomFileSystem.remove_file(local_folder + "Translated/" + ebm_folder_key + "/" + os.path.basename(json_file))
                print(Fore.GREEN + "Finished: " + json_file + Fore.RESET)

def custom_ebm_translation_handler(prompt, model):
    ebm_folders_num = 0
    current_ebm_folder_num = 0
    a24_ebm = local_folder + "/Custom Dumper/Dumper.exe"
    for ebm_folder in CustomFileSystem.get_subfolder_paths(local_folder + "Unpack/event/event_en"):
            ebm_folders_num += 1
    for ebm_folder in CustomFileSystem.get_subfolder_paths(local_folder + "Unpack/event/event_en"):
        ebm_folder_key = CustomFileSystem.get_last_folder_name(ebm_folder)
        current_ebm_folder_num += 1
        print(Fore.GREEN + "Starting Folder " + ebm_folder_key + " -> " + str(current_ebm_folder_num) + " / " + str(ebm_folders_num) + Fore.RESET)
        for file_path in CustomFileSystem.get_files_with_extension(ebm_folder, ".ebm"):
            subprocess.run([a24_ebm, "--extract-strings", file_path], cwd=local_folder)
            with open(local_folder + "extracted-strings.txt", "r", encoding="utf-8") as file:
                extracted_strings = file.read()

            extracted_strings = extracted_strings.replace("\n", "//")
            extracted_strings = extracted_strings.replace("<CR>", " ")

            print(Fore.BLUE + "Starting Translation..." + Fore.RESET)
            output = request_translation(prompt, extracted_strings, file_path, model)
            if output == "Error":
                exit()
            print(Fore.GREEN + "Finished Translating" + Fore.RESET)

            output = CustomFileSystem.remove_empty_lines(output)

            with open(output_path, "w", encoding="utf-8") as file:
                file.write("\n".join(output))
    
            if CustomFileSystem.count_file_lines(local_folder + "output.txt") == CustomFileSystem.count_file_lines(local_folder + "extracted-strings.txt"):
                print("Seems OK")
                subprocess.run([a24_ebm, "--replace-strings", file_path, local_folder + "output.txt"], cwd=local_folder)
                print("New EBM created")
                CustomFileSystem.move_file(local_folder + "modified.ebm", local_folder + "Translated/" + ebm_folder_key + "/modified.ebm")
                CustomFileSystem.rename_file(local_folder + "Translated/" + ebm_folder_key + "/modified.ebm", local_folder + "Translated/" + ebm_folder_key + "/" + os.path.basename(file_path))
                CustomFileSystem.remove_file(file_path)
            else:
                print(Fore.RED + "Chat GPT fucked up, you will manually need to fix this file later." + Fore.RESET)
                CustomFileSystem.move_file(local_folder + 'extracted-strings.txt', local_folder + "Errors/" + "extracted-strings-" + os.path.splitext(os.path.basename(file_path))[0] + ".txt")
                CustomFileSystem.move_file(local_folder + 'output.txt', local_folder + "Errors/" + "output-" + os.path.splitext(os.path.basename(file_path))[0] + ".txt")