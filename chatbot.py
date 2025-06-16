import nltk #Natural Language Toolkit
from nltk.tokenize import word_tokenize # For tokenization
from nltk.corpus import stopwords # For stopwords removal 
import string # For removing punctuation
import json # For loading JSON files
import random # For selecting a random response
import sys # For system commands


#Downloading the required packages
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)


#Getting the intents from the JSON file
with open ('intents.json') as file:
    intents = json.load(file)



#Function for cleaning the user's input
def clean_text(text):

    #convert the text to lower
    text = text.lower()

    #remove paunctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    #Tokenize the text
    tokens =  word_tokenize(text)

    #remove the stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [ word for word in tokens if word not in  stop_words]

    return filtered_tokens


#Function to get the bot's response
def get_response(text):
    tokens = clean_text(text)
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            pattern_tokens = clean_text(pattern)

            #matching the text to a response
            if any(word in tokens for word in pattern_tokens):
                return random.choice(intent['responses'])

    return "I'm sorry, I don't understand."


#Function to save the chat history
def log_chat(user, bot):
    with open("chat_history.txt", "a") as file:
        file.write(f"User: {user}\n")
        file.write(f"Bot: {bot}\n\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_message = sys.argv[1]
        response = get_response(user_message)
        print("Bot:", response)
    else:
        #Creating a conversation loop
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Bot: Goodbye!")
                log_chat(user_input, "Goodbye!")
                break
            response = get_response(user_input)
            print("Bot:", response)
            log_chat(user_input, response)