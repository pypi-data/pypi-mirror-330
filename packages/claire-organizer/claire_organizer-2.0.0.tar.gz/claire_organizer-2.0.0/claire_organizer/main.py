from os import listdir, makedirs, rename, walk, path, rmdir
import tkinter.filedialog
from ziz_utils import clear
import shutil, tkinter, ziz_utils, json

def rename_duplicate(file_path: str, folder_path: str) -> str:
    """
    Rename the files if there are any duplicate, else return the original file name

    :type folder_path: str
    :param folder_path: The path to the folder you want to sort.
    :type file_path: str
    :param folder_path: The path to the file we're checking.
    """
    base_name, extension = path.splitext(file_path)
    counter = 1
    new_file_path = path.join(folder_path, path.basename(file_path))
    
    while path.exists(new_file_path):
        new_file_path = path.join(folder_path, f"{base_name}({counter}){extension}")
        counter += 1
    
    return new_file_path


def file_sorter(folder_path: str, config: dict[str, list[str]]) -> None:
    """
    Sort the files of each folder into each category.

    :type folder_path: str
    :param folder_path: The path to the folder you want to sort.
    :type config: dict[str, list[str]]
    :param config: The config contains extension for each category.
    """

    subfolders = set(config.keys()) | {"Others"}
    for folder_name in subfolders:
        makedirs(path.join(folder_path, folder_name), exist_ok=True)

    for root, dirs, files in walk(folder_path, topdown=False):
        if dirs:
            for dir_name in dirs:
                dir_path = path.join(root, dir_name)
                for file_name in listdir(dir_path):
                    file_path = path.join(dir_path, file_name)
                    try:
                        if path.isfile(file_path):
                            new_file_path = rename_duplicate(file_path, folder_path)
                            shutil.move(file_path, new_file_path)
                    except Exception as e:
                        print(f"Error moving {file_name} from {dir_name} to root: {e}")

        if files:
            for file_name in files:
                file_path = path.join(root, file_name)
                file_ext = path.splitext(file_name)[1].lower()

                moved = False
                for folder_name, extensions in config.items():
                    if file_ext in extensions:
                        target_folder = path.join(folder_path, folder_name)
                        new_file_path = rename_duplicate(file_path, target_folder)
                        try:
                            shutil.move(file_path, new_file_path)
                            moved = True
                            break
                        except Exception as e:
                            print(f"Error moving {file_name} to {folder_name}: {e}")
                
                if not moved:
                    target_folder = path.join(folder_path, "Others")
                    new_file_path = rename_duplicate(file_path, target_folder)
                    try:
                        shutil.move(file_path, new_file_path)
                    except Exception as e:
                        print(f"Error moving {file_name} to Others: {e}")

    for i in listdir(folder_path):
        if not listdir(path.join(folder_path, i)):
            rmdir(path.join(folder_path, i))

def config_manager(def_config: dict, config_folder: str, config_file_name: str) -> None:
    """
    Check the config file to see if it's valid or not. Create new config folder if not exist, write new config file if config doesn't exist or corrupted.
    This is a modified version of the config_manager from ziz_utils remade to work with this program.

    :type def_config: dict
    :param def_config: The default config.
    :type config_folder: str
    :param config_folder: The path to the folder contains the config file.
    :type config_file_name: str
    :param config_file_name: The name of the config file.
    """
    if not isinstance(def_config, dict):
        raise TypeError(f"Parameter 'def_config' expect type dict, got {type(def_config).__name__} instead.")
    if not isinstance(config_folder, str):
        raise TypeError(f"Parameter 'config_path' expect type str, got {type(config_folder).__name__} instead.")
    if not isinstance(config_file_name, str):
        raise TypeError(f"Parameter 'config_file_name' expect type str, got {type(config_file_name).__name__} instead.")

    makedirs(config_folder, exist_ok=True)
    config_path = path.join(config_folder, config_file_name)

    if not path.exists(config_path):
        with open(config_path, "w") as temp:
            json.dump(def_config, temp, ensure_ascii=False, indent=4)
        return
    
    try:
        with open(config_path) as file:
            json.load(file)
    except json.JSONDecodeError:
        with open(config_path, "w") as file:
            json.dump(def_config, file, ensure_ascii=False, indent=4)
        return

def existed(extension: str, config: dict[str, list[str]]) -> bool:
    """
    Check if a certain extension is already in config

    :type extension: str
    :param extension: The extension we're trying to check.
    :type config: dict[str, list[str]]
    :param config: The config contains extension for each category.
    """
    for k in config.keys():
        if extension in config[k]:
            return True
    return False

