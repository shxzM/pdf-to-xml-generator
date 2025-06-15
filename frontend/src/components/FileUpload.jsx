import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [xmlOutput, setXmlOutput] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/convert/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setXmlOutput(response.data.xml);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Upload failed.");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>PDF to XML Converter</h2>
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <br/><br/>
      <button onClick={handleUpload}>Upload and Convert</button>

      {xmlOutput && (
        <div style={{ marginTop: 20 }}>
          <h3>Converted XML:</h3>
          <pre>{xmlOutput}</pre>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
