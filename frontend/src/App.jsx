import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import FileUpload from './components/FileUpload';
import React from 'react';

function App() {
  const [count, setCount] = useState(0)

  return (
      <div>
      <FileUpload />
    </div>
      
  )
}

export default App
