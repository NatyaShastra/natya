import React from "react";
import { Link } from "react-router-dom";
import "../styles/Home.css";

export const Home: React.FC = () => {
  return (
    <div className="home">
      <h2>Welcome to NatyaShastra</h2>
      <p>Experience the joy of dance, blending tradition and culture in perfect harmony.</p>
      
      <Link to="/enquiry" className="btn">I want to Enquire</Link>
      <Link to="/onboarding" className="btn">I want to Onboard</Link>
      <Link to="/booking" className="btn">I want to Order</Link>
      
      <p>Are you an existing customer?</p>
      <Link to="https://books.zohosecure.in/portal/natyashastra/signin#" className="btn">I want to Renew</Link>
    </div>
  );
};
