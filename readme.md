# Translator

A command-line translator powered by [deepl](https://www.deepl.com/translator)

## Usage

1. Register a deepl account, and get the token
2. Clone this repo
3. Install dependencies
    ```
    pip install deepl
    pip install termcolor
    ```
4. create a config file `config.ini` in the same folder of `main.py`, copy this content:
    ```
    [Translator]
    auth_key = <your deepl token>
    target_lang = zh
    ```
5. Start by 
    ```
    $ python main.py
    ```