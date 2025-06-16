# Simple Rule-Based Chatbot

This project is a simple command-line chatbot built with Python and NLTK. It uses a predefined set of intents and responses stored in a JSON file to interact with users.

## Features

*   **Intent-Based Responses:** Understands user input based on keywords and matches it to predefined intents.
*   **JSON-Powered:** Intents, patterns, and responses are loaded from an external `intents.json` file, making it easy to extend and modify the chatbot's knowledge.
*   **Text Preprocessing:**
    *   Converts input text to lowercase.
    *   Removes punctuation.
    *   Tokenizes text into individual words.
    *   Removes common English stopwords.
*   **Randomized Responses:** Selects a random response from the list of available responses for a matched intent, making interactions feel more varied.
*   **Multilingual Support (Basic):** Includes examples of greetings in English and Luganda.
*   **Simple Conversation Loop:** Engages users in a continuous conversation until they choose to exit.
*   **Easy Exit:** Users can type "exit", "quit", or "bye" to end the chat.

## How It Works

1.  **Load Intents:** The chatbot loads conversational intents from `intents.json`. Each intent has a `tag`, a list of `patterns` (phrases a user might say), and a list of `responses` (what the bot can reply).
2.  **User Input:** The chatbot prompts the user for input.
3.  **Clean Input:** The user's input text is cleaned:
    *   Converted to lowercase.
    *   Punctuation is removed.
    *   The text is tokenized into words.
    *   Stopwords (common words like "is", "the", "a") are removed.
4.  **Match Intent:** The cleaned user input tokens are compared against cleaned tokens from the patterns defined in `intents.json`.
    *   If any token from a pattern is found in the user's input tokens, the corresponding intent is considered a match.
5.  **Generate Response:** If a matching intent is found, the chatbot randomly selects one of the predefined responses for that intent.
6.  **No Match:** If no intent matches the user's input, a default "I don't understand" message is returned.
7.  **Loop:** The process repeats until the user exits.

## File Structure

```
Chat_Bot_Project/
├── chatbot.py        # Main Python script for the chatbot logic
├── intents.json      # JSON file containing intents, patterns, and responses
└── README.md         # This file
```

## `intents.json` Structure

The `intents.json` file has the following structure:

```json
{
  "intents": [
    {
      "tag": "unique_intent_identifier",
      "patterns": ["User phrase 1", "User keyword", "Another example pattern"],
      "responses": ["Bot response 1", "Bot response 2"]
    },
    {
      "tag": "another_intent",
      "patterns": ["..."],
      "responses": ["..."]
    }
    // ... more intents
  ]
}
```

*   `tag`: A unique name or category for the intent (e.g., "greeting", "book_appointment").
*   `patterns`: A list of example phrases or keywords that a user might type to express this intent.
*   `responses`: A list of possible responses the chatbot can give if this intent is matched.

