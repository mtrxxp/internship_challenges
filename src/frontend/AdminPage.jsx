import React, { useEffect, useState } from 'react';
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Navbar from './navbar.jsx'
import './navbar.css'
import './adminpage.css'

export default function AdminPage() {
  const [urls, setUrls] = useState([]);
  const [selectedLink, setSelectedLink] = useState(null);
  const [clickData, setClickData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/all_urls')
      .then((res) => res.json())
      .then((data) => setUrls(data))
      .catch((err) => console.error(err));
  }, []);

  const viewClicks = (shortId) => {
    fetch(`http://localhost:5000/analytics/${shortId}`)
      .then((res) => res.json())
      .then((data) => {
        setSelectedLink(data);
        setClickData(data.click_data);
      })
      .catch((err) => console.error(err));
  };

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <h2>All Shortened Links</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Original URL</th>
            <th>Short ID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {urls.map((url) => (
            <tr key={url.id}>
              <td>{url.id}</td>
              <td>{url.original_url}</td>
              <td>{url.short_id}</td>
              <td>
                <button
                  onClick={() => viewClicks(url.short_id)}
                >
                  View Clicks
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {selectedLink && (
        <div className='table_clicks'>
          <h2>
            Clicks for <strong>{selectedLink.short_id}</strong> ({selectedLink.clicks} clicks)
          </h2>
          <table>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Referrer</th>
                <th>User Agent</th>
                <th>IP Address</th>
              </tr>
            </thead>
            <tbody>
              {clickData.map((click, idx) => (
                <tr key={idx}>
                  <td>{click.timestamp}</td>
                  <td>{click.referrer || '-'}</td>
                  <td>{click.user_agent}</td>
                  <td>{click.ip_address}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Navbar />
    <AdminPage />
  </StrictMode>,
)