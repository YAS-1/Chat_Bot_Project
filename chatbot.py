import nltk # type: ignore #Natural Language Toolkit
from nltk.tokenize import word_tokenize # type: ignore # For tokenization
from nltk.corpus import stopwords # type: ignore # For stopwords removal 
import string # For removing punctuation
import json # For loading JSON files
import random # For selecting a random response
import sys # For system commands
import os # For file operations
import io # For input/output operations
from nltk.corpus import wordnet # For wordnet


#Downloading the required packages
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)


#Setting the intents path--
script_dir = os.path.dirname(os.path.abspath(__file__))
intents_path = os.path.join(script_dir, 'intents.json')

#Getting the intents from the JSON file--
with open (intents_path, 'r') as file:
    intents = json.load(file)

#Custom responses--
custom_responses = {
    "who created you": "I was created by Yawe Arthur 💡.",
    "what's your name": "I'm your smart assistant 🤖.",
    "tell me a joke": "Why did the computer go to therapy? Because it had too many bytes of issues! 😂",
    "how are you": "I'm just code, but thanks for asking! I'm running great 🧠.",
    "greetings": ["Hello!", "Hi!", "Hey!", "Howdy!", "Greetings!"],
    "farewells": ["Goodbye!", "Bye!", "See you later!", "Take care!", "Farewell!"],
    "thanks": ["You're welcome!", "My pleasure!", "Anytime!", "No problem!", "Glad to help!"],
    "sorry": ["It's okay!", "No worries!", "Don't worry about it!", "It's all good!", "No problem!"],
    "default": ["I'm sorry, I don't understand.", "I'm not sure I understand.", "Could you please rephrase that?", "I'm not sure how to respond to that.", "I'm not sure what you mean."]
}

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


#Function to get the synonyms of a word--
def expand_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower().replace('_', ' '))
    return synonyms


#Function for cleaning the user's input--
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


#Function to get the bot's response--
def get_response(text):
    tokens = clean_text(text)
    cleaned_input = ' '.join(tokens)
    best_score = 0
    best_response = None
    
    #Check if the user's input is a custom response--
    text_lower = text.lower()
    for key in custom_responses:
        if key in text_lower:
            response = custom_responses[key]
            if isinstance(response, list):
                return random.choice(response)
            return response

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            pattern_tokens = clean_text(pattern)

            
            #Expand the pattern tokens with synonyms--
            pattern_synonyms = set()
            for word in pattern_tokens:
                pattern_synonyms.update(expand_synonyms(word))
                pattern_synonyms.add(word) #Add the word itself as a synonym


            #Expand the user tokens with synonyms--
            user_synonyms = set()
            for word in tokens:
                user_synonyms.update(expand_synonyms(word))
                user_synonyms.add(word) #Add the word itself as a synonym


            #Calculate the score--
            common_words = set(tokens).intersection(set(pattern_tokens))
            score = len(common_words) / (len(set(pattern_tokens).union(set(tokens))) or 1)

            if score > best_score:
                best_score = score
                best_response = random.choice(intent['responses'])
                


    if best_score < 0.2:
        return "🤖 I'm sorry, I don't understand."
    return best_response

#Function to save the chat history--
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