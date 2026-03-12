import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Analyze() {
  const [status, setStatus] = useState("Processing...");
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/");
    }, 4000);
    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <main className="page">
      <h1>Analyzing video</h1>
      <p>{status}</p>
      <p>Please wait while we prepare your feedback.</p>
    </main>
  );
}
