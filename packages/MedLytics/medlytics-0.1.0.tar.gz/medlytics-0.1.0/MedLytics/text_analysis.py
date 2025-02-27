# my_package/text_analysis.py
import spacy
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import textstat
from textblob import TextBlob


# nltk.download('punkt')
# nltk.download('stopwords')
# spacy.load('en_core_web_sm')
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')

class TextAnalysis:
    def __init__(self, text1, text2):
        self.text1 = text1
        self.text2 = text2
        self.length1 = 0
        self.length2 = 0
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words("english"))

    def type_token_ratio(self, text):
        words = word_tokenize(text)
        unique_words = set(words)
        return len(unique_words) / len(words) if words else 0

    def hapax_legomena(self, text):
        words = word_tokenize(text.lower())
        freq_dist = FreqDist(words)
        return [word for word, count in freq_dist.items() if count == 1]

    def ner(self, text):
        doc = self.nlp(text)
        entities = {
            "DRUGS/SUBSTANCES": [],
            "PEOPLE": [],
            "PLACES": [],
            "MEDICAL_TERMS": []
        }
        for ent in doc.ents:
            if ent.label_ == "PRODUCT":
                entities["DRUGS/SUBSTANCES"].append(ent.text)
            elif ent.label_ == "PERSON":
                entities["PEOPLE"].append(ent.text)
            elif ent.label_ == "GPE" or ent.label_ == "LOC":
                entities["PLACES"].append(ent.text)
            elif ent.label_ == "ORG" or ent.label_ == "MONEY":
                entities["MEDICAL_TERMS"].append(ent.text)
        return entities

    def function_word_frequency(self, text):
        words = word_tokenize(text.lower())
        function_words = [word for word in words if word in self.stop_words]
        return len(function_words) / len(words) if words else 0

    def punctuation_usage(self, text):
        punctuation_count = {p: text.count(p) for p in string.punctuation}
        total_punctuation = sum(punctuation_count.values())
        return punctuation_count, total_punctuation

    def readability_scores(self, text):
        flesch = textstat.flesch_reading_ease(text)
        gunning_fog = textstat.gunning_fog(text)
        smog = textstat.smog_index(text)
        return flesch, gunning_fog, smog

    def sentiment_analysis(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            return "Positive"
        elif sentiment < 0:
            return "Negative"
        else:
            return "Neutral"

    def semantic_categories(self, text):
        words = word_tokenize(text)
        categories = {
            "NOUNS": [],
            "VERBS": [],
            "ADJECTIVES": []
        }
        for word in words:
            pos_tag = nltk.pos_tag([word])[0][1]
            if pos_tag.startswith('NN'):
                categories["NOUNS"].append(word)
            elif pos_tag.startswith('VB'):
                categories["VERBS"].append(word)
            elif pos_tag.startswith('JJ'):
                categories["ADJECTIVES"].append(word)
        return categories

    def compare_texts(self):
        analysis = {
            "Type-Token Ratio": {
                "Text 1": self.type_token_ratio(self.text1),
                "Text 2": self.type_token_ratio(self.text2)
            },
            "Hapax Legomena": {
                "Text 1": self.hapax_legomena(self.text1),
                "Text 2": self.hapax_legomena(self.text2)
            },
            "NER": {
                "Text 1": self.ner(self.text1),
                "Text 2": self.ner(self.text2)
            },
            "Function Word Frequency": {
                "Text 1": self.function_word_frequency(self.text1),
                "Text 2": self.function_word_frequency(self.text2)
            },
            "Punctuation Usage": {
                "Text 1": self.punctuation_usage(self.text1),
                "Text 2": self.punctuation_usage(self.text2)
            },
            "Readability Scores": {
                "Text 1": self.readability_scores(self.text1),
                "Text 2": self.readability_scores(self.text2)
            },
            "Sentiment Analysis": {
                "Text 1": self.sentiment_analysis(self.text1),
                "Text 2": self.sentiment_analysis(self.text2)
            },
            "Semantic Categories": {
                "Text 1": self.semantic_categories(self.text1),
                "Text 2": self.semantic_categories(self.text2)
            }
        }
        return analysis
    

