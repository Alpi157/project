import fuzzywuzzy
from fuzzywuzzy import process
from nltk.tokenize import word_tokenize
from nltk.metrics import distance

def handle_question(data, question, file_path):
    question = question.lower()
    question = word_tokenize(question)
    closest_question = ""
    closest_distance = float("inf")
    closest_answer = ""
    for entry in data:
        q = entry["question"].lower()
        q_text = word_tokenize(q)
        dist = distance.edit_distance(question, q_text)
        if dist < closest_distance:
            closest_distance = dist
            closest_question = q
            closest_answer = entry["answer"]
    if closest_distance < 3:
        return closest_answer
    else:
        new_question = ' '.join(question) + "+++"
        data.append({"question": new_question, "answer": ""})
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return "Извините, у меня пока нет ответа на этот вопрос. Но я добавил ваш вопрос в базу данных."