def main() -> None:
    """
    The main function.
    """
    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    config_file_name = "config.json"
    config_folder = path.join(path.expanduser("~"), "claire_config")
    config_path = path.join(config_folder, config_file_name)

    illegal_chars = [*r'\/:*?"<>|']
    def_config = {
        "Images": [".png", ".jpg", ".jpeg", ".webp", ".gif"],
        "Videos": [".mp4", ".avi", ".webm", ".mkv", ".flv"],
        "Documents": [".doc", ".docx", ".pdf", ".txt"],
        "Sounds": [".mp3", ".wav", ".m4a"],
        "Archives": [".zip", ".rar"],
        "Executables": [".exe"]
    }
    
    makedirs(config_folder, exist_ok = True)
    config_manager(def_config, config_folder, config_file_name)

    with open(config_path) as file:
        config = json.load(file)

    clear()
    while True:
        cmd = input("1. Choose a folder to organize. \n2. Options. \n3. Exit. \nYour input: ").strip()
        clear()

        if cmd not in [*"123"]:
            print("Invalid input: Option does not exist. \n")
        elif not cmd:
            print("Invalid input: Empty input. \n")
        elif cmd == "3":
            root.destroy()
            exit(0)
        elif cmd == "1":
            target = tkinter.filedialog.askdirectory(title="Choose your output folder. Cancel to go back")
            if not target:
                print("Cancelled. \n")
                continue
            file_sorter(target, config)
            print("Sucessful. \n")

        while cmd == "2":
            categories = [x for x in config.keys()]
            options = [str(x) for x in range(1, len(config) + 4)]
            option = input(f"""Configure file types in each category.
{ziz_utils.menu(config)}
{len(config) + 1}. Add/Remove file category.
{len(config) + 2}. Go back.
{len(config) + 3}. Reset setting to default.
Your input: """).strip()
            clear()

            option_index = int(option) - 1
            if option not in options:
                print("Invalid input: Option does not exist. \n")
            elif not option:
                print("Invalid input: Empty input. \n")
            elif option == str(len(config) + 2):
                break
            elif option == str(len(config) + 3):
                    while True:
                        confirm = input("Do you want to reset setting to default? [Y/N]: ").strip().lower()
                        clear()

                        if confirm == "n":
                            print("Cancelled.")
                            break
                        elif confirm not in [*"yn"]:
                            print("Invalid input: Option does not exist. \n")
                            continue
                        elif not confirm:
                            print("Invalid input: Empty input. \n")
                            continue

                        config = def_config
                        print("Success. \n")
                        break

            elif option == str(len(config) + 1):
                while True:
                    mode = input("1. Add. \n2. Remove. \n3. Back. \nYour input: ").strip()
                    clear()

                    if mode not in [*"123"]:
                        print("Invalid input: Option does not exist. \n")
                    elif not mode:
                        print("Invalid input: Empty input. \n")
                    elif mode == "3":
                        break

                    while mode == "1":
                        category = input(f"{ziz_utils.menu(config)} \nYour input (Type / to go back): ").strip()
                        clear()

                        if category == "/":
                            break
                        elif category in categories:
                            print("Invalid input: Category already exist. \n")
                            continue
                        elif any(char in illegal_chars for char in category):
                            print("Invalid input: Category's name contains illegal character(s). \n")
                            continue
                        elif not category:
                            print("Invalid input: Empty input. \n")
                            continue

                        config.setdefault(category, [])
                        categories = [x for x in config.keys()]
                        ziz_utils.write_config(def_config, config, config_folder, config_file_name)
                    
                    while mode == "2":
                        temp = [str(x) for x in range(1, len(config) + 1)]
                        category = input(f"Type the category you want to remove: \n{ziz_utils.menu(config)} \n{len(config) + 1}. Exit. \nYour input: ").strip()
                        clear()

                        if category == str(len(config) + 1):
                            break
                        elif category not in temp:
                            print("Invalid input: Option does not exist. \n")
                            continue
                        elif not category:
                            print("Invalid input: Empty input. \n")
                            continue

                        del config[categories[int(category) - 1]]
                        categories = [x for x in config.keys()]
                        ziz_utils.write_config(def_config, config, config_folder, config_file_name)
                continue
        
            while True:
                extensions = config[categories[option_index]]
                mode = input(f"""Configure file extension for {categories[option_index]}:
1. Append mode. 
2. Remove mode.
3. Back
Your input: """).strip()
                clear()

                if mode == "3":
                    break
                elif mode not in [*"123"]:
                    print("Invalid input: Option does not exist. \n")
                elif not mode:
                    print("Invalid input: Empty input. \n")

                
                while mode == "1":
                    if extensions:
                        extension = input(fr"""Type the file extension you want to add to the "{categories[option_index]}" list of extension:
{ziz_utils.menu(extensions)}
Your input (Preceed the extension with a ".") (Type / to go back): """).strip()
                    else:
                        extension = input(fr"""Type the file extension you want to add to the "{categories[option_index]}" list of extension:
Your input (Preceed the extension with a ".") (Type / to go back): """).strip()
                    clear()

                    if extension == "/":
                        break
                    elif extension.startswith(".") and extension.count(".") == 1 and len(extension) > 1 and not existed(extension, config):
                        config[categories[option_index]].append(extension)
                        ziz_utils.write_config(def_config, config, config_folder, config_file_name)
                    elif "." not in extension and extension and not existed(extension, config):
                        extension = "." + extension
                        config[categories[option_index]].append(extension)
                        ziz_utils.write_config(def_config, config, config_folder, config_file_name)
                    elif existed(extension, config):
                        print("Invalid input: Extension already exist in other category. \n")
                    elif not extension:
                        print("Invalid input: Empty input. \n")
                    else:
                        print("Invalid input: Not a valid extension. \n")
                    
                while mode == "2":
                    options = [str(x) for x in range(1, len(config) + 2)]
                    if extensions:
                        option = input(fr"""Type the extension you want to remove from the "{categories[option_index]}" list of extension:
{ziz_utils.menu(extensions)}
{len(extensions) + 1}. Go back.
Your input: """).strip()
                    else:
                        option = input(fr"""Type the extension you want to remove from the "{categories[option_index]}" list of extension:
{len(extensions) + 1}. Go back.
Your input: """).strip()
                    ziz_utils.clear()

                    if option == str(len(extensions) + 1):
                        break
                    elif option not in options:
                        print("Invalid input: Not a valid extension. \n")
                        continue
                    elif not option:
                        print("Invalid input: Empty input. \n")
                        continue

                    del extensions[int(option) - 1]
                    ziz_utils.write_config(def_config, config, config_folder, config_file_name)

if __name__ == "__main__":
    main()