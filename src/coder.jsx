import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Navbar from './navbar.jsx'
import './navbar.css'
import React, { useState } from 'react';
import './coder.css'

export default function QRCodeGenerator() {
  const [text, setText] = useState('');
  const [qrCode, setQrCode] = useState(null);

  const generateQRCode = async () => {
    if (!text.trim()) {
      alert('Please enter some text');
      return;
    }

    const response = await fetch('/generate_qr', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    if (response.ok) {
      const blob = await response.blob();
      const imgUrl = URL.createObjectURL(blob);
      setQrCode(imgUrl);
    } else {
      alert('Error generating QR Code');
    }
  };

  return (
    <div className='coder'>
      <h1>QR Code Generator</h1>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter URL"
      />
      <br></br>
      <button
        onClick={generateQRCode}
      >
        Generate QR Code
      </button>
      <br></br>
      {qrCode && (
        <img src={qrCode} alt="QR Code" className='qr'/>
      )}
    </div>
  );
}

