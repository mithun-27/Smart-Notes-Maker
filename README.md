
# 🧠 Smart Notes Maker  
### Summarize PDFs, YouTube Lectures, and Text Notes into Bullet Points + Auto-Generated Quiz Questions

Smart Notes Maker is an **AI-powered note system** that extracts text from **PDFs**, **YouTube transcripts**, or **raw lecture notes**, and automatically produces:

✔ Bullet-point summaries  
✔ Auto-generated quiz questions  
✔ Clean & interactive web UI  
✔ Fully offline processing (no API keys needed)

---

## 🚀 Features

### 🔍 Multi-input Support
- **Upload PDF files**
- **Paste YouTube video URL** (fetches caption transcript)
- **Paste raw lecture text**

### 🤖 Smart Processing
- Summarizes long text into clear bullet points  
- Generates quiz questions based on summary  
- Works **offline** using Python NLP heuristics  
- No external API or LLM required

### 🎨 Beautiful Frontend (HTML + CSS + JS)
- Interactive tabs (Text / PDF / YouTube)
- Smooth animations & modern gradients  
- “Show Answer” quiz reveal toggles  

### 🧩 Modular Backend
Backend built using:
- **Flask**
- **youtube-transcript-api**
- **PyPDF2**
- **Custom summarizer + quiz generator**

---

## 📂 Project Structure

```

smart-notes-maker/
│
├── backend/
│   ├── app.py
│   ├── summarizer.py
│   ├── quiz_generator.py
│   ├── pdf_utils.py
│   ├── youtube_utils.py
│   └── requirements.txt
│
└── frontend/
├── index.html
├── style.css
└── script.js

````

---

## ⚙️ Installation & Setup (Windows)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/smart-notes-maker.git
cd smart-notes-maker/backend
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Backend Server

```bash
python app.py
```

Backend will start on:

```
http://127.0.0.1:5000
```

### 5️⃣ Run the Frontend

Simply open:

```
frontend/index.html
```

in any browser (Chrome recommended).

---

## 🧪 How to Use

### **⭐ Text Mode**

Paste any long text → click **Generate Smart Notes**.

### **⭐ PDF Mode**

Upload any PDF (lecture notes, papers, books).

### **⭐ YouTube Mode**

Paste a YouTube URL (must have English captions enabled).

---

## 💡 Tech Stack

### **Frontend**

* HTML
* CSS (custom modern UI)
* JavaScript (fetch API + interactivity)

### **Backend**

* Python
* Flask
* PyPDF2
* youtube-transcript-api
* Custom NLP logic

---

## 📌 Screenshot Area

### 1️⃣ Text/Notes:
<img width="1916" height="874" alt="Screenshot 2025-12-12 115342" src="https://github.com/user-attachments/assets/0d9a8893-7924-425f-958a-46c9403506d1" />

### 2️⃣ PDF upload:
<img width="1909" height="873" alt="Screenshot 2025-12-12 115115" src="https://github.com/user-attachments/assets/9c39be03-8848-4c19-af32-ba7fe51d4161" />

### 3️⃣ YouTube Transcript :
<img width="1917" height="870" alt="Screenshot 2025-12-12 115200" src="https://github.com/user-attachments/assets/c58b8cad-8421-4196-95b5-5f7f9f52b1cc" />

---

## 🛠 Future Improvements (Optional)

* LLM-powered summarization (OpenAI / Gemini)
* Database for saving notes
* User authentication
* Dark/light theme toggle

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first.

---


## ✨ Author

**Mithun S**
AI/ML Developer | Content Writer | Fullstack Learner

---

Happy Learning! 🚀
If you like this project, don't forget to ⭐ the repo!
