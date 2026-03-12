import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

type ResultData = {
  requestId: string;
  stepId: string | null;
  summary: string;
  issues: { type: string; message: string; severity: string }[];
  annotationsUrl: string | null;
};

export default function Result() {
  const { requestId } = useParams<{ requestId: string }>();
  const [data, setData] = useState<ResultData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!requestId) return;

    axios
      .get<ResultData>(`/api/results/${requestId}`)
      .then((res) => setData(res.data))
      .catch(() => setError("Unable to fetch analysis results."));
  }, [requestId]);

  if (error) {
    return (
      <main className="page">
        <h1>Error</h1>
        <p>{error}</p>
      </main>
    );
  }

  if (!data) {
    return (
      <main className="page">
        <h1>Loading results…</h1>
      </main>
    );
  }

  return (
    <main className="page">
      <h1>Analysis Results</h1>
      <p>{data.summary}</p>

      <section>
        <h2>Issues</h2>
        <ul>
          {data.issues.map((issue, idx) => (
            <li key={idx}>
              <strong>{issue.type}</strong>: {issue.message}
            </li>
          ))}
        </ul>
      </section>

      {data.annotationsUrl && (
        <section>
          <h2>Annotated Video</h2>
          <video controls width={480} src={data.annotationsUrl} />
        </section>
      )}
    </main>
  );
}
