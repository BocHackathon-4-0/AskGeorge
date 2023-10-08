import React from 'react';
import './App.css';
import ChatBox from './ChatBox';
import Toolbar from './Toolbar'

function App() {
  return (
    <div className="App">
      <div className="sidebar">
          <Toolbar/>
      </div>
      <div className="chat-container">
        <ChatBox />
      </div>
    </div>
  );
}

export default App;
