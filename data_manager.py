import json

def read_dictionary(our_file):
    with open(our_file, "r", encoding="utf-8") as fi:
        data = fi.readlines()
    return data

def write_chats(filename, information, today):
    new = open(filename, "a")
    new.write(today + "\n")
    new.write(str(information) + "\n")