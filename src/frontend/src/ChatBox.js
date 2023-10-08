import React, { useState } from "react";
import './ChatBox.css';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    const response = await fetch(`http://0.0.0.0:5601/query?text=${input}`);
    const text = await response.text();
    setMessages([...messages, { user: 'You', text: input }, { user: 'Bot', text }]);
    setInput("");
  };

  return (
    <div className="chatbox">
      <div className="messages">
        {messages.map((message, idx) => (
          <div key={idx} className={`message ${message.user.toLowerCase()}`}>
            <strong>{message.user}</strong>: {message.text}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default ChatBox;
