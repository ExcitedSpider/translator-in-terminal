import unittest
import json
from utils import meaning_to_string

class TestUtils(unittest.TestCase):

    def test_meaning_to_string(self):
        meaning = json.loads("""{
          "partOfSpeech": "exclamation",
          "definitions": [
            {
              "definition": "used as a greeting or to begin a phone conversation.",
              "example": "hello there, Katie!",
              "synonyms": [],
              "antonyms": []
            }
          ]
        }""")
        print(meaning_to_string(meaning))

if __name__ == '__main__':
    unittest.main()