import React from "react";

// Add this to declare tidioChatApi on the window object
declare global {
  interface Window {
    tidioChatApi?: { open: () => void };
  }
}

import "../styles/Contact.css";
export const Contact: React.FC = () => (
  <div className="contact-bg">
    <div className="contact-content">
      <div className="page-container">
        <h2>Contact Us</h2>
        <p>📍 Location: Gachibowli & Tellapur, Hyderabad</p>
        <p>📞 Phone: <a href="tel:9845517116">Call us</a></p>
        <p>📧 Email: <a href="mailto:NatyaShastra@gmail.com">Email us</a></p>
        <p>💬 WhatsApp (Only escalations): <a href="https://wa.me/9344134242" target="_blank" rel="noopener noreferrer">Chat Now</a></p>
        <button className="btn" style={{background: '#0077ff'}} onClick={() => window.tidioChatApi?.open()}>
          Chat with us
        </button>
      </div>
    </div>
  </div>
);

export default Contact;