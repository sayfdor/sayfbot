from fuzzywuzzy import fuzz

other_letter = {'а': ['а', 'a', '@'], 'б': ['б', '6', 'b'], 'в': ['в', 'v'], 'г': ['г', 'r', 'g'],
                'д': ['д', 'd', 'g'], 'е': ['е', 'e'], 'ё': ['ё', 'e'], 'ж': ['ж', 'zh', '*'], 'з': ['з', '3', 'z'],
                'и': ['и', 'u', 'i'], 'й': ['й', 'u', 'i'], 'к': ['к', 'k', 'i{', '|{'], 'л': ['л', 'l', 'ji'],
                'м': ['м', 'm'], 'н': ['н', 'h', 'n'], 'о': ['о', 'o', '0'], 'п': ['п', 'n', 'p'], 'р': ['р', 'r', 'p'],
                'с': ['с', 'c', 's'], 'т': ['т', 'm', 't'], 'у': ['у', 'y', 'u'], 'ф': ['ф', 'f'],
                'х': ['х', 'x', 'h', '}{'], 'ц': ['ц', 'c', 'u,'], 'ч': ['ч', 'ch'], 'ш': ['ш', 'sh'],
                'щ': ['щ', 'sch'], 'ь': ['ь', 'b'], 'ы': ['ы', 'bi'], 'ъ': ['ъ'], 'э': ['э', 'e'], 'ю': ['ю', 'io'],
                'я': ['я', 'ya']}

obscene_words_cen = [[1089, 1091, 1082], [1087, 1080, 1079, 1076], [1076, 1072, 1091, 1085], [1093, 1091, 1081],
                     [1093, 1091, 1077], [1077, 1073], [1085, 1072, 1093], [1087, 1086, 1093, 1091],
                     [1087, 1086, 1088, 1085], [1087, 1086, 1088, 1077, 1074], [1084, 1080, 1085, 1077, 1090]]


def recensore(lst: list) -> list:
    obscene_words = []
    for word in lst:
        word = ''.join([chr(letter) for letter in word])
        obscene_words.append(word)
    return obscene_words


def replace_letters(message: str) -> str:
    message = message.lower().replace(' ', '')
    for key, value in other_letter.items():
        for letter in value:
            for phr in message:
                if letter == phr:
                    message = message.replace(phr, key)
    return message

def check(message: str) -> bool:
    message = replace_letters(message)
    for word in recensore(obscene_words_cen):
        for part in range(len(message)):
            fragment = message[part: part + len(word)]
            if fuzz.WRatio(fragment, word) > 70:
                return True
    return False


if __name__ == '__main__':
    pass
