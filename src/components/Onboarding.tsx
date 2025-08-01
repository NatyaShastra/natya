import React from "react";
import "../styles/Navbar.css";
import "../styles/Onboarding.css";

export const Onboarding: React.FC = () => (
  <div className="onboard-bg">
    <div className="onboard-content">
      <div className="page-container">
        <h2>Join NatyaShastra</h2>
        <p>Ready to dance? Complete the onboarding process and be part of our vibrant community!</p>
        <a href="https://forms.gle/7eWsWetSH86qjNsA8" className="btn" target="_blank" rel="noopener noreferrer">Join Now</a>
      </div>
    </div>
  </div>
);

export default Onboarding;
