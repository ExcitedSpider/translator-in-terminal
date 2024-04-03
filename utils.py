def meaning_to_string(meaning):
    def formatDefinition(wordDef):
        string = f"Definition: {wordDef['definition']}"
        if 'example' in wordDef:
            string + f"\nExample: {wordDef['example']}"
        return string
    
    return "Part Of Speech: " + meaning['partOfSpeech'] + "\n" + '\n'.join(map(formatDefinition, meaning['definitions']))
