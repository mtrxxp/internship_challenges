import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import Navbar from './navbar.jsx';
import './navbar.css';
import './shortener.css';

import React, { useState } from 'react';

export default function URLShortener() {
  const [url, setUrl] = useState('');
  const [shortUrl, setShortUrl] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch('http://localhost:5000/shortener', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    if (res.ok) {
      const data = await res.json();
      setShortUrl(data.short_url); // ожидаем short_url, как в старом варианте
    } else {
      const error = await res.text();
      alert(`Ошибка при сокращении URL: ${error}`);
    }
  };

  return (
    <div className="shortener-container">
      <h1>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="icon-big"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
          />
        </svg>
        URL Shortener
      </h1>
      <form onSubmit={handleSubmit}>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL"
          required
        />
        <br />
        <button type="submit" className="btn">
          🔗 Shorten URL
        </button>
      </form>
      {shortUrl && (
        <p className="result">
          Shortened URL: <a href={shortUrl}>{shortUrl}</a>
        </p>
      )}
    </div>
  );
}
