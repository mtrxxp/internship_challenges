import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Navbar from './navbar.jsx'
import './navbar.css'
import React, { useState } from 'react';
import './shortener.css'

function Shortener() {
  const [url, setUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('http://localhost:5000/shortener', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();
    if (data.short_url) {
      setShortUrl(data.short_url);
    } else {
      alert(data.error);
    }
  };
  return (
    <div className='shortener'>
      <h1>URL Shortener</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL"
        />
        <br></br>
        <button type="submit">
          Shorten
        </button>
      </form>
      {shortUrl && (
        <div>
          <p>Short URL:</p>
          <a className='URLShort' href={shortUrl}>{shortUrl}</a>
        </div>
      )}
    </div>
  );
}

export default Shortener;

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Navbar />
    <Shortener />
  </StrictMode>,
)