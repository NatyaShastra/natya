import React from 'react';
import { Link } from 'react-router-dom';  // For navigation

export const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/enquiry">Enquiry</Link></li>
        <li><Link to="/onboarding">Onboard</Link></li>
        <li><Link to="/booking">Place Orders</Link></li>
        <li><Link to="/about">About</Link></li>
        <li><Link to="/services">Services</Link></li>
        <li><Link to="/contact">Contact</Link></li>
      </ul>
    </nav>
  );
};