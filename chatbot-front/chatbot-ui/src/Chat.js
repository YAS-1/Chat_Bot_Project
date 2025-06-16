import React, { useState } from 'react';
import axios from 'axios';
import './Chat.css';

export const Chat = () => {

    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { sender: "user", text:input };
        setMessages([...messages, userMessage]);

        try {
            const res = await axios.post("http://localhost:5000/chat", { message: input });
            const botMessage = { sender: "bot", text: res.data.reply };
            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            const errorMsg = { sender: "bot", text: "Oops! Server error"};
            setMessages((prev) => [...prev, errorMsg]);
        }
        setInput("");
        
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') sendMessage();
    };

    return (
        <div className="chat-container">
        <div className="chat-box">
            {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.sender}`}>
                {msg.text}
            </div>
            ))}
        </div>
        <div className="input-area">
            <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Type a message..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
        </div>
    );
}

export default Chat;

