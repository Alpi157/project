import datetime 
import fuzzywuzzy
from bot_handler import BotHandler
from question_handler import handle_question
from data_manager import read_dictionary, write_chats

token = "YOUR_BOT_TOKEN"
path_dic = "tbot_dataset.txt"
unanswered_file_path = "unanswered.json"

greet_bot = BotHandler(token)
now = datetime.datetime.now()

rate = 77

def main():
    new_offset = None
    hour = now.hour
    dicti = []
    resp = read_dictionary(path_dic)
    dicti.append(resp)

    data = []

    unanswered_questions = []

    while True:
        updates = greet_bot.get_updates(new_offset)

        if len(updates) > 0:
            for update in updates:
                last_update = update
                last_update_id = last_update['update_id']
                last_chat_text = last_update['message']['text']
                last_chat_id = last_update['message']['chat']['id']
                last_chat_name = last_update['message']['chat']['first_name']
                try:
                    first_chat_name = last_update['message']['chat']['last_name']
                except:
                    first_chat_name = "none"

                if last_chat_text == "/start":
                    greet_bot.send_message(last_chat_id, 'Привет, {}! Пожалуйста, задайте свой вопрос.'.format(last_chat_name))
                else:
                    counter = 0
                    best_match = None
                    greet_bot.send_message(last_chat_id, 'Пожалуйста, подождите немного, {}.'.format(last_chat_name))
                    for el in dicti[0]:
                        if el.startswith("вопрос:"):
                            components = el.split("ответ:")
                            if len(components) == 2:
                                question, answer = components
                                leven = fuzzywuzzy.fuzz.partial_ratio(last_chat_text.lower(), question.lower().strip())
                                if leven >= rate and leven > counter:
                                    print("Understand")
                                    counter = leven
                                    best_match = answer.strip()

                    if best_match:
                        greet_bot.send_message(last_chat_id, best_match)
                    else:
                        unanswered_response = handle_question(data, last_chat_text, unanswered_file_path)
                        greet_bot.send_message(last_chat_id, unanswered_response)

                write_chats(last_chat_name + "_" + first_chat_name, last_update, str(datetime.datetime.now()))
                new_offset = last_update_id + 1

        else:
            print("No updates")

    if unanswered_questions:
        with open(unanswered_file_path, "a", encoding="utf-8") as file:
            for question in unanswered_questions:
                file.write(question + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()