# This is the main file of the app, and should be the one you open to use the app. The ui and some functions are stored here

import gradio as gr
import webbrowser

from functions import *
from fixer import *

def translation_start(gust_tools_path, is_a24, openai_apikey):
    prompt = UI.get_prompt(UI)
    model = UI.get_model(UI)

    openai.api_key = openai_apikey
    custom_ebm_translation_handler(prompt, model) if is_a24 else gust_tools_translator_handler(gust_tools_path, prompt, model)
    return "ok"

def refresh_errors():
    files_to_fix = []
    for file in CustomFileSystem.get_files_in_folder(local_folder + "/Errors"):
        if "extracted-strings-" in os.path.basename(file):
            print("Found extracted: " + CustomFileSystem.get_text_after_specific_text(file, "extracted-strings-"))
            files_to_fix.append(CustomFileSystem.get_text_after_specific_text(file, "extracted-strings-"))
        else:
            print("Found output: " + CustomFileSystem.get_text_after_specific_text(file, "output-"))
    return gr.Dropdown.update(choices=files_to_fix)

def fix_handler(fix_a24, to_fix, gust_tools_path):
        return custom_dumper_fixer(to_fix) if fix_a24 else gust_tools_fixer(to_fix, gust_tools_path)
        

def count_original_file_lines(text, fix_a24):
        if fix_a24:
            return gr.Markdown.update(value="Lines: " + str(CustomFileSystem.count_lines(text)))
        else:
            return gr.Markdown.update(value="Lines: " + str(CustomFileSystem.count_lines(text) - 1)) # all extracted files with gust tools have an extra blank line so this should help make the count work properly

def count_new_file_lines(text):
    return gr.Markdown.update(value="Lines: " + str(CustomFileSystem.count_lines(text)))

def mod_creator_handler(gust_tools_path, is_a24):
    return UI.custom_dumper_create_mod_folder(gust_tools_path) if is_a24 else UI.gust_tools_create_mod_folder(gust_tools_path)


