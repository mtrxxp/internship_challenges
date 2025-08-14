import React, { useState, useEffect } from "react";
import "./adminpage.css";

function Scrabber() {
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState("idle");
  const [message, setMessage] = useState("");
  const [csvFiles, setCsvFiles] = useState([]);

  const startScrape = async () => {
    setStatus("pending");
    setMessage("🔄 Scraping started...");
    setCsvFiles([]);

    try {
      const response = await fetch("/start_scrape", { method: "POST" });
      if (!response.ok) throw new Error("Failed to start scraping");
      const data = await response.json();
      setTaskId(data.task_id);
    } catch (error) {
      setStatus("error");
      setMessage("❌ Failed to start scraping.");
    }
  };

  const stopScrape = async () => {
    try {
      const res = await fetch("/stop_scrape", { method: "POST" });
      if (!res.ok) throw new Error("Failed to stop scraping");
      await res.json();

      setStatus("stopped");
      setMessage("🛑 Scraper stopped. CSV files are ready for download.");
      fetchCsvFiles();
    } catch {
      setMessage("❌ Failed to stop scraping.");
    }
  };

  const fetchCsvFiles = async () => {
    try {
      const res = await fetch("/csv_files");
      if (!res.ok) throw new Error("Failed to fetch CSV files");
      const files = await res.json();
      setCsvFiles(files);
    } catch {
      setMessage("⚠ Не удалось загрузить список CSV-файлов.");
    }
  };

  useEffect(() => {
    if (!taskId || status !== "pending") return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`/scrape_status/${taskId}`);
        if (!res.ok) throw new Error("Failed to fetch status");

        const data = await res.json();
        const scrapeStatus = data.status;

        if (scrapeStatus === "completed") {
          setStatus("success");
          setMessage("✅ Scraping completed!");
          fetchCsvFiles();
          clearInterval(interval);
        } else if (scrapeStatus === "failed") {
          setStatus("error");
          setMessage("❌ Scraping failed.");
          clearInterval(interval);
        }
      } catch {
        setStatus("error");
        setMessage("❌ Error fetching status.");
        clearInterval(interval);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [taskId, status]);

  return (
    <div className="scrabber-container">
      <h2>
        YouTube Channel Scraper
      </h2>

      <div className="button-group">
        <button
          onClick={startScrape}
          className="btn"
          disabled={status === "pending" || status === "stopping"}
        >
          ▶ Start Scraping
        </button>

        <button
          onClick={stopScrape}
          className="btn stop-btn"
          disabled={status !== "pending"}
        >
          🛑 Stop Scraping
        </button>
      </div>

      <p className="scrape-status">
        {message}
        {status === "pending" && <span className="loader"></span>}
      </p>

      {(status === "success" || status === "stopped") && csvFiles.length > 0 && (
        <div className="csv-list">
          <h4>📁 Available CSV Files</h4>
          <ul>
            {csvFiles.map((filename, idx) => (
              <li key={idx}>
                <a
                  href={`/download_csv/${filename}`}
                  className="btn small-btn"
                  download
                >
                  ⬇ {filename}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Scrabber;
