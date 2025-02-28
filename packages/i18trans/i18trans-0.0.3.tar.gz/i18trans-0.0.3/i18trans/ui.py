import tkinter as tk
from tkinter import filedialog
from tkinter.constants import W
import json,os,codecs,time
import threading
from . import config
from googletrans import Translator

root = tk.Tk() 
root.title(config.APP_NAME)
root.geometry(config.APP_SIZE) 
root.configure(background=config.APP_BG_COLOR)

tab_menu_var = tk.StringVar()
tab_menu_var.set("2 Tab Space") 


def upload_json():
    """Opens a file dialog, reads a JSON file, and uploads it."""
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not file_path:
        return  # User cancelled the dialog

    try:
        with open(file_path, 'r') as f:
            data = json.load(f) 
            beautified_json = json.dumps(data, indent=2)
            input_box.delete('1.0', tk.END) 
            input_box.insert(tk.END, beautified_json)


    except FileNotFoundError:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "File not found.\n")
    except json.JSONDecodeError as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "Invalid JSON file.\n" +str(e))
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"An unexpected error occurred: {e}\n")          

def validate_json():
    """Validates the JSON content from the text area."""
    json_text = input_box.get("1.0", tk.END).strip()

    if not json_text:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END,"Error: Please enter JSON data.")
        return

    try:
        json.loads(json_text)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END,"Success: Valid JSON!")
    except json.JSONDecodeError as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Error: Invalid JSON:\n{e}")

def format_json():
    """Beautifies the JSON content in the text area."""
    json_text = input_box.get("1.0", tk.END)

    if not json_text:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END,"Error: Please enter JSON data.")
        return

    try:
        if tab_menu_var:
            if tab_menu_var.get() =="4 Tab Space":
                tab = 4
            elif tab_menu_var.get() =="3 Tab Space":
                tab = 3
            else:
                tab = 2     
        else:
            tab = 2     
        parsed_json = json.loads(json_text)
        beautified_json = json.dumps(parsed_json, indent=tab)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, beautified_json)

    except json.JSONDecodeError as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Error: Invalid JSON:\n{e}")

def minify_json():
    json_text = input_box.get("1.0", tk.END)

    if not json_text:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END,"Error: Please enter JSON data.")
        return

    try:
        parsed_json = json.loads(json_text)
        minified_json = json.dumps(parsed_json, separators=(',', ':'))  # Minify by removing whitespace
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, minified_json)

    except json.JSONDecodeError as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Error: Invalid JSON:\n{e}")

def get_selected_language_list(event):
    selected_libery = language_list.curselection()
    object_format = {}
    for i in selected_libery:
        object_format[language_list.get(i)] = config.LANGUAGE[language_list.get(i)]   
    selected_items_list_Format = json.dumps(object_format, indent=4)
    output_box.delete('1.0', tk.END)
    output_box.insert(tk.END, str(selected_items_list_Format))

def folderName(text):
    if "-" in text:
      return f"{text.split("-", 1)[0]}_{text.split("-", 1)[1].upper()}"
    else:
       return text
    
def massage_box(text):
    old_text = output_box.get("1.0", tk.END)
    new_text = old_text + text
    output_box.insert(tk.END, new_text)
    output_box.see(tk.END)

def create_or_select_folder():
    """
    Prompts the user to either create a new folder in the Downloads directory
    or select an existing folder using a file dialog.
    """

    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

    choice = tk.messagebox.askyesno(
        "Create or Select Folder",
        "Do you want to Save json file a _locales folder in Downloads? (Yes to create, No to select)"
    )

    if choice:  # Create new folder
        new_folder_name = "_locales"
        if new_folder_name:
            new_folder_path = os.path.join(downloads_path, new_folder_name)
            try:
                os.makedirs(new_folder_path, exist_ok=True)  # Create the folder
                return new_folder_path
            except Exception as e:
                massage_box(f"Error: Failed to create folder: {e}")
                return None
        else:
            return None #User cancelled folder creation.

    else:  # Select existing folder
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            return folder_selected
        else:
            return None #User cancelled folder selection.

def translate_run():
    output_box.delete("1.0", tk.END)
    massage_box("Please wait...")
    translate_json()     

def openFolder(name):
    if not os.path.exists(name):
        massage_box("Error: Extension Folder Not Exist! "+name)
    else:
        path = os.path.realpath(name)
        os.startfile(path)  

def translate_json():
    """Translates the JSON content in the text area."""
    json_text = input_box.get("1.0", tk.END).strip()

    selected_indices = language_list.curselection()
    selected_languages = [config.LANGUAGE[language_list.get(index)] for index in selected_indices]

    print(selected_languages)

    if not json_text:
        massage_box("Error: Please enter JSON data.")
        return
    
    if not selected_languages:
        massage_box(f"Error: Please select at least one target language.")
        return
    
    def translation_thread():
        try:
            parsed_json = json.loads(json_text)
            save_path = create_or_select_folder()

            if not save_path:
                massage_box( f"Error: folder not found")
                return


            for lang in selected_languages:
                translated_json = translate_recursive(parsed_json, lang)
                folder_name = folderName(lang)
                print(lang)
                print(translated_json)
                beautified_json = json.dumps(translated_json, ensure_ascii=False, indent=4)
                massage_box(beautified_json)
                time.sleep(1)

                folder_path = save_path+"/"+ folder_name

                file_path = os.path.join(folder_path, 'messages.json')

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    massage_box( "[*] DONE: "+folder_path+" does not exist. Create "+folder_path)

                with open(file_path, 'wb') as f:
                    json.dump(translated_json, codecs.getwriter('utf-8')(f), ensure_ascii=False, indent=4)
                    massage_box("Save Json")

            openFolder(save_path)   

        except json.JSONDecodeError as e:
            massage_box(f"Error: Invalid JSON:\n{e}")   
        except Exception as e:
            massage_box(f"Error: Translation or save error: {e}")

    threading.Thread(target=translation_thread).start() 



