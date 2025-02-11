import React from "react";
import { Link } from "react-router-dom";

export const Home: React.FC = () => {
  return (
    <div className="home">
      <h2>Welcome to NatyaShastra</h2>
      <p>Experience the joy of dance, blending tradition and culture in perfect harmony.</p>
      <Link to="/onboarding" className="btn">Join a Class</Link>
      <Link to="/enquiry" className="btn">Enquire Now</Link>
    </div>
  );
}; 
