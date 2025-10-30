import React, { useState } from 'react';
import './App.css';

const styles = {
  sidebarOptionHover: {
    backgroundColor: '#333333',
  }
};

function Sidebar({ setCurrentPage, setChatHistory, handleClearChat }) {
  const [hoveredOption, setHoveredOption] = useState(null);

  const options = ['Chat 1', 'Chat 2', 'Chat 3', 'Chat 4'];
  const clearChatOption = 'Clear Current Chat';

  return (
    <div className="sidebar">
      <h2 style={{ marginBottom: '30px' }}>StockSense</h2>
      <nav>
        {options.map((option, index) => (
          <div className="sidebarOption"
            key={index}
            style={{
              ...(hoveredOption === index ? styles.sidebarOptionHover : {})
            }}
            onMouseEnter={() => setHoveredOption(index)}
            onMouseLeave={() => setHoveredOption(null)}
            onClick={() => setCurrentPage(option.toLowerCase().replace(' ', ''))}
          >
            {option}
          </div>
        ))}
      </nav>
	  <div className="hidden"></div>
      <div className="clearOption" onClick={handleClearChat}>
        {clearChatOption}
      </div>
    </div>
  );
}

function ChatInterface({ chatId, chatHistory, setChatHistory }) {
  const [input, setInput] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
	
    if (input.trim()) {
	let x = input;
	setInput('');
	
	setChatHistory(prev => ({
			...prev,
			[chatId]: [...(prev[chatId] || []), {
			  type: 'getting_input',
			  content: "You: "+x,
			  timestamp: new Date().toISOString(),
			}],
		  }));
	
    try {
      // Send input to the Flask server
      const response = await fetch('http://localhost:5000/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input.trim()}),
      });

      // Check if the response is successful
      if (response.ok) {
        const data = await response.json();
        
        // Assuming the server response contains a message
        const aiResponse = {
          type: 'ai_response',
          content: data.message,  // Data from Flask response
          timestamp: new Date().toISOString(),
        };

        // Update chat history with Flask's response
        setChatHistory(prev => ({
          ...prev,
          [chatId]: [...(prev[chatId] || []), aiResponse],
        }));
      } else {
		  const data = await response.json();
		  const failResponse = {
          type: 'fail_response',
          content: "Failure to retrieve data from AI. Please try again later.",
          timestamp: new Date().toISOString(),
        };
        setChatHistory(prev => ({
          ...prev,
          [chatId]: [...(prev[chatId] || []), failResponse],
        }));
      }
    } catch (error) {
		  console.error('Error communicating with Flask server:', error);
		  setChatHistory(prev => ({
			...prev,
			[chatId]: [...(prev[chatId] || []), {
			  type: 'error',
			  content: 'Unable to connect to the server. Please try again later.',
			  timestamp: new Date().toISOString(),
			}],
		  }));
		}
	}

  // Clear input after sending
  setInput('');
  };

  return (
    <div className="content">
      <div className="topWarningBar">
        <p><b>Please double check information provided by StockSense. AI generated content may not always be accurate.</b></p>
      </div>
      <div className="chatArea">
        <div className="output">
		  {chatHistory[chatId]?.map((msg, index) => (
			<div key={index}>
			  <p>{msg.content}</p>
			</div>
		  ))}
		</div>
        <form onSubmit={handleSubmit} className="bottomChatBar">
          <input className="chatInput"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Chat with AI..."
          />
          <button type="submit" className="chatButton">Send</button>
        </form>
      </div>
    </div>
  );
}

function App() {
  const [chatHistory, setChatHistory] = useState({});
  const [currentPage, setCurrentPage] = useState('chat1');
  
  const handleClearChat = () => {
    const confirmed = window.confirm('Are you sure you want to clear the current chat?');
    if (confirmed) {
      setChatHistory(prev => ({
      ...prev,
      [currentPage]: [],
    }));
    }
  };

  return (
    <div className="app">
      <Sidebar 
        setCurrentPage={setCurrentPage}
        setChatHistory={setChatHistory}
		handleClearChat={handleClearChat}
      />
      <ChatInterface 
        chatId={currentPage} 
        chatHistory={chatHistory} 
        setChatHistory={setChatHistory}
      />
    </div>
  );
}

export default App;
