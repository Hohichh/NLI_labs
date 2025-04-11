import re

def parse_noun_rules(input_str: str) -> dict:
    """Парсит правила для существительных"""
    parts = [p.strip() for p in input_str.split(',')]
    if len(parts) != 2:
        raise ValueError("Нужно указать 2 параметра через запятую: number, posessive")
    
    return {
        'number': parts[0],
        'posessive': parts[1]
    }

def parse_verb_rules(input_str: str) -> dict:
    """Парсит правила для глаголов"""
    parts = [p.strip() for p in input_str.split(',')]
    if len(parts) != 5:
        raise ValueError("Нужно указать 5 параметров через запятую: tense, tense_type, number, person, voice")
    
    return {
        'tense': parts[0],
        'tense_type': parts[1],
        'number': parts[2],
        'person': parts[3],
        'voice': parts[4]
    }

def parse_adjective_rules(input_str: str) -> dict:
    """Парсит правила для прилагательных и наречий"""
    parts = [p.strip() for p in input_str.split(',')]
    if len(parts) != 1:
        raise ValueError("Нужно указать 1 параметр: degree")
    
    return {
        'degree': parts[0]
    }

def parse_add_word(input_str: str) -> str:
    stripped_input = input_str.strip()
    if not stripped_input or ' ' in stripped_input:
        return None
    cleaned_word = re.sub(r"[^\w'-]", "", input_str, flags=re.UNICODE)
    cleaned_word = re.sub(r"^['-]+|['-]+$", "", cleaned_word)
    if not cleaned_word:
        return None
    
    return cleaned_word.strip()

