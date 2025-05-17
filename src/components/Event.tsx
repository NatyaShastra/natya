import React from "react";
import "../styles/EventGallery.css";

export const Event: React.FC = () => (
  <div className="event-bg">
    <div className="event-content">
      <h2>Upcoming Events</h2>
      <ul>
        <li>
          <h2><strong>NatyaShastra Annual Dance Festival</strong><br /></h2>
          Date: June 7, 2025<br />
          Venue: Preston Prime Mall, Gachibowli, Hyderabad<br />
          Participants & More details: <a target="_blank" href="https://docs.google.com/spreadsheets/d/1EvOy75xYUpiKmKyBkCwcthnsWNVV4N43/edit?gid=1636669978#gid=1636669978">Click here for the list</a><br />
        </li> 
      </ul>
    </div>
  </div>
);

export default Event;
