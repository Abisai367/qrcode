import React, { useState } from "react";
import "./home.css";

export default function Home() {
  const [preferredName, setPreferredName] = useState("");
  const [url, setUrl] = useState("");
  const [qrCode, setQrCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [color, setColor] = useState("");

  const generate = async (event) => {
    event?.preventDefault();
    const trimmedUrl = url.trim();

    if (!trimmedUrl) {
      alert("Please enter a URL to generate a QR code.");
      return;
    }

    const formData = new FormData();
    formData.append("url", trimmedUrl);
    formData.append("image_name", preferredName.trim());

    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Unable to generate QR code.");
      }

      const blob = await response.blob();
      const qrCodeUrl = URL.createObjectURL(blob);
      setQrCode(qrCodeUrl);
    } catch (error) {
      console.error("Error generating QR code:", error);
      alert(error.message || "Error generating QR code.");
    } finally {
      setLoading(false);
    }
  };

  const downloadQrCode = () => {
    if (!qrCode) {
      alert("Please generate a QR code first.");
      return;
    }

    const link = document.createElement("a");
    link.href = qrCode;
    link.download = preferredName.trim() ? `${preferredName.trim()}.png` : "qrcode.png";
    link.click();
  };

  return (
    <div className="home">
      <div className="page">
        <section className="hero-card card">
          <div>
            <p className="eyebrow">QR Code Studio</p>
            <h1>Generate and download QR codes instantly.</h1>
            <p className="hero-copy">
              Enter any URL, choose a filename, and create a polished QR image you can save or share.
            </p>
          </div>
        </section>

        <div className="content-grid">
          <section className="generator-card card">
            <div className="section-header">
              <h2>Create QR Code</h2>
              <p>Fast, reliable, and ready for download.</p>
            </div>

            <form className="form-grid" onSubmit={generate}>
              <label htmlFor="url">Website URL</label>
              <input
                id="url"
                type="url"
                placeholder="https://www.example.com"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
              />

              <label htmlFor="preferredName">Image filename</label>
              <input
                id="preferredName"
                type="text"
                placeholder="my-qr-code"
                value={preferredName}
                onChange={(e) => setPreferredName(e.target.value)}
              />
              <label htmlFor="color">Color (optional)</label>
              <input
                id="color"
                type="color"
                value={color}
                onChange={(e) => setColor(e.target.value)}
              />

              <button className="primary-button" type="submit" disabled={loading}>
                {loading ? "Generating..." : "Generate QR code"}
              </button>
            </form>
          </section>

          <aside className="preview-card card">
            <div className="section-header">
              <h2>Preview</h2>
              <p>Your generated QR code will appear here.</p>
            </div>

            <div className="output">
              <div className="preview-box">
                {qrCode ? (
                  <img src={qrCode} alt="Generated QR Code" />
                ) : (
                  <p className="preview-placeholder">Generate a QR code to preview it here.</p>
                )}
              </div>

              <button
                className="secondary-button"
                type="button"
                onClick={downloadQrCode}
                disabled={!qrCode}
              >
                Download QR Code
              </button>
            </div>
          </aside>
        </div>

        <footer className="footer-card card">
          <div>
            <p className="footer-title">Need help in Designing Websites?</p>
            <p className="footer-copy">
              I am a passionate web developer and I will help you build your website. Reach out to me via email for inquiries.
            </p>
          </div>
          <div className="footer-meta">
            <span>Developer ABISAI</span>
            <a href="mailto:webdevabisai@gmail.com">webdevabisai@gmail.com</a>
          </div>
        </footer>
      </div>
    </div>
  );
}
