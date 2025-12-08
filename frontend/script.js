// frontend/script.js

const BASE_URL = "http://127.0.0.1:5000";

// Tab switching
const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(".tab-content");

tabButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    tabButtons.forEach((b) => b.classList.remove("active"));
    tabContents.forEach((tc) => tc.classList.remove("active"));
    btn.classList.add("active");
    const tabId = btn.getAttribute("data-tab");
    document.getElementById(tabId).classList.add("active");
    clearResults();
  });
});

// Elements
const textInput = document.getElementById("text-input");
const processTextBtn = document.getElementById("process-text-btn");

const pdfInput = document.getElementById("pdf-input");
const processPdfBtn = document.getElementById("process-pdf-btn");

const youtubeInput = document.getElementById("youtube-url-input");
const processYoutubeBtn = document.getElementById("process-youtube-btn");

const loader = document.getElementById("loader");
const statusMessage = document.getElementById("status-message");

const resultsSection = document.getElementById("results-section");
const summaryList = document.getElementById("summary-list");
const quizContainer = document.getElementById("quiz-container");

function showLoader(message) {
  loader.classList.remove("hidden");
  statusMessage.textContent = message || "Processing...";
}

function hideLoader() {
  loader.classList.add("hidden");
}

function showError(msg) {
  statusMessage.textContent = msg;
  statusMessage.style.color = "#fecaca";
}

function showInfo(msg) {
  statusMessage.textContent = msg;
  statusMessage.style.color = "#e5e7eb";
}

function clearResults() {
  resultsSection.classList.add("hidden");
  summaryList.innerHTML = "";
  quizContainer.innerHTML = "";
  showInfo("");
}

// Render summary + quiz
function renderResults(data) {
  summaryList.innerHTML = "";
  quizContainer.innerHTML = "";

  if (data.summary && data.summary.length) {
    data.summary.forEach((point) => {
      const li = document.createElement("li");
      li.textContent = point;
      summaryList.appendChild(li);
    });
  } else {
    const li = document.createElement("li");
    li.textContent = "No summary generated.";
    summaryList.appendChild(li);
  }

  if (data.quiz && data.quiz.length) {
    data.quiz.forEach((q) => {
      const card = document.createElement("div");
      card.className = "quiz-item";

      const questionP = document.createElement("p");
      questionP.className = "quiz-question";
      questionP.textContent = q.question;

      const btn = document.createElement("button");
      btn.className = "toggle-answer-btn";
      btn.textContent = "Show Answer";

      const answerP = document.createElement("p");
      answerP.className = "quiz-answer";
      answerP.textContent = q.answer;

      btn.addEventListener("click", () => {
        const isVisible = answerP.style.display === "block";
        answerP.style.display = isVisible ? "none" : "block";
        btn.textContent = isVisible ? "Show Answer" : "Hide Answer";
      });

      card.appendChild(questionP);
      card.appendChild(btn);
      card.appendChild(answerP);
      quizContainer.appendChild(card);
    });
  } else {
    const card = document.createElement("div");
    card.className = "quiz-item";
    card.textContent = "No quiz questions generated.";
    quizContainer.appendChild(card);
  }

  resultsSection.classList.remove("hidden");
}

// Handlers
processTextBtn.addEventListener("click", async () => {
  const text = textInput.value.trim();
  if (!text) {
    showError("Please paste some text first.");
    return;
  }

  clearResults();
  showLoader("Summarizing your notes and generating quiz...");

  try {
    const res = await fetch(`${BASE_URL}/api/from-text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const data = await res.json();
    hideLoader();

    if (!res.ok) {
      showError(data.error || "Something went wrong.");
      return;
    }

    showInfo("Done! Scroll down to see your Smart Notes.");
    renderResults(data);
  } catch (err) {
    hideLoader();
    showError("Failed to reach backend. Is the server running?");
    console.error(err);
  }
});

processPdfBtn.addEventListener("click", async () => {
  const file = pdfInput.files[0];
  if (!file) {
    showError("Please choose a PDF file first.");
    return;
  }

  clearResults();
  showLoader("Uploading PDF and generating Smart Notes...");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${BASE_URL}/api/from-pdf`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    hideLoader();

    if (!res.ok) {
      showError(data.error || "Something went wrong while processing PDF.");
      return;
    }

    showInfo("Done! Scroll down to see your Smart Notes.");
    renderResults(data);
  } catch (err) {
    hideLoader();
    showError("Failed to reach backend. Is the server running?");
    console.error(err);
  }
});

processYoutubeBtn.addEventListener("click", async () => {
  const url = youtubeInput.value.trim();
  if (!url) {
    showError("Please paste a YouTube URL.");
    return;
  }

  clearResults();
  showLoader("Fetching transcript and generating Smart Notes...");

  try {
    const res = await fetch(`${BASE_URL}/api/from-youtube`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    const data = await res.json();
    hideLoader();

    if (!res.ok) {
      showError(data.error || "Something went wrong while fetching transcript.");
      return;
    }

    showInfo("Done! Scroll down to see your Smart Notes.");
    renderResults(data);
  } catch (err) {
    hideLoader();
    showError("Failed to reach backend. Is the server running?");
    console.error(err);
  }
});
