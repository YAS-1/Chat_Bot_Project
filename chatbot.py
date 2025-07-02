import nltk #Natural Language Toolkit
from nltk.tokenize import word_tokenize # For tokenization
from nltk.corpus import stopwords # For stopwords removal 
import string # For removing punctuation
import json # For loading JSON files
import random # For selecting a random response
import sys # For system commands
import os # For file operations


#Downloading the required packages
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

#Setting the intents path
script_dir = os.path.dirname(os.path.abspath(__file__))
intents_path = os.path.join(script_dir, 'intents.json')

#Getting the intents from the JSON file
with open (intents_path, 'r') as file:
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
    best_score = 0
    best_response = "🤖 I'm sorry, I don't understand."
    best_tag = None
    
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            pattern_tokens = clean_text(pattern)
            common_words = set(tokens).intersection(set(pattern_tokens))
            score = len(common_words) / (len(set(pattern_tokens).union(set(tokens))) or 1)

            if score > best_score:
                best_score = score
                best_response = random.choice(intent['responses'])
                best_tag = intent['tag']


    print(f"Best score: {best_score}, Best response: {best_response}, Best tag: {best_tag}")

    return best_response if best_score >= 0.2 else "🤖 I'm sorry, I don't understand."

#Function to save the chat history
def log_chat(user, bot):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of chatbot.py
    log_path = os.path.join(base_dir, "chat_history.txt")  # Path to chat_history.txt

    with open(log_path, 'a', encoding="utf-8") as file:
        file.write(f"User: {user}\n")
        file.write(f"Bot: {bot}\n\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_message = sys.argv[1]
        response = get_response(user_message)
        print(response)
        # log_chat(user_message, response)
    else:
        #Creating a conversation loop
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Bot: Goodbye!")
                log_chat(user_input, "Goodbye!")
                break
            response = get_response(user_input)
            print(response)
            log_chat(user_input, response)