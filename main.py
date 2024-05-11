import deepl
import configparser
from datetime import datetime
import os
from termcolor import cprint
import re
import requests
from utils import meaning_to_string

"""
if a string contains non-english characters
"""

def contain_foreign(text):
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    return bool(chinese_pattern.search(text))


"""
Read a configuration file and extract a specific value.

Args:
    config_file (str): Path to the configuration file.
    section (str): Section in the configuration file.
    option (str): Option within the specified section.

Returns:
    str: Value corresponding to the specified section and option.
"""


def read_config_value(config_file, section, option):
    config = configparser.ConfigParser()
    config.read(config_file)

    if section in config:
        if option in config[section]:
            return config[section][option]
        else:
            raise KeyError(
                f"Option '{option}' not found in section '{section}'")
    else:
        raise KeyError(
            f"Section '{section}' not found in the configuration file")


def create_folder_if_not_exsit(folder_path):
    """
    Create a folder if it does not exist.

    Args:
        folder_path (str): Path to the folder to be created.

    Returns:
        bool: True if the folder was created or already exists, False otherwise.
    """
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        try:
            # Create the folder if it does not exist
            os.makedirs(folder_path)
            return True
        except OSError as e:
            raise KeyError(f"Error creating folder '{folder_path}': {e}")
            return False
    else:
        return True

script_dir = os.path.dirname(__file__)
config_file_path = os.path.join(script_dir, "config.ini")
auth_key = read_config_value(config_file_path, 'Translator', 'auth_key')
target_lang = read_config_value(config_file_path, 'Translator', 'target_lang')


def __main__():
    while (True):
        from_text = ""
        cprint("Please enter your text. Ends with $ or a single new line",
               color="light_blue")
        while (True):
            input_line = input()
            if input_line == "":
                break
            elif input_line.endswith("$"):
                input_line = input_line.removesuffix('$')
                from_text += input_line
                break
            else:
                from_text += input_line

        if from_text == "":
            cprint("Please say something", color="light_red")
            continue

        cprint("Processing...", color="light_blue")

        result = {"text": None}
        isSentence = contain_foreign(from_text) or any(char.isspace() for char in from_text)

        if isSentence:
            result = translate_sentences(from_text)
        else:
            result = translate_word(from_text)

        base_filename = datetime.now().strftime('%Y%m%d%H%M') + "-" + \
            " ".join(from_text.split()[:3])

        history_folder = './history/'
        create_folder_if_not_exsit(history_folder)

        replicate_key = 1
        unique_file_name = base_filename
        while (os.path.exists(history_folder + unique_file_name + '.txt')):
            unique_file_name = base_filename + str(replicate_key)
            replicate_key += 1

        if isSentence:
            cprint("Translate Result:", color="light_blue")
        else:
            cprint("Word Definition:", color="light_blue")
        # print(from_text)
        print(result.text)

        with open(history_folder + unique_file_name + '.txt', 'w', encoding="utf-8") as file:
            file.write(from_text)
            file.write('\n\n')
            file.write(result.text)


# https://dictionaryapi.dev/
dictionary_url_base = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


class Result:
    def __init__(self, text):
        self.text = text


def translate_word(from_word):
    response = requests.get(dictionary_url_base + from_word)
    if response.status_code == 200:
        resJson = response.json()
        def parseWord(word): return "\n\n".join(
            map(meaning_to_string, word['meanings']))
        return Result("\n\n".join(map(parseWord, resJson)))
    elif "message" in response.json():
        return Result(response.json()['message'])
    else:
        return Result("Network Error")


def translate_sentences(from_text):
    from_text = from_text.replace("\r\n", " ")
    from_text = from_text.replace("\n\r", " ")
    from_text = from_text.replace("\n", " ")

    translator = deepl.Translator(auth_key)

    if contain_foreign(from_text):
        result = translator.translate_text(from_text, target_lang="EN-US")
    else:
        result = translator.translate_text(
            from_text, target_lang=target_lang)

    return Result(result.text)


__main__()
