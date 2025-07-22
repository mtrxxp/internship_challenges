
import { Routes, Route } from 'react-router-dom';
import Navbar from './navbar.jsx';
import Shortener from './shortener.jsx';
import QRCodeGenerator from './coder.jsx';
import ChannelTable from './scrabber.jsx';
import AdminPage from './AdminPage.jsx';

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/shortener" element={<Shortener />} />
        <Route path="/qrcode" element={<QRCodeGenerator />} />
        <Route path="/scrabber" element={<ChannelTable />} />
        <Route path="/table" element={<AdminPage />} />
      </Routes>
    </>
  );
}