import { useState, useRef } from "react";
import { startJob, pollUntilComplete } from "../api/adforgeClient";
import "./Dashboard.css";

export default function Dashboard() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
        setPreview(reader.result);
        setResult(null);
        setError(null);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
        setPreview(reader.result);
        setResult(null);
        setError(null);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async () => {
    if (!image) return;

    setStatus("uploading");
    setError(null);
    setResult(null);
    setProgress(10);

    try {
      const { jobId } = await startJob(image);
      setStatus("processing");
      
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress((p) => Math.min(p + 5, 90));
      }, 2000);

      const data = await pollUntilComplete(jobId);
      clearInterval(progressInterval);
      setProgress(100);
      setResult(data);
      setStatus("complete");
    } catch (err) {
      setError(err.message);
      setStatus("error");
      setProgress(0);
    }
  };

  const isProcessing = status === "uploading" || status === "processing";

  return (
    <div className="dashboard">
      <div className="dashboard-grid">
        {/* Upload Section */}
        <div className="card upload-card">
          <h2 className="card-title">
            <span className="icon">📸</span> Upload Product
          </h2>
          
          <div
            className={`dropzone ${preview ? "has-image" : ""}`}
            onClick={() => fileInputRef.current?.click()}
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              hidden
            />
            
            {preview ? (
              <img src={preview} alt="Preview" className="preview-image" />
            ) : (
              <div className="dropzone-content">
                <div className="dropzone-icon">🖼️</div>
                <p className="dropzone-text">Drop your image here</p>
                <p className="dropzone-hint">or click to browse</p>
              </div>
            )}
          </div>

          <button
            className={`generate-btn ${isProcessing ? "processing" : ""}`}
            onClick={handleSubmit}
            disabled={!image || isProcessing}
          >
            {isProcessing ? (
              <>
                <span className="spinner"></span>
                {status === "uploading" ? "Uploading..." : "Creating Magic..."}
              </>
            ) : (
              <>🚀 Generate Ad</>
            )}
          </button>

          {isProcessing && (
            <div className="progress-container">
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${progress}%` }}></div>
              </div>
              <p className="progress-text">{progress}% - Crafting your ad...</p>
            </div>
          )}

          {error && (
            <div className="error-message">
              <span>⚠️</span> {error}
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="card results-card">
          <h2 className="card-title">
            <span className="icon">🎬</span> Your Ad
          </h2>

          {!result && !isProcessing && (
            <div className="empty-state">
              <div className="empty-icon">🎥</div>
              <p>Your generated ad will appear here</p>
              <p className="empty-hint">Upload an image to get started</p>
            </div>
          )}

          {isProcessing && (
            <div className="generating-state">
              <div className="pulse-ring"></div>
              <div className="generating-icon">✨</div>
              <p>AI is working its magic...</p>
              <div className="generating-steps">
                <div className={`step ${progress > 10 ? "active" : ""}`}>Analyzing image</div>
                <div className={`step ${progress > 30 ? "active" : ""}`}>Writing script</div>
                <div className={`step ${progress > 50 ? "active" : ""}`}>Generating voiceover</div>
                <div className={`step ${progress > 70 ? "active" : ""}`}>Creating visuals</div>
                <div className={`step ${progress > 90 ? "active" : ""}`}>Assembling ad</div>
              </div>
            </div>
          )}

          {result && (
            <div className="result-content">
              {/* Hero Image */}
              <div className="result-hero">
                <img src={result.imageUrl} alt="Generated Ad" className="hero-image" />
                <div className="hero-overlay">
                  <span className="badge">AI Generated</span>
                </div>
              </div>

              {/* Audio Player */}
              <div className="audio-section">
                <h3><span>🔊</span> Voiceover</h3>
                <audio controls src={result.audioUrl} className="audio-player" />
              </div>

              {/* Script */}
              <div className="script-section">
                <h3><span>📝</span> Ad Script</h3>
                <div className="script-content">
                  {result.script}
                </div>
              </div>

              {/* Actions */}
              <div className="result-actions">
                <button className="action-btn primary" onClick={() => window.open(result.imageUrl)}>
                  ⬇️ Download Image
                </button>
                <button className="action-btn secondary" onClick={() => window.open(result.audioUrl)}>
                  🎵 Download Audio
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
