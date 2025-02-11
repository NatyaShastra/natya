import React, { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css"; // Import CSS

import logo from "../assets/natya.png"; // Ensure correct path
export const Navbar: React.FC = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
        <img src={logo} alt="NatyaShastra Logo" className="header-logo" />
        </Link>
        <div className="menu-icon" onClick={() => setMenuOpen(!menuOpen)}>
          <div className={menuOpen ? "bar open" : "bar"}></div>
          <div className={menuOpen ? "bar open" : "bar"}></div>
          <div className={menuOpen ? "bar open" : "bar"}></div>
        </div>
        <ul className={menuOpen ? "nav-links open" : "nav-links"}>
          <li><Link to="/" onClick={() => setMenuOpen(false)}>Home</Link></li>
          <li><Link to="/enquiry" onClick={() => setMenuOpen(false)}>Enquiry</Link></li>
          <li><Link to="/onboarding" onClick={() => setMenuOpen(false)}>Onboard</Link></li>
          <li><Link to="/booking" onClick={() => setMenuOpen(false)}>Order</Link></li>
          <li><Link to="/about" onClick={() => setMenuOpen(false)}>About</Link></li>
          <li><Link to="/services" onClick={() => setMenuOpen(false)}>Services</Link></li>
          <li><Link to="/contact" onClick={() => setMenuOpen(false)}>Contact</Link></li>
        </ul>
      </div>
    </nav>
  );
};
