import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DiaSense",
  description: "Diabetes risk support",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="container nav">
          <a href="/">DiaSense</a>
          <nav>
            <a href="/predict">Predict</a>
            <a href="/ops">Ops</a>
            <a href="/help">Help</a>
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
