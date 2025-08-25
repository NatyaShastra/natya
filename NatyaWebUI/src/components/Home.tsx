import React from "react";
import { Link } from "react-router-dom";
import "../styles/Home.css";

export const Home: React.FC = () => (
  <div className="home-bg">
    <video
      className="home-bg-video"
      src="/home_bg.mp4"
      autoPlay
      loop
      muted
      playsInline
    />
    <div className="home-content">
      <div className="home">
        <h2>Welcome to NatyaShastra</h2>
        <p>Experience the joy of dance, blending tradition and culture in perfect harmony.</p>
        
        <Link to="/enquiry" className="btn">I want to Enquire</Link>
        <Link to="/onboarding" className="btn">I want to Onboard</Link>
        <Link to="/booking" className="btn">I want to Order</Link>
        <button className="btn" style={{background: '#0077ff'}} onClick={() => window.tidioChatApi?.open()}>
          Chat with us
        </button>
        
        <p>Are you an existing customer?</p>
        <Link to="https://books.zohosecure.in/portal/natyashastra/signin#" className="btn">I want to Renew / Make payment</Link>
      </div>
    </div>
  </div>
);

export default Home;
