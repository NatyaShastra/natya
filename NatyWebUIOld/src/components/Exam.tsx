import React from "react";
import "../styles/Onboarding.css";

export const Exam: React.FC = () => (
  <div className="exam-bg">
    <div className="exam-content">
      <h2>Exam Application & Eligibility</h2>
      <h3>How to Apply</h3>
      <ul className="exam-list">
        <li>Fill out the online exam application form. <a href="https://forms.gle/3dqBKPTy3aCovfvC9" target="_blank">Apply for Grade Exam</a></li>
        <li>Submit required documents and fees.</li>
        <li>Wait for confirmation from the admin.</li>
      </ul>
      <h3>Eligibility List</h3>
      <ul className="exam-list">
        <li><a href="https://docs.google.com/spreadsheets/d/1XuUXtjczPtIzU4CvxBYIOl1Yckng26LT/edit?gid=353205811#gid=353205811" target="_blank">Exam Eligibility & Fee details</a></li>  
      </ul>
    </div>
  </div>
);

export default Exam;
