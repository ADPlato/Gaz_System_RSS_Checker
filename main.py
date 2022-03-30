import feedparser
import pickle
import tkinter


def get_actual_RSS(URL):
    parsed_data = feedparser.parse(URL)
    messages_list = []
    for info in parsed_data['entries']:
        messages_list.append(f'{info["updated"]}\n{info["title"]}')
    return messages_list


def get_previous_RSS():
    try:
        file = open("messages", 'rb')
        messages = pickle.load(file)
    except:
        file = open("messages", 'wb')
        messages = []

    file.close()
    return messages


def save_RSS(messages):
    file = open("messages", 'wb')
    pickle.dump(messages, file)
    file.close()


def popup_message(message):
    popup = tkinter.Tk()
    popup.title("Gaz-System RSS")
    label = tkinter.Label(popup, text=message)
    label.pack(side="top", fill="x", pady=10)
    button_accept = tkinter.Button(popup, text="Przeczytano", command=popup.destroy)
    button_accept.pack(fill="x")
    popup.mainloop()


URL = 'https://www.gaz-system.pl/pl/rss-komunikaty-ogloszenia.html'

actual_messages = get_actual_RSS(URL)
previous_messages = get_previous_RSS()

if len(actual_messages) > len(previous_messages):
    message = actual_messages[len(actual_messages) - len(previous_messages) - 1]
    popup_message(f"NOWA WIADOMOSC:\n{message}")
    previous_messages.append(message)
    save_RSS(previous_messages)

elif len(actual_messages) < len(previous_messages):
    popup_message("Błąd XML")
