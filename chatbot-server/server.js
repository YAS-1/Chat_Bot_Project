// Dependencies
import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import {spawn} from "child_process";

// Create an Express app
const app = express();

// Middlewares
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// The chat functionality
app.post("/chat", (req, res) => {

    const userInput = req.body.message;// Get the user's input

    const pyProcess = spawn("python",["../chatbot.py", userInput]);// Start the Python process

    let botResponse = "";// Variable to store the bot's response

    // Listen for the child process to send data
    pyProcess.stdout.on("data", (data) =>{
        botResponse += data.toString();
    });

    // Listen for the child process error
    pyProcess.stderr.on("data", (data) => {
        console.error("Error:", data.toString());
    });

    // Listen for the child process to close
    pyProcess.on("close", () => {
        if (!botResponse.trim() === "🤖 I'm sorry, I don't understand.") 
        console.log("Bot response:", botResponse);
        res.json({reply: botResponse.trim()});
    });

    console.log("User input:", userInput);
});

//Start the server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