def translate_recursive(data, target_language):
    """Recursively translates the values in a JSON object or array."""
    translator = Translator()

    if isinstance(data, dict):
        translated_data = {}
        for key, value in data.items():
            translated_data[key] = translate_recursive(value, target_language)
        return translated_data

    elif isinstance(data, list):
        translated_data = [translate_recursive(item, target_language) for item in data]
        return translated_data

    elif isinstance(data, str):
        try:
            translation = translator.translate(data, dest=target_language)
            return translation.text
        except Exception as e:
            massage_box(f"Translation error: {e}")
            return data
    else:
        return data



input_label = tk.Label(root, text = 'INPUT JSON', bg='#2c3e50', fg='#ffffff', font=('calibre',10, 'bold'), width=config.LABEL_WIDTH, height=config.LABEL_HIGHT)
input_label.grid(row=0, column=0, sticky = W, padx=10, pady=(10, 0))

output_label = tk.Label(root, text = 'OUTPUT JSON', bg='#2c3e50', fg='#ffffff', font=('calibre',10, 'bold'), width=config.LABEL_WIDTH, height=config.LABEL_HIGHT)
output_label.grid(row=0, column=3, sticky = W, padx=10, pady=(10, 0))

input_box = tk.Text(root, font=('calibre',10, 'bold'), fg="#1a1a1a", height=config.BOX_HIGHT, width=config.BOX_WIDTH)
input_box.grid(row=1, column=0, rowspan=10, sticky = W, padx=10, pady=0)

output_box = tk.Text(root, font=('calibre',10, 'bold'), fg="#1a1a1a", height=config.BOX_HIGHT, width=config.BOX_WIDTH)
output_box.grid(row=1, column=3, rowspan=10, sticky = W, padx=10, pady=0)

upload_button = tk.Button(root, 
                    text = "Upload Data", 
                    fg = "white",
                    bg = config.APP_BG_COLOR,
                    bd =  1, 
                    font=('calibre', 12,'bold'), 
                    width=config.BUTTON_WIDTH, 
                    height=2, command=upload_json)
upload_button.grid(row=0, column=2,rowspan=2,  padx=0, pady=(10, 0))

validate_button = tk.Button(root, 
                    text = "Validate", 
                    fg = "white",
                    bg = config.APP_BG_COLOR,
                    bd =  1, 
                    font=('calibre', 12,'bold'), 
                    width=config.BUTTON_WIDTH, 
                    height=2, command=validate_json)
validate_button.grid(row=1, column=2,rowspan=2,  padx=0, pady=(10, 0))


tab_menu = tk.OptionMenu(root, tab_menu_var,*config.TAB_LIST)
tab_menu.config(width=config.MENU_WIDTH)
tab_menu.grid(row=2, column=2,rowspan=2,  padx=0, pady=(10, 0))

format_button = tk.Button(root, 
                    text = "Format / Beautify", 
                    fg = "white",
                    bg = config.APP_BG_COLOR,
                    bd =  1, 
                    font=('calibre', 12,'bold'), 
                    width=config.BUTTON_WIDTH, 
                    height=2,command=format_json)
format_button.grid(row=3, column=2,rowspan=2,  padx=0, pady=(10, 0))

minify_button = tk.Button(root, 
                    text = "Minify / Compact", 
                    fg = "white",
                    bg = config.APP_BG_COLOR,
                    bd =  1, 
                    font=('calibre', 12,'bold'), 
                    width=config.BUTTON_WIDTH, 
                    height=2,command=minify_json)
minify_button.grid(row=4, column=2,rowspan=2,  padx=0, pady=(10, 0))

LANGUAGE_KEY = []
for key in config.LANGUAGE.keys():
       LANGUAGE_KEY.append(key) 


language_list = tk.Listbox(root, selectmode=tk.MULTIPLE, width=config.LIST_WIDTH,height=config.LIST_HIGHT, font=('calibre',10,'normal'), exportselection=False)
language_list.grid(row=5, column=2,rowspan=5,  padx=0, pady=(10, 0))

for lang in LANGUAGE_KEY:
    language_list.insert(tk.END, lang)

language_list.bind("<<ListboxSelect>>", get_selected_language_list) 

# horizontal
scrollbar = tk.Scrollbar(root, orient="horizontal")
scrollbar.config(command=language_list.yview)
scrollbar.grid(row=8, column=2,rowspan=2, padx=0, pady=(50, 0)) 

translate_button = tk.Button(root, 
                    text = "Translate", 
                    fg = "white",
                    bg = config.APP_BG_COLOR,
                    bd =  1, 
                    font=('calibre', 12,'bold'), 
                    width=config.BUTTON_WIDTH, 
                    height=2, command=translate_run)
translate_button.grid(row=9, column=2,rowspan=2,  padx=0, pady=(10, 0))






