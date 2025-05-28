class Chat :
    def __init__(self, name):
        self.name = name

    def meow(self):
        print(f"{self.name} says Meow!")

    def __str__(self):
        return f"Chat(name={self.name})"
    

if __name__ == "__main__":
    chat1 = Chat("Mittens")
    chat2 = Chat("Whiskers")
    chat3 = Chat("Shadow")
    chat4 = Chat("Shadow")  # Duplicate name, but different instance
    set_de_chats = {
        chat1,
        chat2,
        chat3,
        chat4
    }
    for chat in set_de_chats:
        chat.meow()  # Output: Mittens says Meow! (and so on for other cats)
    
    set_de_chats.remove(chat2)
    print("After removing Whiskers:")
    print(len(set_de_chats))  # Output: {Chat(name=Mittens), Chat(name=Shadow)}
    