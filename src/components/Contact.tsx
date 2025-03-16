import React from "react";

import "../styles/Contact.css";
export const Contact: React.FC = () => {
  return (
    <div className="page-container">
      <h2>Contact Us</h2>
      <p>📍 Location: Gachibowli & Tellapur, Hyderabad</p>
      <p>📞 Phone: <a href="tel:9845517116">Call us</a></p>
      <p>📧 Email: <a href="mailto:NatyaShastra@gmail.com">Email us</a></p>
      <p>💬 WhatsApp (Only escalations): <a href="https://wa.me/9344134242" target="_blank" rel="noopener noreferrer">Chat Now</a></p>
    </div>
  );
}; 