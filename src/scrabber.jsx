import React, { useState, useEffect } from "react";
import "./adminpage.css";

function Scrabber() {
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState("idle");
  const [message, setMessage] = useState("");

  const startScrape = async () => {
    setStatus("pending");
    setMessage("🔄 Scraping started...");

    try {
      const response = await fetch("/start_scrape", {
        method: "POST",
      });

      if (!response.ok) throw new Error("Failed to start scraping");

      const data = await response.json();
      setTaskId(data.task_id);
    } catch (error) {
      setStatus("error");
      setMessage("❌ Failed to start scraping.");
      console.error(error);
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

        if (scrapeStatus === "SUCCESS") {
          setStatus("success");
          setMessage("✅ Scraping completed!");
          clearInterval(interval);
        } else if (scrapeStatus === "FAILURE") {
          setStatus("error");
          setMessage("❌ Scraping failed.");
          clearInterval(interval);
        }
      } catch (error) {
        setStatus("error");
        setMessage("❌ Error fetching status.");
        clearInterval(interval);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [taskId, status]);

  return (
    <div className="scrabber-container">
      <h2>YouTube Channel Scraper</h2>

      <button
        onClick={startScrape}
        className="btn"
        disabled={status === "pending"}
      >
        {status === "pending" ? "Scraping..." : "Start Scraping"}
      </button>

      <p className="scrape-status">
        {message}
        {status === "pending" && (
          <span className="loader" style={{ marginLeft: "10px" }}></span>
        )}
      </p>

      {status === "success" && (
        <a href="/download_csv" className="btn download-btn" download>
          📥 Download CSV
        </a>
      )}
    </div>
  );
}

export default Scrabber;
