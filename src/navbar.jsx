import { Link } from 'react-router-dom';
import './navbar.css';

export default function Navbar() {
  return (
    <nav>
      <p>Challenges</p>
      <ul>
        <li><Link to="/shortener">URL Shortener</Link></li>
        <li><Link to="/qrcode">QR-Code Generator</Link></li>
        <li><Link to="/scrabber">YT Scrapper</Link></li>
        <li><Link to="/table">URLs table</Link></li>
      </ul>
    </nav>
  );
};