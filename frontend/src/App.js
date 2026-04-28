import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const [form, setForm] = useState({
    name: "",
    date: "",
    type: "",
    notes: "",
  });

  // Chat send
  const sendMessage = async () => {
    if (!message.trim()) return;

    const newChat = [...chat, { sender: "user", text: message }];
    setChat(newChat);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message,
      });

      setChat([
        ...newChat,
        { sender: "bot", text: res.data.response || "No response" },
      ]);
    } catch (err) {
      setChat([
        ...newChat,
        { sender: "bot", text: "Error connecting to backend" },
      ]);
    }

    setMessage("");
  };

  // Form submit
  const handleFormSubmit = async () => {
    if (!form.name || !form.date || !form.type) {
      alert("Please fill all required fields");
      return;
    }

    const text = `Doctor ${form.name}, Date ${form.date}, Type ${form.type}, Notes ${form.notes}`;

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        message: text,
      });

      setChat([
        ...chat,
        { sender: "user", text },
        { sender: "bot", text: res.data.response },
      ]);

      // Reset form
      setForm({
        name: "",
        date: "",
        type: "",
        notes: "",
      });

    } catch {
      alert("Error submitting form");
    }
  };

  return (
    <div className="container">

      {/* Sidebar */}
      <div className="sidebar">
        <h2>AI CRM Assistant</h2>
        <p>Manage healthcare interactions using AI</p>
      </div>

      {/* Main */}
      <div className="main">

        {/* Chat Section */}
        <div className="chat-section">
          <h3>Chat Assistant</h3>

          <div className="chat-box">
            {chat.map((msg, index) => (
              <div
                key={index}
                className={msg.sender === "user" ? "user-msg" : "bot-msg"}
              >
                {msg.text.split("\n").map((line, i) => (
                  <div key={i}>{line}</div>
                ))}
              </div>
            ))}
          </div>

          <div className="input-box">
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your message..."
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        </div>

        {/* Form Section */}
        <div className="form-section">
          <h3>Log Interaction</h3>

          <input
            placeholder="Doctor Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />

          <input
            type="date"
            value={form.date}
            onChange={(e) => setForm({ ...form, date: e.target.value })}
          />

          <input
            placeholder="Interaction Type"
            value={form.type}
            onChange={(e) => setForm({ ...form, type: e.target.value })}
          />

          <input
            placeholder="Notes"
            value={form.notes}
            onChange={(e) => setForm({ ...form, notes: e.target.value })}
          />

          <button onClick={handleFormSubmit}>Submit</button>
        </div>

      </div>
    </div>
  );
}

export default App;