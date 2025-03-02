from random import choice
from os import path, makedirs
from ziz_utils import clear
import string
import json
import ziz_utils

def PasswordGenerator(password_length: int, charlist: list[str]) -> str:
    """
    Generate password with length equals to password_length and characters takes from charlist

    :type password_length: int
    :param password_length: Self-explanatory
    :type charlist: list[str]
    :param charlist: List of characters used to 
    """
    output = ""
    while len(output) < password_length:
        output += choice(charlist)
    return output

def main() -> None:
    """
    The main function
    """
    config_file_name = "config.json"
    config_folder = path.join(path.expanduser("~"), "thors_hammer")
    config_path = path.join(config_folder, config_file_name)

    def_config = {
        "isUppercaseLettersEnabled": True,
        "isNumberEnabled": True,
        "isSpecialCharactersEnabled": True,
        "passwordLength": 8
    }
    
    makedirs(config_folder, exist_ok = True)
    ziz_utils.config_manager(def_config, config_folder, config_file_name)

    with open(config_path) as file:
        config = json.load(file)

    clear()
    while True:
        cmd = input("1. Generate passwords. \n2. Config. \n3. Exit. \nYour input: ").strip()
        clear()
        
        if cmd == "3":
            exit(0)
        elif not cmd:
            print("Invalid input: Empty input. \n")
            continue
        elif cmd not in [*"12"]:
            print("Invalid input: Command does not exist. \n")
            continue
        
        while cmd == "2":
            option = input(f"""Config password generation.
1. Config password length.
2. Generate uppercase alphabetical characters: {config["isUppercaseLettersEnabled"]}.
3. Generate numbers: {config["isNumberEnabled"]}.
4. Generate special characters: {config["isSpecialCharactersEnabled"]}.
5. Go back.
Toggle: """).strip()
            clear()

            match option:
                case "2": 
                    config["isUppercaseLettersEnabled"] = not config["isUppercaseLettersEnabled"]
                case "3": 
                    config["isNumberEnabled"] = not config["isNumberEnabled"]
                case "4": 
                    config["isSpecialCharactersEnabled"] = not config["isSpecialCharactersEnabled"]
                case "5": 
                    break
                case "":
                    print("Invalid input: Empty input. \n")
                case "1":
                    while True:
                        print(f"Current password length: {config["passwordLength"]}.")
                        p_len = input("Enter the length of your password (from 8 to 20 characters, preceed your number with * to bypass this)(Enter / to cancel): ").strip()
                        clear()

                        if p_len == "/":
                            break
                        elif not p_len:
                            print("Invalid input: Empty input. \n")
                        elif not ziz_utils.isInt(p_len) and not p_len.startswith("*"):
                            print("Invalid input: Input have to be an integer. \n")
                        elif not p_len.startswith("*"):
                            if int(p_len) <= 8 or int(p_len) >= 20:
                                print("Invalid input: Password length can only be in range from 8 to 20 characters, preceed your number with * to bypass this. \n")
                        elif int(p_len.replace("*", "")) <= 0:
                            print("Invalid input: Password length cannot be shorter than 1. \n")

                        config["passwordLength"] = int(p_len.replace("*", ""))
                        ziz_utils.write_config(def_config, config, config_folder, config_file_name)
                case _:
                    print("Invalid input: Option does not exist. \n")

        password_chars = string.ascii_lowercase
        if config["isUppercaseLettersEnabled"]:
            password_chars += string.ascii_uppercase
        if config["isNumberEnabled"]: 
            password_chars += string.digits
        if config["isSpecialCharactersEnabled"]: 
            password_chars += string.punctuation.replace("|", "")

        if cmd == "1":
            password = PasswordGenerator(config["passwordLength"], password_chars)
        while cmd == "1":
            print(f"Output: {password} \n")
            regen = input("Do you want to regenerate your password? [Y/N]: ").strip().upper()
            clear()

            if regen == "N":
                break
            elif not regen or regen == "Y":
                password = PasswordGenerator(config["passwordLength"], password_chars)
            else:
                print("Invalid input: Option does not exist. \n")

if __name__ == "__main__":
    main()