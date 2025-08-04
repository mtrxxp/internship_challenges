import { Link } from 'react-router-dom';
import './navbar.css';

export default function Navbar() {
  return (
    <nav>
      <p>🚀 Challenges</p>
      <ul>
        <li>
          <Link to="/shortener">
            <svg xmlns="http://www.w3.org/2000/svg" 
                 fill="none" viewBox="0 0 24 24" 
                 strokeWidth="1.5" stroke="currentColor"
                 className="icon">
              <path strokeLinecap="round" strokeLinejoin="round" 
                    d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
            URL Shortener
          </Link>
        </li>
        <li>
          <Link to="/qrcode">
            <svg xmlns="http://www.w3.org/2000/svg" 
                 fill="none" viewBox="0 0 24 24" 
                 strokeWidth="1.5" stroke="currentColor"
                 className="icon">
              <path strokeLinecap="round" strokeLinejoin="round" 
                    d="M3 3h7v7H3V3zM14 3h7v7h-7V3zM3 14h7v7H3v-7zM14 14h3v3h-3v-3z" />
            </svg>
            QR-Code Generator
          </Link>
        </li>
        <li>
          <Link to="/scrabber">
            <svg xmlns="http://www.w3.org/2000/svg" 
                 fill="none" viewBox="0 0 24 24" 
                 strokeWidth="1.5" stroke="currentColor"
                 className="icon">
              <path strokeLinecap="round" strokeLinejoin="round" 
                    d="M4.5 4.5l15 15m0-15l-15 15" />
            </svg>
            YT Scrapper
          </Link>
        </li>
        <li>
          <Link to="/table">
            <svg xmlns="http://www.w3.org/2000/svg" 
                 fill="none" viewBox="0 0 24 24" 
                 strokeWidth="1.5" stroke="currentColor"
                 className="icon">
              <path strokeLinecap="round" strokeLinejoin="round" 
                    d="M4 6h16M4 10h16M4 14h16M4 18h16" />
            </svg>
            URLs Table
          </Link>
        </li>
      </ul>
    </nav>
  );
};
