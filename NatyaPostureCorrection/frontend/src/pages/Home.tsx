import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

type Step = {
  id: string;
  name: string;
  description: string;
  referenceVideoUrl: string;
};

export default function Home() {
  const [steps, setSteps] = useState<Step[]>([]);
  const [selectedStep, setSelectedStep] = useState<string>("");
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get<Step[]>("/api/steps").then((res) => {
      setSteps(res.data);
      if (res.data.length > 0) {
        setSelectedStep(res.data[0].id);
      }
    });
  }, []);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!videoFile) return;

    setSubmitting(true);

    const formData = new FormData();
    formData.append("student_video", videoFile);
    formData.append("step_id", selectedStep);

    try {
      const res = await axios.post("/api/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      navigate(`/result/${res.data.requestId}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="page">
      <h1>Natya Posture Correction</h1>
      <p>Select a step and upload your performance video.</p>

      <form onSubmit={handleSubmit} className="form">
        <label>
          Step
          <select
            value={selectedStep}
            onChange={(e) => setSelectedStep(e.target.value)}
          >
            {steps.map((step) => (
              <option key={step.id} value={step.id}>
                {step.name}
              </option>
            ))}
          </select>
        </label>

        {steps.length > 0 && (
          <div className="reference-video">
            <h2>Reference video</h2>
            <video
              controls
              width={360}
              src={steps.find((s) => s.id === selectedStep)?.referenceVideoUrl}
            />
          </div>
        )}

        <label>
          Your video (5–10 seconds)
          <input
            type="file"
            accept="video/*"
            onChange={(e) => setVideoFile(e.target.files?.[0] ?? null)}
          />
        </label>

        <button type="submit" disabled={!videoFile || submitting}>
          {submitting ? "Uploading…" : "Analyze"}
        </button>
      </form>
    </main>
  );
}
