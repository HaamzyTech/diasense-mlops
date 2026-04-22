interface PageProps {
  params: { requestId: string };
}

export default function ResultPage({ params }: PageProps) {
  return (
    <main>
      <h1>Prediction Result</h1>
      <p>Request ID: {params.requestId}</p>
      <p>TODO: Render result details from backend-api.</p>
    </main>
  );
}
