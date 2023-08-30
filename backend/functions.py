import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.metrics.distance import edit_distance

from typing import List

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class QuestionProcessing:
    def __preprocess_text(self, text: str) -> List[str]:
        # Приведение к нижнему регистру
        text = text.lower()

        # Удаление знаков препинания
        text = ''.join([c for c in text if c.isalpha() or c.isspace()])

        # Токенизация
        tokens = word_tokenize(text)

        # Удаление стоп-слов
        stop_words = set(stopwords.words('russian'))
        tokens = [token for token in tokens if token not in stop_words]
        
        stemmer = SnowballStemmer('russian')
        tokens = [stemmer.stem(token) for token in tokens]
        # Лемматизация
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return tokens


    def __compare_questions(self, question1: str, question2: str):
        # Предварительная обработка вопросов
        tokens1 = self.__preprocess_text(question1)
        tokens2 = self.__preprocess_text(question2)

        # Сравнение вопросов по редакционному расстоянию (edit distance)
        distance = edit_distance(tokens1, tokens2)

        # Нормализация расстояния
        normalized_distance = distance / max(len(tokens1), len(tokens2))

        return normalized_distance
    

    def find_closest_question(self, user_question: str, list_of_questions: List[dict[str, str]]) -> str:
        # print(list_of_questions)
        closest_distance = 1
        closest_question = ''
        for qa in list_of_questions:
            distance = self.__compare_questions(user_question, qa['question'])
            print(distance, qa['question'])
            if distance < closest_distance and distance < 0.75:
                closest_distance = distance
                closest_question = qa['question']
        print(closest_distance, closest_question)
        return closest_question
