import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [xmlOutput, setXmlOutput] = useState('');
  const [uploadedFileName, setUploadedFileName] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(e.target.files[0]);
    setUploadedFileName(selectedFile ? selectedFile.name : '');
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file first.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/convert/', formData);
      
      
      setXmlOutput(response.data.xml);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Upload failed.");
    }
  };

  const handleDownload = () => {
  if (!xmlOutput) {
    alert("No XML content to download!");
    return;
  }

  let xmlFileName = 'converted.xml';
    if (uploadedFileName) {
      xmlFileName = uploadedFileName.replace(/\.pdf$/i, '') + '.xml';
    }

  const blob = new Blob([xmlOutput], { type: 'application/xml' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', xmlFileName);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
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
          <button onClick={handleDownload}>Download XML</button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
