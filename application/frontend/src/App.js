import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [userRequest, setUserRequest] = useState('');
  const [jsonFile, setJsonFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const [subQuestions, setSubQuestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!jsonFile) {
      alert('Please upload a JSON file');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('user_request', userRequest);
    formData.append('file', jsonFile);

    try {
      const response = await axios.post('http://127.0.0.1:8000/process_request', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'user', content: userRequest },
        { role: 'assistant', content: response.data.result },
      ]);
      setSubQuestions(response.data.sub_questions);
      setUserRequest('');
    } catch (error) {
      console.error('Error uploading file:', error);
    }

    setLoading(false);
  };

  const handleSubQuestionClick = (subQuestion) => {
    setUserRequest(subQuestion.sub_question);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="bg-white p-6 rounded shadow-lg w-full max-w-3xl">
        <h1 className="text-3xl font-bold mb-6">Project Management Chat</h1>
        <div className="mb-6">
          <label className="block text-gray-700 font-bold mb-2" htmlFor="jsonFile">
            Upload JSON File
          </label>
          <input
            id="jsonFile"
            type="file"
            accept="application/json"
            onChange={(e) => setJsonFile(e.target.files[0])}
            className="border border-gray-300 rounded-lg py-2 px-4 w-full"
            required
          />
        </div>
        <div className="h-96 overflow-y-auto mb-6">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg mb-4 ${
                message.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'
              }`}
            >
              <p className="font-bold">{message.role === 'user' ? 'You' : 'Assistant'}</p>
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>
          ))}
        </div>
        {subQuestions.length > 0 && (
          <div className="mb-6">
            <h2 className="text-xl font-bold mb-2">Related Questions</h2>
            <div className="grid grid-cols-2 gap-4">
              {subQuestions.map((subQuestion, index) => (
                <button
                  key={index}
                  className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
                  onClick={() => handleSubQuestionClick(subQuestion)}
                >
                  {subQuestion.sub_question}
                </button>
              ))}
            </div>
          </div>
        )}
        <form onSubmit={handleSubmit}>
          <div className="flex">
            <input
              type="text"
              value={userRequest}
              onChange={(e) => setUserRequest(e.target.value)}
              className="flex-grow border border-gray-300 rounded-lg py-2 px-4 mr-4"
              placeholder="Type your message..."
              required
            />
            <button
              type="submit"
              className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
              disabled={loading}
            >
              {loading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;