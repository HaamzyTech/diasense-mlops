export default function HomePage() {
  return (
    <main className="container">
      <section className="card">
        <h1>DiaSense Diabetes Risk Assistant</h1>
        <p>A simple tool to submit diabetes risk inputs and review the model output.</p>
        <p>
          Start at <a href="/predict">Predict</a> or review operational status at <a href="/ops">Ops</a>.
        </p>
      </section>
    </main>
  );
}
