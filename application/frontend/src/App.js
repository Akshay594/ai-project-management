import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [userRequest, setUserRequest] = useState('');
  const [jsonFile, setJsonFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!jsonFile) {
      alert('Please upload a JSON file');
      return;
    }

    const formData = new FormData();
    formData.append('user_request', userRequest);
    formData.append('file', jsonFile);

    try {
      const response = await axios.post('http://127.0.0.1:8000/process_request', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-4">Project Management App</h1>
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-full max-w-md">
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="userRequest">
            User Request
          </label>
          <input
            id="userRequest"
            type="text"
            value={userRequest}
            onChange={(e) => setUserRequest(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="jsonFile">
            Upload JSON File
          </label>
          <input
            id="jsonFile"
            type="file"
            accept="application/json"
            onChange={(e) => setJsonFile(e.target.files[0])}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            required
          />
        </div>
        <div className="flex items-center justify-between">
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Submit
          </button>
        </div>
      </form>
      {result && (
        <div className="mt-6 bg-white p-6 rounded shadow-md w-full max-w-md">
          <h2 className="text-2xl font-bold mb-4">Result</h2>
          <pre className="whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