with gr.Blocks(title="Atelier Translator") as ui:
    with gr.Tabs(): 
        with gr.Tab("Unpack"):
            gr.Label('Atelier Translator - Unpack', show_label=False)
            gr.Markdown("⚠️ Before doing anything please go to settings and put your gust tools path, game path, OpenAI key, and select if you are gonna use this tool for Ryza 3 ⚠️")
            gr.Markdown("First of all we are going to unpack the file PACK01.PAK from your game files, press the button to start the process:")
            btn3 = gr.Button("Start Unpack", variant="primary")
            unpack_status = gr.Textbox(show_label=False, interactive=False)
            pass
        with gr.Tab("Translator"):
            gr.Label('Atelier Translator', show_label=False)
            gr.Markdown("⚠️ If you haven't yet unpacked the game files please go to the unpack tab ⚠️")
            gr.Markdown("⚠️ Before you continue edit or create a new promp for translation, go to the settings tab to do that ⚠️")
            gr.Markdown("Now click the start translation button to start the translation, this can take a lot of hours if you have a trial account and you might not be able to fully translate a game in one day, for more info visit: https://platform.openai.com/docs/guides/rate-limits")
            btn4 = gr.Button("Start Translation", variant="primary")
            translation_status = gr.Textbox(show_label=False, interactive=False)
            gr.Markdown("⚠️ If something is not working correctly open task manager find python process and kill it, when you restart the app and click start translation it will continue from where it left it ⚠️")
            pass
        with gr.Tab("Fixer"):
            gr.Label('Atelier Translator - Fixer', show_label=False)
            gr.Markdown("First of all select what file you wanna fix (press the refresh button to refresh the list)")
            to_fix = gr.Dropdown(interactive=True)
            refresh = gr.Button("Refresh list", variant="primary")
            gr.Markdown("Now click on Start Manual Fix and make the ChatGPT file text have the same lines as original file, then click save file. (You can click count lines to check you corrected it fine)")
            Show_file_content = gr.Button("Start Manual Fix", variant="primary")
            with gr.Row():
                original_text_lines = gr.Markdown("Lines: ")
                new_text_lines = gr.Markdown("Lines: ")
            with gr.Row():
                original_text = gr.Textbox(label="Original file text:", lines=30, interactive=False)
                new_text = gr.Textbox(label="ChatGPT file text:", lines=30, interactive=True)
            count_textbox_lines = gr.Button("Count lines")
            save_file = gr.Button("Save File", variant="primary")
            save_status = gr.Textbox(show_label=False, interactive=False)
            gr.Markdown("Now if you fixed the text you are can click the Fix file button!")
            Start_fix = gr.Button("Fix file", variant="primary")
            fix_status = gr.Textbox(show_label=False, interactive=False)
            pass
        with gr.Tab("Repack"):
            gr.Label('Atelier Translator - Repack', show_label=False)
            gr.Markdown("Now that you translated the game and fixed all errors we can repack the files so that you can update your game!")
            btn8 = gr.Button("Start Repack", variant="primary")
            repack_status = gr.Textbox(show_label=False, interactive=False)
            pass
        with gr.Tab("Mod"):
            gr.Label('Atelier Translator - MOD creator', show_label=False)
            gr.Markdown("Welcome to the mod creator, this is the last step of the program! You can skip this if you don't wanna share your modded .pak file but if you do please use this instead of sharing the direct .PAK file")
            gr.Markdown("The folder that this tool will create can be installed to the game using: https://github.com/Ferripro321/Atelier-Language-Updater")
            Start_mod = gr.Button("Create MOD", variant="primary")
            mod_status = gr.Textbox(show_label=False, interactive=False)    
        with gr.Tab("Fix Mod Syntax"):
            gr.Label('Atelier Translator - MOD Syntax fixer', show_label=False)
            gr.Markdown("You created and tested your mod and you saw weird white boxes or missing words? You are at the right place, let's start!")
            gr.Markdown("The format you should use on the following text box is this one: á=a, í=i, ó=o, ú=u, Á=A, Í=I, Ï=I, ï=i, Ö=O, ö=o, Ó=O, Ú=U, ¿=, ¡=, ñ=ny")
            gr.Markdown("You can use this example to fix Spanish Mods^^")
            characters_to_fix = gr.Textbox(label="Characters to fix")
            mod_Start_fix = gr.Button("Start Fix", variant="primary")
            mod_fix_status = gr.Textbox(show_label=False, interactive=False)
        with gr.Tab("Settings"):
            gr.Label('Atelier Translator - Settings', show_label=False)
            gr.Markdown("First of all to use this tool you need to setup your OpenAI API key, gust tools path and game path")
            gr.Markdown("To get your game path go to steam, right click on the game, go to manage -> and click browse local files")
            game_path = gr.Textbox(label="Game Path")
            btn1 = gr.Button("Find Path")
            gr.Markdown("If you don't have gust tools installed please visit: https://github.com/VitaSmith/gust_tools/releases once you download the zip, extract it and put the path in the following textbox:")
            gust_tools_path = gr.Textbox(label="Gust tools Path")
            btn2 = gr.Button("Find Path")
            gr.Markdown("To get an OpenAI API Key visit: https://platform.openai.com/account/api-keys make sure you have credits on your account (When you create your acc you get free credits, but this will expire in few months so if they expired create a new account): https://platform.openai.com/account/usage")
            openai_apikey = gr.Textbox(label="OpenAI API key")
            gr.Markdown("Click the Atelier Ryza 3 check box if you are translating / creating a mod for that specific game")
            is_a24 = gr.Checkbox(label="Atelier Ryza 3")
            gr.Markdown("You may wanna edit this prompt to make Chat GPT translate to the language you want, current promp is ideal for Spanish. (Click save prompt after editing it)")
            gr.Markdown("⚠️ The largest the prompt is the more time and credits it will take ⚠️")
            new_prompt = gr.Textbox(label="Prompt",value=UI.get_prompt(UI), lines=15)
            btn5 = gr.Button("Save prompt", variant="primary")
            prompt_status = gr.Textbox(show_label=False, interactive=False)
            gr.Markdown("To make sure the promp has been changed/loaded correctly you can click the following button and check your console to see the prompt that has been returned")
            test_prompt = gr.Button("Test prompt")
            gr.Markdown("You can change the OpenAI Model here, but I wouldn't recommend to use gpt4 models due to price. More info on models here: https://platform.openai.com/docs/models")
            new_model = gr.Textbox(label="Model", value=UI.get_model(UI))
            btn6 = gr.Button("Save model", variant="primary")
            model_status = gr.Textbox(show_label=False, interactive=False)
            gr.Markdown("To make sure the model has been changed/loaded correctly you can click the following button and check your console to see the prompt that has been returned")
            test_model = gr.Button("Test model")
            gr.Markdown("If you want to save current app settings such as paths, api key,... -> Click on 'Save current settings', and then to reload them click on 'Load past settings'")
            gr.Markdown("⚠️ Model and Prompt won't be saved using this button, please click on their buttons for saving ⚠️")
            with gr.Row():
                Bsave_settings = gr.Button("Save current settings", variant="primary")
                Breload_settings = gr.Button("Load past settings", variant="primary")
            settings_status = gr.Textbox(show_label=False, interactive=False)
            gr.Markdown("⚠️ Proceed with caution, the following buttons are only intended to start from 0, only use them if you wanna start from 0 or you already have backup of everything and you wanna start the translation for a new game ⚠️")
            delete_translated = gr.Button("Delete Translated Folder (THIS WILL REMOVE THE FOLDER THAT CONTAINS THE TRANSLATED GAME FILES)", variant="stop")
            delete_errors = gr.Button("Delete Errors (THIS WILL REMOVE THE DETECTED ERRORS THAT CHAT GPT MADE, WITHOUT FIXING THIS ERRORS MANUALLY YOU CAN'T REPACK THE GAME)", variant="stop")
            delete_unpack = gr.Button("Delete Unpack (THIS WILL REMOVE THE FOLDER THAT CONTAINS THE ORIGINAL TEXTS OF THE GAME)", variant="stop")
            delete_status = gr.Textbox(show_label=False, interactive=False)
            pass
        with gr.Tab("Credits"):
            gr.Label('Atelier Translator - Credits', show_label=False)
            gr.Markdown("Thanks to azusagawa.it for the EBM extractor for a24 (Ryza 3) -> https://github.com/Azusagawa-it/a24_ebm")
            gr.Markdown("Thanks to MisterGunXD for helping with bugs, styling, and creating the python Encoder/Decoder for json files that gust_ebm creates -> https://github.com/MisterGunXD")
            gr.Markdown("Thanks to VitaSmith for creating Gust Tools -> https://github.com/VitaSmith/gust_tools")
            gr.Markdown("Thanks to myself (Ferripro321) for everything else (; -> https://github.com/Ferripro321")
            gr.Markdown("If you find any bug or you need help you can dm me on discord (ferripro) or send me an email at ferripro@proton.me")
            pass
    
    btn1.click(UI.find_path, outputs=game_path)
    btn2.click(UI.find_path, outputs=gust_tools_path)
    btn3.click(UI.unpack_pak, inputs=[game_path, gust_tools_path], outputs=unpack_status)
    btn4.click(lambda: "Translation Started, from now on check terminal for logs", outputs=translation_status)
    btn4.click(translation_start, inputs=[gust_tools_path, is_a24, openai_apikey])
    btn5.click(UI.update_prompt.__get__(UI), inputs=new_prompt, outputs=prompt_status)
    btn6.click(UI.update_model.__get__(UI), inputs=new_model, outputs=model_status)
    btn8.click(UI.repack_game, inputs=[gust_tools_path], outputs=repack_status)


    test_prompt.click(UI.prompt_test.__get__(UI))
    test_model.click(UI.model_test.__get__(UI))
    refresh.click(refresh_errors, outputs=to_fix)
    Show_file_content.click(UI.load_original_file, inputs=to_fix, outputs=original_text)
    Show_file_content.click(UI.load_file_to_edit, inputs=to_fix, outputs=new_text)
    count_textbox_lines.click(count_original_file_lines, inputs=[original_text, is_a24], outputs=original_text_lines)
    count_textbox_lines.click(count_new_file_lines, inputs=new_text, outputs=new_text_lines)
    save_file.click(UI.save_output_file, inputs=[new_text, to_fix], outputs=save_status)
    Start_fix.click(fix_handler, inputs=[is_a24, to_fix, gust_tools_path], outputs=fix_status)
    Start_mod.click(mod_creator_handler, inputs=[gust_tools_path, is_a24], outputs=mod_status)
    Bsave_settings.click(UI.save_settings, inputs=[openai_apikey, gust_tools_path, game_path, is_a24], outputs=settings_status)
    mod_Start_fix.click(UI.fix_mod, inputs=characters_to_fix, outputs=mod_fix_status)

    delete_translated.click(UI.delete_translated_folder, outputs=delete_status)
    delete_errors.click(UI.delete_errors_folder, outputs=delete_status)
    delete_unpack.click(UI.delete_unpack_folder, outputs=delete_status)

    # This is retarded but I have no idea how to do it in a different way
    Breload_settings.click(lambda: UI.get_env_variable("OPENAI_API_KEY", "settings.env"), outputs=openai_apikey)
    Breload_settings.click(lambda: UI.get_env_variable("GAME_PATH", "settings.env"), outputs=game_path)
    Breload_settings.click(lambda: UI.get_env_variable("GUST_TOOLS_PATH", "settings.env"), outputs=gust_tools_path)
    Breload_settings.click(lambda: UI.get_env_variable("CUSTOMDUMPER", "settings.env") == "True", outputs=is_a24)
    Breload_settings.click(UI.load_model.__get__(UI), outputs=new_model)
    Breload_settings.click(UI.load_prompt.__get__(UI), outputs=new_prompt)
    Breload_settings.click(lambda: "Done Loading Settings!", outputs=settings_status)


if not os.path.exists(local_folder + "settings.env"):
    with open(local_folder + "settings.env", 'w') as f:
        f.write("")
    print(f"'{local_folder + 'settings.env'}' created!")

webbrowser.open('http://127.0.0.1:7860')
ui.launch()
