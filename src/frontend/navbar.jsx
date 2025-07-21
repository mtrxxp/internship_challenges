import './navbar.css'

export default function Navbar(){
    return(
        <nav>
            <p>
                Challenges
            </p>
            <ul>
                <a href="../shortener.html">
                    <li>URL Shortener</li>
                </a>
                <a href="../qrcode.html">
                    <li>QR-Code Generator</li>
                </a>
                <a href="../scrabber.html">
                    <li>YT Scrapper</li>
                </a>
                <a href="../table.html">URLs table</a>
            </ul>
        </nav>
    )
};