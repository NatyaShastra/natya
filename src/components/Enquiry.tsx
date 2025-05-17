import React, { useState } from "react";
import "../styles/Enquiry.css";
import { Link } from "react-router-dom";

export const Enquiry: React.FC = () => {
  const [openCategory, setOpenCategory] = useState<string | null>(null);

  const toggleCategory = (category: string) => {
    setOpenCategory(openCategory === category ? null : category);
  };

  const faqData = [
    {
      category: "General Information",
      questions: [
        { q: "What is NatyaShastra?", a: "NatyaShastra is a community-based dance studio dedicated to celebrating and teaching Bharatanatyam." },
        { q: "What dance styles do you offer?", a: "We offer classical Bharatanatyam in a traditional format in same way how we learnt from our Gurus from the roots of Tamil Nadu." },
        { q: "Where is NatyaShastra located?", a: "Our studio is at Hyderabad (in multiple avenues), with online classes available worldwide." },
        { q: "Do you offer online classes?", a: "Yes, we provide online classes for students across India and internationally." }
      ]
    },
    {
      category: "Enrollment & Classes",
      questions: [
        { q: "How do I enroll in a class?", a: "Visit our 'Onboard' page to fill out the registration form or contact us through the 'Enquiry' section." },
        { q: "What are the class timings?", a: "Class timings vary based on batch and venue. Please check the schedule in the 'Enquiry' section." },
        { q: "Are classes divided by age group?", a: "Yes, we have different batches for various age groups and skill levels." },
        { q: "Do you offer personalized dance coaching?", a: "Yes, we offer one-on-one coaching for those seeking extra guidance." },
        { q: "Can parents attend classes with younger children?", a: "In some beginner classes, parental involvement is allowed as per the instructor’s guidance." }
      ]
    },
    {
      category: "Fees & Payments",
      questions: [
        { q: "What is the fee structure?", a: "Fees vary by location, age group, and tenure. Contact us for details." },
        { q: "Are there any discounts available?", a: "Yes, we offer discounts for younger students and tenure-based packages." },
        { q: "What are the payment options?", a: "We accept online payments, UPI, net banking. CASH NOT ACCEPTED STRICTLY." },
        { q: "What are the due dates for Payment renewals?", a: "You will have invoices for Jan 5, April 5, June 5 & Oct 5" },
        // { q: "How do I update my enrollment or payment details?", a: "Reach out via the 'Enquiry' section to update your details." }
      ]
    },
    {
      category: "Tamboolam Tradition (Guru Shishya Parampara)",
      questions: [
        { q: "What is the Guru Shishya Parampara at NatyaShastra?", a: "Our teaching is rooted in the traditional Guru Shishya Parampara, emphasizing personalized mentorship and direct knowledge transfer." },
        { q: "How does this tradition influence classes?", a: "It ensures that each student receives individualized attention, nurturing both technical skills and artistic expression." },
        { q: "Are there opportunities to learn directly from renowned gurus?", a: "Yes, we regularly host workshops and masterclasses with esteemed gurus in the dance community." }
      ]
    },
    {
      category: "Access to Adavus Folder",
      questions: [
        { q: "What is the Adavus folder?", a: "The Adavus folder is a curated collection of essential dance steps (adavus) used for mastering classical techniques." },
        { q: "Who can access the Adavus folder?", a: "Access is granted exclusively to registered students for practice and self-study." },
        { q: "How do I access the Adavus folder?", a: "Upon enrollment, your permissions are approved to access Adavus folder." }
      ]
    },
    {
      category: "Class Policies",
      questions: [
        { q: "Do you offer trial classes?", a: "Yes, trial classes are available upon request." },
        { q: "What should I wear for a class?", a: "Wear comfortable dancewear. Offline Bharatanatyam students must order NatyaShastra uniform using 'Order' section in Natyashatra website." },
        { q: "Is there a cancellation or refund policy?", a: "CANCELLATION OR REFUND NOT ALLOWED" }
      ]
    },
    {
      category: "Events & Performances",
      questions: [
        { q: "Will I have opportunities to perform?", a: "Yes! We organize events where students can showcase their skills. See upcoming events and participants on the Event page." },
        { q: "Where can I view event galleries and performance videos?", a: "Visit the Gallery page to see photos, videos, and details from our events." },
        { q: "How are these events organized?", a: "Events are organized by our team in collaboration with local cultural organizations and are announced on our Event page and social media channels." },
        { q: "Can I participate if I'm a new student?", a: "Participation is based on skill level and readiness. New students may be encouraged to join after an initial period of training decided by the Guru." }
      ]
    },
    {
      category: "Curriculum at a Glance",
      questions: [
        { q: "What does the curriculum cover?", a: "Our curriculum covers foundational adavus, advanced techniques, performance skills, and theoretical aspects of dance." },
        { q: "Is the curriculum structured by level?", a: "Yes, it is divided as per Grade levels starting from Pre-grade till Grade 8 for progressive learning." },
        { q: "Where can I see the curriculum details?", a: "Once onboarded, students must purchase NatyaShastra Grade book which gives curriculum in detail for that respective grade." }
      ]
    },
    {
      category: "Summer Camp",
      questions: [
        { q: "Do you offer a summer camp?", a: "Yes, we host a summer camp that combines intensive dance training with fun activities, workshops, and performance opportunities." },
        { q: "Who can attend the summer camp?", a: "The camp is open to students of all levels, designed to boost both technique and confidence." },
        { q: "How do I register for the summer camp?", a: "Registration must be done on or before April using our Onboard or Enquiry pages. For existing students, no separate registration required." },
        { q: "What are summer camp durations and What do i learn?", a: "Summer camp usually happens in between April & June, where students will learn dance items. These performances will provide them opportunities to showcase their skills at various events throughout the year." }
      ]
    },
    {
      category: "Grade Examination Eligibility and Certification",
      questions: [
        { q: "What are the grade examination requirements?", a: "Grade examinations assess proficiency in dance techniques based on attendance, progress, and performance. See the Exam page for details." },
        { q: "Who is eligible for grade examinations?", a: "Eligibility is determined by our instructors based on each student's progress and performance. The Exam page lists eligible candidates." },
        { q: "What certifications do you offer?", a: "Successful candidates receive recognized certifications that reflect their proficiency in dance after their Salangai Pooja." },
        { q: "How can I apply for a grade examination?", a: "Applications are accepted through our Exam page or directly at our studio after an internal review." }
      ]
    },
    {
      category: "Contact & Support",
      questions: [
        { q: "What qualifications do your instructors have?", a: "Our instructors are professionally trained and have extensive experience in dance." },
        { q: "How can I get more information or ask further questions?", a: "Visit the 'Enquiry' page to contact us or join our WhatsApp group." }
      ]
    }
  ];

  return (
    <div className="enquiry-bg">
      <div className="enquiry-content">
        <h2>Join the WhatsApp group & Enquiry Now</h2>
        <p>Want to know more? Join the group & message us. (Provide student name, age, place)</p>
        <a href="https://chat.whatsapp.com/HxXDfnafyFO6ykxdN97DYi" className="btn" target="_blank" rel="noopener noreferrer">
          Enquire Now
        </a>

        {/* Event Section */}
        <section className="enquiry-section">
          <h3>Events</h3>
          <p>See upcoming events, dates, venues, and participants below or visit the <Link to="/event">Event page</Link> for more details.</p>
        </section>

        {/* Exam Section */}
        <section className="enquiry-section">
          <h3>Exams</h3>
          <p>Find out how to apply for exams, eligibility, and candidate lists below or visit the <Link to="/exam">Exam page</Link> for more details.</p>
        </section>

        <h3>Frequently Asked Questions (FAQ)</h3>
        <div className="faq-section">
          {faqData.map((categoryData, index) => (
            <div key={index} className="faq-category">
              <h4 className="faq-category-title" onClick={() => toggleCategory(categoryData.category)}>
                {categoryData.category} {openCategory === categoryData.category ? "▲" : "▼"}
              </h4>
              {openCategory === categoryData.category && (
                <ul className="faq-list">
                  {categoryData.questions.map((item, idx) => (
                    <li key={idx} className="faq-item">
                      <strong>{item.q}</strong>
                      {/* Render answer as HTML to support anchor tags */}
                      <p dangerouslySetInnerHTML={{ __html: item.a }} />
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
