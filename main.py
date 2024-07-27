from datetime import datetime
import os
from termcolor import cprint
import re
from utils import read_config_value, get_input, parse_input_text, TaskCategory
from processors import translate_sentences, translate_word, Result

script_dir = os.path.dirname(__file__)
config_file_path = os.path.join(script_dir, "config.ini")
auth_key = read_config_value(config_file_path, 'Translator', 'auth_key')
target_lang = read_config_value(config_file_path, 'Translator', 'target_lang')

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


def __main__():
    while (True):
        raw_input = get_input()
        cmd = parse_input_text(raw_input)
        input_text = cmd.input 

        cprint("Processing...", color="light_blue")

        result = Result()

        if cmd.taskCat == TaskCategory.Translate or cmd.taskCat == TaskCategory.Unknown:
            result = translate_sentences(input_text, auth_key, target_lang)
        elif cmd.taskCat == TaskCategory.Dictionary:
            result = translate_word(input_text)

        base_filename = datetime.now().strftime('%Y%m%d%H%M') + "-" + \
            " ".join(input_text.split()[:3])

        history_folder = './history/'
        create_folder_if_not_exsit(history_folder)

        replicate_key = 1
        unique_file_name = base_filename
        while (os.path.exists(history_folder + unique_file_name + '.txt')):
            unique_file_name = base_filename + str(replicate_key)
            replicate_key += 1

        # print(input_text)
        print(result.text)

        with open(history_folder + unique_file_name + '.txt', 'w', encoding="utf-8") as file:
            file.write(input_text)
            file.write('\n\n')
            file.write(result.text)


__main__()