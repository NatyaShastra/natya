import React from "react";
import "../styles/EventGallery.css";

export const Event: React.FC = () => (
  <div className="event-bg">
    <div className="event-content">
      <h2>Completed Events</h2>
      <ul>
        <li>
          <h2><strong>2025 Salangai & NatyaShastra 9th Annual Day Celebration</strong></h2>
          <div>Salangai Students: <strong>Hiya, Moksha, Anivitha, Sri Saanvi</strong></div>
          <div>Venue: Preston Prime Mall, Gachibowli, Hyderabad</div>
          <div>
            Highlights: <a href="https://www.youtube.com/watch?v=j6bXFoU9RNc" target="_blank" rel="noopener noreferrer">Watch Highlights</a><br />
            Full Video: <a href="https://www.youtube.com/watch?v=8TONd98ippA&t=6354s" target="_blank" rel="noopener noreferrer">Watch Full Event</a><br />
            More details: <a href="https://docs.google.com/spreadsheets/d/1EvOy75xYUpiKmKyBkCwcthnsWNVV4N43/edit?gid=1636669978#gid=1636669978" target="_blank" rel="noopener noreferrer">Participation & Details</a>
          </div>
        </li>
        <li>
          <h2><strong>2024 NatyaShastra Annual Day & Salangai Pooja</strong></h2>
          <div>Salangai Students: <strong>Neha, Amaya, Hitakshi</strong></div>
          <div>Venue: Preston Prime Mall, Gachibowli, Hyderabad</div>
          <div>
            Highlights: <a href="https://www.youtube.com/watch?v=z4bqEwFoWRE" target="_blank" rel="noopener noreferrer">Watch Highlights</a><br />
            Full Video: <a href="https://www.youtube.com/watch?v=fLo7PHAv70U&t=6647s" target="_blank" rel="noopener noreferrer">Watch Full Event</a>
          </div>
        </li>
      </ul>
    </div>
  </div>
);

export default Event;
