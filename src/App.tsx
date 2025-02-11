import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from './components/Header';
// import { Navbar} from './components/Navbar';
// import Carousel from './components/Carousel';
import Footer from './components/Footer';
import {Home } from './components/Home'
import {About} from './components/About';
import {Services} from './components/Services'; 
import {Contact} from './components/Contact';  
import {Enquiry} from  './components/Enquiry';   
import {Onboarding} from  './components/Onboarding';   
import {Booking} from  './components/Booking';    

const App: React.FC = () => {
  return (
    <Router>  {/* Ensure your Router is wrapping your components */}
      <Header />
      {/* <Navbar />   */}
      <Routes>
        {/* <Route path="/" element={<Carousel />} /> */}
        <Route path="/" element={<Home />} />
        <Route path="/enquiry" element={<Enquiry />} />
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/booking" element={<Booking />} />
        <Route path="/about" element={<About />} />
        <Route path="/services" element={<Services />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;
