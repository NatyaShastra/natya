import React from "react";
import { Navbar } from "./Navbar"; // Import Navbar
import "../styles/Header.css";
// import logo from "../assets/natya.png"; // Ensure correct path

export const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-top">
        <h1 className="header-title">NatyaShastra</h1>
        {/* <img src={logo} alt="NatyaShastra Logo" className="header-logo" /> */}
      </div>
      <p className="header-tagline">
        Transforming students, to create a powerful future through Dance
      </p>
      <Navbar />
    </header>
  );
};
