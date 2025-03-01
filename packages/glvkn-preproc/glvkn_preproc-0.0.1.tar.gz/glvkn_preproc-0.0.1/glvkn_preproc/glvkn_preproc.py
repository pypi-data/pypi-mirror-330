import re
import nltk
import spacy
import unicodedata
import string
import emoji
import sentencepiece as spm
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer
from langdetect import detect
from tokenizers import Tokenizer
from tokenizers.models import BPE, WordPiece
from tokenizers.trainers import BpeTrainer, WordPieceTrainer
from tokenizers.pre_tokenizers import Whitespace

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

morph_ru = MorphAnalyzer()
nlp_models = {}

bpe_tokenizer = Tokenizer(BPE())
wordpiece_tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))
bpe_tokenizer.pre_tokenizer = Whitespace()

def get_spacy_model(lang):
    if lang not in nlp_models:
        try:
            nlp_models[lang] = spacy.load(f"{lang}_core_news_sm")
        except OSError:
            nlp_models[lang] = None
    return nlp_models.get(lang)

def get_stopwords(lang):
    try:
        return set(stopwords.words(lang))
    except OSError:
        return set()

def process_text(text, tokenizer='nltk'):
    """
    tokenizer:
    'nltk' - NLTK токенизация
    'spacy' - spaCy токенизация
    """
    # Определение языка
    try:
        lang = detect(text)
    except:
        lang = 'en'  # По умолчанию английский
    
    # Очистка текста
    text = text.lower()
    text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")  # Замена кавычек
    text = re.sub(r'\d+', '<NUM>', text)  # Замена цифр
    text = re.sub(r'[@#$%^&*]', ' ', text)  # Удаление спецсимволов
    text = re.sub(r'@\w+', '<MENTION>', text)  # Замена упоминаний
    text = re.sub(r'#\w+', '<HASHTAG>', text)  # Замена хештегов
    text = re.sub(r'<.*?>', ' ', text)  # Удаление HTML-тегов
    text = re.sub(r'[^\w\s]', ' ', text)  # Удаление спецсимволов, но сохранение дефисов
    text = re.sub(r'\s+', ' ', text).strip()  # Удаление лишних пробелов
    text = emoji.replace_emoji(text, replace='<EMOJI>')  # Замена эмодзи
    
    # Получение стоп-слов
    stop_words = get_stopwords(lang)
    
    # Токенизация и лемматизация
    if tokenizer == 'nltk':
        tokens = word_tokenize(text)
    elif tokenizer == 'spacy':
        nlp = get_spacy_model(lang)
        if nlp:
            tokens = [token.lemma_ for token in nlp(text) if token.text.lower() not in stop_words and not token.is_punct]
        else:
            tokens = word_tokenize(text)
    else:
        tokens = word_tokenize(text)
    
    # Удаление стоп-слов
    tokens = [word for word in tokens if word not in stop_words]
    
    return ' '.join(tokens)

