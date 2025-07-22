import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Navbar from './navbar.jsx'
import './navbar.css'
import React, { useEffect, useState } from "react";
import './adminpage.css'

function ChannelTable() {
  const [channels, setChannels] = useState([]);

  useEffect(() => {
    fetch("http://youtube_api:5001/channels")
      .then((res) => res.json())
      .then((data) => setChannels(data))
      .catch((err) => console.error(err));
  }, []);

  
  return (
    <div>
      <h1>YouTube Channels</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Country</th>
            <th>Views</th>
            <th>Video count</th>
            <th>Subscribers</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          {channels.map((channel) => (
            <tr key={channel.id}>
              <td>{channel.title}</td>
              <td>{channel.country}</td>
              <td>{channel.views}</td>
              <td>{channel.video_count}</td>
              <td>{channel.subscribers.toLocaleString()}</td>
              <td>
                <a
                  href={channel.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Visit
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ChannelTable;


