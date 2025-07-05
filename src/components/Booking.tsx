import React from "react";
import "../styles/Booking.css";

export const Booking: React.FC = () => (
  <div className="order-bg">
    <div className="order-content">
      <h2>Explore the NatyaShastra Cultural Shoppe</h2>
      <p>
        Order your dance books, uniforms, and accessories easily at our store. 
        We offer a Cash on Delivery (COD) option, and you can conveniently pay 
        using the payment invoices sent to your account.
      </p>

      <p>
        To explore our store, check out our:
        <a 
          href="https://natyashastra.myinstamojo.com/" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ marginLeft: "5px" }}
        >
          NatyaShastra Essentials Store 
        </a>.
      </p>
      <p>
        To access your payment invoices and manage orders, visit:
        <a 
          href="https://books.zohosecure.in/portal/natyashastra/signin#" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ marginLeft: "5px" }}
        >
          NatyaShastra Payments Portal
        </a>.
      </p>
      <button className="btn" style={{background: '#0077ff'}} onClick={() => window.tidioChatApi?.open()}>
        Need help? Chat with us
      </button>
    </div>
  </div>
);

export default Booking;
