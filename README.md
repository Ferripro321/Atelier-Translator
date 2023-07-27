# Atelier Translator
A simple tool that uses AI to translate Atelier games into any language

# How to use Atelier Translator:
1. Open or create a file called settings.env and place the following code:
   
   ```Dotenv
    OPENAI_API_KEY=YOUR-OPENAI-KEY-HERE # replace YOUR-OPENAI-KEY-HERE with the key you can find in https://platform.openai.com/account/api-keys (make sure you still have the free balance or create a new account to get free 5$ -> https://platform.openai.com/account/usage)
    GUST_EBM_PATH=PATH-TO-GUST-EBM # Replace PATH-TO-GUST-EBM with the path of your gust ebm. Example: C:/Users/Ferra/Desktop/gust_tools/gust_ebm.exe (Download it here: https://github.com/VitaSmith/gust_tools/releases)
    EVENT_FOLDER=YOUR-UNPACKED-GAME-EVENT-PATH # Replace YOUR-UNPACKED-GAME-EVENT-PATH with the event_en / any event_ folder found on the unpacked game files (guide will be included in next steps) Example: C:/Users/Ferra/Desktop/Sophie 2 unpack/event/event_en
    CUSTOMDUMPER=True/False # Replace True/False with True if you wanna use the tool for Ryza 3 or a more recent game, False for older games than Ryza 3
    DEBUGER=False # Put True if you know what you are doing, but you probably wanna keep this at False.
   ```
2. Scroll down on this file and in promp change Spanish to the language you wanna translate to.
3. Go to your game files, go to data folder of the game, copy "PACK01.PAK" and paste it on a new folder that you can create on your desktop.
4. Drag the PACK01.PAK that you have on the folder you created to gust_pak.exe -> [Download it here](https://github.com/VitaSmith/gust_tools/releases)
5. Now you will see some folders and files, go to event, then event_en (This is the folder path you have to put on YOUR-UNPACKED-GAME-EVENT-PATH)
6. Open the Microsoft store
7. Search "Python 3.11" and install it
8. Now open cmd (windows key + R and type cmd, then click enter)
9. Put the following commands one by one on the cmd (only needed the first time):
    
   ```
    pip install openai
    pip install pyperclip
    pip install colorama
    pip install python-dotenv
   ```
10. Now enter this command replace <PATH_WHERE_YOU_HAVE_ATELIER_TRANSLATOR> with the path to the atelier translator folder, example: C:/Users/Ferra/Desktop/Atelier Translator:
   
   ```
    cd "<PATH_WHERE_YOU_HAVE_ATELIER_TRANSLATOR>"
   ```
11. Now run the program by entering this command:
    
   ```
    python "Atelier Translator.py"
   ```
12. Enjoy

# How to use the Manual Fixer:
Warning: Only use this tool to fix errors!

1. Chose what version you wanna use, Custom Dumper or Gust tools (Custom Dumper is for Ryza 3 or +) (Gust tools is for Sophie 2 or -)
3. Manually fix output.txt (Check ExtractedStrings.txt to check original file strings)
   - TIP: Both files must have the same lines, this is usually the problem. Make sure Chat GPT didn't jump lines by accident on output.txt
4. Change file_to_fix to the name of the json you wanna fix
5. Change file_to_fix_folder to the name of the folder where the json you wanna fix is
6. Run the program and it will fix the file
