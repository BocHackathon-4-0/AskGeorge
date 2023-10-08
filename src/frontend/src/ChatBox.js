import React, { useState } from "react";
import './ChatBox.css';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = (e) => {
    e.preventDefault();

    // Check if the message is empty or has less than 3 characters
    if (!input.trim() || input.length < 3) {
        return; // Exit the function
    }

    const userMessage = {
      user: "You",
      text: input
    };
    
    setMessages(prevMessages => [userMessage, ...prevMessages]);
    setIsLoading(true);

    fetch(`http://127.0.0.1:5601/query?text=${input}`)
      .then((response) => response.text())
      .then((data) => {
        const botMessage = {
          user: "Bot",
          text: data
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
            {message.text}
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
