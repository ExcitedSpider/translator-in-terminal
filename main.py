import deepl
import configparser
from datetime import datetime
import os
from termcolor import cprint
import re

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
            raise KeyError(f"Option '{option}' not found in section '{section}'")
    else:
        raise KeyError(f"Section '{section}' not found in the configuration file")


def __main__(): 
    auth_key = read_config_value("config.ini", 'Translator', 'auth_key')
    target_lang = read_config_value("config.ini", 'Translator', 'target_lang')
    print(f"auth_key: ${auth_key}")

    while(True): 
      from_text = ""
      cprint("Please enter your text. Ends with $ or a single new line", color="light_blue")
      while(True):
        input_line = input()
        if input_line == "":
            if from_text == "":
              cprint("Please say something", color="light_red")
            else:
              break
        elif input_line.endswith("$"):
            input_line = input_line.removesuffix('$')
            from_text += input_line
            break
        else:
            from_text += input_line
      cprint("Processing...", color="light_blue")

      from_text = from_text.replace("\r\n", " ")
      from_text = from_text.replace("\n\r", " ")
      from_text = from_text.replace("\n", " ")

      translator = deepl.Translator(auth_key)

      if contain_foreign(from_text):
        result = translator.translate_text(from_text, target_lang="EN-US")
      else:
        result = translator.translate_text(from_text, target_lang=target_lang)

      base_filename = datetime.now().strftime('%Y%m%d%H%M') + "-" + " ".join(from_text.split()[:3])

      history_folder = './history/'
      path = history_folder + base_filename

      replicate_key = 1
      unique_file_name = base_filename
      while(os.path.exists(history_folder + unique_file_name + '.txt')):
        unique_file_name = base_filename + str(replicate_key)
        replicate_key += 1

      cprint("Done. Here's your words:", color="light_blue")

      # print(from_text)
      print(result.text)


      with open(history_folder + unique_file_name + '.txt', 'w', encoding="utf-8") as file:
        file.write(from_text)
        file.write('\n\n')
        file.write(result.text)


__main__()