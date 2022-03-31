import json
import io

def get_phrases():
    with io.open('phrases.json', 'r', encoding='utf-8') as json_:
        phrase = json.load(json_)
        return phrase


if __name__ == '__main__':
    pass
