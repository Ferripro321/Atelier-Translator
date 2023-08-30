# This file contains the functions used by the fixer section of the UI. 
# This code can be dramatically improved but to save time I just adapted old fixer code to work with the web ui.

from functions import *
from translator import *

def gust_tools_fixer(file_to_fix, gust_tools):
    file_to_fix = file_to_fix[:-4]
    extracted_strings_path = local_folder + "Errors/extracted-strings-" + file_to_fix + ".txt"
    output_path = local_folder + "Errors/output-" + file_to_fix + ".txt"
    file_to_fix_folder = (file_to_fix).split("_")[2]
    ebm_folder = local_folder + "Unpack/event/event_en/" + file_to_fix_folder
    gust_ebm = gust_tools + "/gust_ebm.exe"

    print(CustomFileSystem.count_file_lines(output_path))
    print(CustomFileSystem.count_file_lines(extracted_strings_path))

    if CustomFileSystem.count_file_lines(output_path) == CustomFileSystem.count_file_lines(extracted_strings_path): 
        print("Seems OK")
        with open(output_path, "r", encoding="utf-8") as file:
                output = file.read()
        output = CustomFileSystem.remove_empty_lines(output)

        try:
            with open(ebm_folder + "/" + file_to_fix, "r", encoding="utf-8") as file:
                file_contents = file.read()
        except:
            CustomFileSystem.remove_file(output_path)
            CustomFileSystem.remove_file(extracted_strings_path)
            return "Seems like the error has been fixed already by a possible re-run of the translator, due to this the error file has been deleted." 

        replaced_json = re.sub(r'0x([0-9a-fA-F]+)', replace_hex_values, file_contents)
        decoded_json = json.loads(replaced_json)
        for i, linea in enumerate(output):
                    decoded_json['messages'][i]['msg_string'] = linea.strip()
        MATCH_ALL_XYZ = r'(?<![a-zA-Z\"])(?![\"])(\b\d+)'

        with open(ebm_folder + "/" + file_to_fix, "w", encoding="utf-8") as file:
            file.write(re.sub(MATCH_ALL_XYZ, replace_decimal_values, json.dumps(decoded_json, ensure_ascii=False)))

        CustomFileSystem.move_file(ebm_folder + "/" + file_to_fix, local_folder + "Translated/" + file_to_fix_folder + "/" + file_to_fix)
        subprocess.run([gust_ebm, local_folder + "Translated/" + file_to_fix_folder + "/" + file_to_fix])
        print("New EBM created")
        CustomFileSystem.remove_file(local_folder + "Translated/" + file_to_fix_folder + "/" + file_to_fix)
        CustomFileSystem.remove_file(output_path)
        CustomFileSystem.remove_file(extracted_strings_path)
        return "Done fixing: " + file_to_fix
    else: 
        return "File " + file_to_fix + " isn't fixed"

def custom_dumper_fixer(file_to_fix):
    file_to_fix_folder = (file_to_fix).split("_")[2]
    file_to_fix = file_to_fix.replace(".txt", ".ebm") # Doing this so I don't have to change how the old standalone fixer used to work.
    a24_ebm = local_folder + "Custom Dumper/Dumper.exe"

    extracted_strings_path = local_folder + "Errors/extracted-strings-" + os.path.splitext(os.path.basename(file_to_fix))[0] + ".txt"
    output_path = local_folder + "Errors/output-" + os.path.splitext(os.path.basename(file_to_fix))[0] + ".txt"
    ebm_folder = local_folder + "Unpack/event/event_en/" + file_to_fix_folder

    print(CustomFileSystem.count_file_lines(output_path))
    print(CustomFileSystem.count_file_lines(extracted_strings_path))

    if CustomFileSystem.count_file_lines(output_path) == CustomFileSystem.count_file_lines(extracted_strings_path): 
        print("Seems OK")
        if os.path.isfile(ebm_folder + "/" + file_to_fix):
            subprocess.run([a24_ebm, "--replace-strings", ebm_folder + "/" + file_to_fix, output_path], cwd=local_folder)
            print("New EBM created")
            CustomFileSystem.move_file(local_folder + "modified.ebm", local_folder + "Translated/" + file_to_fix_folder + "/modified.ebm")
            CustomFileSystem.rename_file(local_folder + "Translated/" + file_to_fix_folder + "/modified.ebm", local_folder + "Translated/" + file_to_fix_folder + "/" + file_to_fix)
            CustomFileSystem.remove_file(ebm_folder + "/" + file_to_fix)
            CustomFileSystem.remove_file(extracted_strings_path)
            CustomFileSystem.remove_file(output_path)
            return "Done fixing: " + file_to_fix
        else:
            CustomFileSystem.remove_file(extracted_strings_path)
            CustomFileSystem.remove_file(output_path)
            return "Seems like the error has been fixed already by a possible re-run of the translator, due to this the error file has been deleted." 
    else: 
        return "File " + file_to_fix + " isn't fixed"
