from googletrans import Translator

def create_translation_dict_pro():
    french_words = ["Bonjour", "Au revoir", "Bienvenue", "A bientôt"]
    translator = Translator()
    
    # Dictionary comprehension: {key: value for item in list}
    return {word: translator.translate(word, src='fr', dest='en').text for word in french_words}

if __name__ == "__main__":
    print(create_translation_dict_pro())