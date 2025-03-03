import re
import json

def count_approximate_words_and_non_words(text):
    # Conta palavras
    words = re.findall(r'\b\w+\b', text)

    # Conta "não-palavras" (qualquer sequência de caracteres que não seja uma palavra, excluindo espaços)
    non_words = re.findall(r'[^\w\s]+', text)

    return len(words), len(non_words)

def count_approximate_words_non_words_and_tokens(text):
    words,non_words = count_approximate_words_and_non_words(text)

    return words, non_words, int(0.75*(words+non_words))


def generate_word_token_json(text):
    # Contar palavras e tokens
    word_count, no_word_count, token_count = count_approximate_words_non_words_and_tokens(text)
    
    # Criar o dicionário com as contagens
    result = {
        'approximate_word_count': word_count,
        'approximate_no_word_count': no_word_count,
        'approximate_token_count': token_count,
        'character_count': len(text)
    }
    
    # Converter o dicionário para string JSON
    result_json = json.dumps(result, indent=4)
    
    return result_json
