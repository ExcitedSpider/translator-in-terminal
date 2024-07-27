import configparser
import re
from termcolor import cprint
from enum import Enum

def meaning_to_string(meaning):
    def formatDefinition(wordDef):
        string = f"Definition: {wordDef['definition']}"
        if "example" in wordDef:
            string += f"\nExample: {wordDef['example']}"
        return string
    
    return "Part Of Speech: " + meaning['partOfSpeech'] + "\n" + '\n'.join(map(formatDefinition, meaning['definitions']))

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

def get_input(printHint = True) -> str:
    from_text = ""
    if printHint:
        cprint("Please enter your text. Ends with $ or a single new line",
            color="light_blue")
    while from_text == "":
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
    return from_text 

class TaskCategory(Enum):
    Unknown = 0
    Translate = 1
    Dictionary = 2
    AIAssistant = 3

class Command:
    def __init__(self, taskCat: TaskCategory, input: str) -> None:
        self.taskCat = taskCat
        self.input = input

cmdword_to_task = {
    't': TaskCategory.Translate,
    'translate': TaskCategory.Translate,
    'd': TaskCategory.Dictionary,
    'dictionary': TaskCategory.Dictionary,
    'a': TaskCategory.AIAssistant,
    'ai': TaskCategory.AIAssistant,
    'c': TaskCategory.AIAssistant # for "chat"
}


def parse_input_text(txt: str) -> Command:
    """
    Parse the raw input text to a command object
    """
    words = txt.split()
    cmdWord = words[0].lower()
    
    if cmdWord in cmdword_to_task:
        return Command(cmdword_to_task[cmdWord], " ".join(words[1:]))
    else:
        return Command(TaskCategory.Unknown, txt)

def contain_foreign(text):
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    return bool(chinese_pattern.search(text))