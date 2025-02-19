import React from "react";
import "../styles/Booking.css"; // Updated CSS file name

export const Booking: React.FC = () => {
  return (
    <div className="booking-container">
      <h2>Provide your uniform and grade book details & submit the form</h2>
      <p>For more details on payments, venue, and timings, click enquiry.</p>

      {/* Embedded Google Form */}
      <iframe
        src="https://forms.gle/cgH3yYX4z8613p7R6"
        width="100%"
        height="1200px"
        frameBorder="0"
        marginHeight={0}
        marginWidth={0}
        allowFullScreen
        title="Booking Form"
      >
        Loading…
      </iframe>
    </div>
  );
};
