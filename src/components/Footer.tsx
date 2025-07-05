import React from "react";

// Add this to declare tidioChatApi on the window object
declare global {
  interface Window {
    tidioChatApi?: { open: () => void };
  }
}

import "../styles/Footer.css";
const Footer: React.FC = () => {
  return (
    <footer>
      <p style={{ color: "white" }}>© 2025 NatyaShastra | All rights reserved</p>
      <a href="https://wa.me/9160228929">WhatsApp</a>
      <a href="tel:9160228929">Call Us</a>
      <div>
        <a
          href="https://www.facebook.com/share/15oQVLtAmE/?mibextid=wwXIfr"
          target="_blank"
          rel="noopener noreferrer"
        >
          Facebook
        </a>
        <a href="https://youtube.com/@natyashastraschoolofdance5525?si=PQKwF91-GSvxqJ1m" target="_blank" rel="noopener noreferrer">
          Youtube
        </a>
        <a
          href="https://instagram.com/natyashastraforall?igshid=MzMyNGUyNmU2YQ=="
          target="_blank"
          rel="noopener noreferrer"
        >
          Instagram
        </a>
      </div>
      <button className="btn" style={{background: '#0077ff', marginTop: '10px'}} onClick={() => window.tidioChatApi?.open()}>
        Need help? Chat with us
      </button>
    </footer>
  );
};

export default Footer;
