<div align="center">
  <h1>🎬 AI Content Studio (Major Update)</h1>
  <p><strong>The World's Best Open-Source AI Video & Podcast Generator</strong></p>
  
  [![YouTube](https://img.shields.io/badge/Subscribe_on-YouTube-FF0000?style=for-the-badge&logo=youtube)](https://www.youtube.com/@naqashai)
  [![Patreon](https://img.shields.io/badge/Support_on-Patreon-f96854?style=for-the-badge&logo=patreon)](https://www.patreon.com/c/naqashafzal)
  [![Instagram](https://img.shields.io/badge/Follow_on-Instagram-E4405F?style=for-the-badge&logo=instagram)](https://www.instagram.com/naqashafzal/)
  ![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
</div>

---

**AI Content Studio** is the ultimate, fully-automated platform designed to generate viral social media content at the click of a button. Whether you want to generate full AI-powered video podcasts from scratch or automatically extract viral TikToks from long-form YouTube videos, AI Content Studio provides a sleek, unified dashboard to manage your entire content pipeline.

If you love this project and want to support its development, please consider helping out on **[Patreon](https://www.patreon.com/c/naqashafzal)** or follow my journey on **[Instagram](https://www.instagram.com/naqashafzal/)**!

## 🌟 Key Features (Next-Gen v2.0 Studio)

AI Content Studio has been completely upgraded into an advanced, autonomous AI creative production and video editing platform:

### 🎬 Autonomous AI Director & Visual Storyboard
- **Supervisory AI Orchestrator:** Dynamic agent team (`StrategyAgent`, `TrendDiscoveryAgent`, `ResearchAgent`, `CreativeDirectorAgent`, `QualityAssuranceAgent`, `LearningAgent`).
- **Self-Healing QA Retry Loops:** Automatically critiques generated scripts. If QA score is below 80, the director autonomously rewrites weak scenes based on actionable critique before initiating renders.
- **Interactive Scene Cards & Selective Regeneration:** Lock approved scenes while selectively regenerating individual scenes with custom user instructions (e.g. *"Change to a drone wide establishing shot"*).

### ✂️ Magic AI Clipper 2.0 (Multimodal OpusClip Engine)
- **Multimodal Hotspot Fusion:** Combines Whisper transcriptions with **audio RMS volume peaks** (detecting vocal excitement, applause, punchlines) and **OpenCV HSV histogram cuts** to score and rank clips on genuine audio-visual virality.
- **Active Speaker Framing with Hysteresis:** Face detection with intelligent shot hysteresis (minimum 1.5s interval) prevents camera shaking and jitter on minor head movements.
- **B-Roll Auto-Injection:** Automatically pulls topic-relevant visual B-roll from Pixabay for high-retention visual pacing.

### 🎨 Intelligent Style Engine & Reference Video Cloner
- **Clone Editing Styles:** Upload any reference video from creators like MrBeast, Alex Hormozi, or Vox. The engine uses computer vision to extract shot durations, cut frequency, and caption animations into reusable style profiles.
- **Live Brand Kit Studio:** Real-time 9:16 short preview with custom dual-accent color palettes, typography options, watermark placement/opacity, and stinger intros.

### 🔊 Studio Audio Mastering & Urdu / Roman Urdu Support
- **Broadcast Loudness Normalization:** Integrated FFmpeg EBU R128 `loudnorm=I=-14:TP=-1.5:LRA=11` filter across video renders, aligning output with YouTube and TikTok broadcast targets.
- **Phonetic Normalization:** Full Urdu Unicode character normalization and Roman Urdu phonetic dictionary (e.g. *kese -> kaisay*, *kyun -> kyoon*, *mujhe -> mujhey*, *dunya -> duniya*) for natural neural TTS pronunciation.

### ⚡ Resilient SQLite Queue & Multi-Model Gateway
- **Persistent Durable Queue:** Tasks survive server restarts; recovers interrupted rendering jobs with stage-by-stage checkpoints.
- **Multi-Model Routing:** Unified provider gateway supporting Google Gemini, OpenAI-compatible APIs, and local Ollama with automatic failover.
- **Zero Mock Exploits:** Real OAuth token management and manual publishing packages.

## 🔋 How to Use Tutorial
🔥 **NEW FULL DETAILED VIDEO TUTORIAL COMING SOON!** 🔥
A complete step-by-step video for this massively updated version is currently in the works. Make sure to **[Subscribe to our YouTube Channel (@naqashai)](https://www.youtube.com/@naqashai)** so you don't miss it when it drops!

**Old Version References:**
- If you are looking for the original codebase, you can find the old version safely stored in the GitHub Commits History.
- 👉 **<a href="https://youtu.be/9JpSs57RjbY?si=5ihW2Pl_JFtwAz45">Watch the Old Version Video Tutorial</a>**

---

## 🛠️ Tech Stack & Architecture

Built with a modern, high-performance tech stack designed for speed and scalability:

### Frontend (Web UI)
- **Framework:** Next.js (React)
- **Styling:** Tailwind CSS + Glassmorphism UI
- **Icons:** Lucide React
- **Real-time Engine:** WebSockets for live pipeline logging and progress bars

### Backend (API Engine)
- **Server:** FastAPI (Python)
- **Video Processing:** FFmpeg (Core requirement for slicing, cropping, and caption burning)
- **Downloading:** `yt-dlp` (For bypassing YouTube blocks and downloading media)
- **Transcription:** OpenAI Whisper (Local, offline audio-to-text transcription)
- **Subtitles:** `pysubs2` (For generating and styling `.ass` subtitle files)
- **AI Brain:** Google Gemini API (For content curation, logic, and script writing)

---

## 🚀 Getting Started

### Prerequisites
Before running the application, ensure you have the following installed on your system:
1. **Python 3.10+**
2. **Node.js (v18+)** & npm
3. **FFmpeg** (Must be installed and added to your system's PATH variable)
4. A **Google Gemini API Key** (Set via the UI Settings tab)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/naqashafzal/AI-Content-Studio.git
   cd AI-Content-Studio
   ```

2. **Setup the Python Backend:**
   ```bash
   # Create a virtual environment
   python -m venv .venv
   
   # Activate it (Windows)
   .venv\Scripts\activate
   # Activate it (Mac/Linux)
   source .venv/bin/activate
   
   # Install backend dependencies
   pip install -r requirements.txt
   
   # Important Note: If you face issues with file uploads, ensure python-multipart is installed
   pip install python-multipart
   ```

3. **Setup the Next.js Frontend:**
   ```bash
   cd web
   npm install
   ```

### Running the Application

#### ⚡ 1-Click Launch (Windows - Recommended)
Simply run or double-click **`start.bat`**:
```cmd
start.bat
```
The automated launcher will verify Python 3.10+, Node.js 18+, and FFmpeg, initialize storage folders, activate `.venv`, check dependencies, launch both server consoles, and automatically open your browser to `http://localhost:3000`!

#### 🛠️ Manual Launch (All Platforms)
You can run both servers manually in separate terminal windows:

**1. Start the Backend API (from the root directory):**
```bash
python server/main.py
# The FastAPI server will run on http://localhost:8008
```

**2. Start the Frontend UI (from the `/web` directory):**
```bash
npm run dev
# The Next.js app will run on http://localhost:3000
```

Open your browser and navigate to `http://localhost:3000` to start creating!

---

## 🤝 Support & Connect

Building and maintaining this open-source project takes a lot of time and effort! If this tool has helped you grow your channels, automate your workflows, or make money, please consider supporting me:

- 💖 **Support on Patreon:** [patreon.com/c/naqashafzal](https://www.patreon.com/c/naqashafzal)
- 📸 **Follow on Instagram:** [@naqashafzal](https://www.instagram.com/naqashafzal/)

Your support helps me keep updating the tool, adding new AI features, and keeping the core open-source for everyone!

---

## ⚠️ Troubleshooting

- **Clipper Audio is out of sync:** Ensure you are using the latest backend code. We force `-c:a aac` during FFmpeg extraction to prevent audio PTS drift.
- **0.00s Clips generated:** This means the AI couldn't read the timestamps. Ensure `pipeline_shorts.py` is formatting the transcript chunks with `[start - end]` brackets.
- **FFmpeg errors / "Subtitles not found":** Ensure FFmpeg is installed globally on your machine and that `ffmpeg` is a recognized terminal command.

## 📄 License
This project is licensed under the MIT License.
