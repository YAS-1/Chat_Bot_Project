import nltk #Natural Language Toolkit
from nltk.tokenize import word_tokenize # For tokenization
from nltk.corpus import stopwords # For stopwords removal 
import string # For removing punctuation
import json # For loading JSON files
import random # For selecting a random response


#Downloading the required packages
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


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


#Creating a conversation loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Bot: Goodbye!")
        break
    response = get_response(user_input)
    print("Bot:", response)