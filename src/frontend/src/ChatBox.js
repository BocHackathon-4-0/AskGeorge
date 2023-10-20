import React, { useState } from "react";
import './ChatBox.css';
import ReactMarkdown from 'react-markdown';  // Import react-markdown

function ChatBox() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleSend = (e) => {
        e.preventDefault();

        if (!input.trim() || input.length < 3) {
            return;
        }

        const userMessage = {
            user: "You",
            type: "text",
            content: input
        };

        setMessages(prevMessages => [userMessage, ...prevMessages]);

        setIsLoading(true);

        fetch(`http://127.0.0.1:5601/query?text=${input}`)
            .then((response) => response.text())
            .then((data) => {
                const botMessage = {
                    user: "Bot",
                    type: "markdown",  // Set type to markdown for bot's responses
                    content: data
                };
                setMessages(prevMessages => [botMessage, ...prevMessages]);
                setIsLoading(false);
            })
            .catch((error) => {
                console.error("Error:", error);
                setIsLoading(false);
            });
        

        setInput("");
    };

    return (
        <div className={`chatbox ${messages.length > 0 ? 'has-messages' : ''}`}>
            <div className="messages">
                {[...messages].reverse().map((message, idx) => (
                    <div key={idx} className={`message ${message.user.toLowerCase()}`}>
                        {message.type === "text" && message.content}
                        {message.type === "markdown" && <ReactMarkdown>{message.content}</ReactMarkdown>}
                        {message.type === "image" && <img src={message.content} alt="Sent by bot" />}
                    </div>
                ))}
            </div>
            <form className="input-area" onSubmit={handleSend}>
                <input
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    placeholder="Type your message..."
                />
                <button type="submit" disabled={isLoading || !input.trim() || input.length < 3}>
                    Send
                </button>
            </form>
        </div>
    );
}

export default ChatBox;
