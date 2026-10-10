# CareerLearn AI

An AI-powered learning assistant that identifies your skill gaps for your target career, explains missing concepts, connects them to real-world applications, and gives you practical tasks to learn by doing.

Built for **ForgeHacks 2026** (AI + Education Track).

## Problem

Learners often struggle to connect theoretical knowledge to real-world career applications. They know *what* to learn, but not *why* it matters or *how* to apply it, keeping them in tutorial hell.

## Solution

CareerLearn AI goes beyond basic course recommendation. It analyzes your current skills against a target career, identifies your gaps, and generates a personalized learning plan that emphasizes:
1. **Understand** (What is this concept and why do I need it?)
2. **Connect** (How does this specifically apply to the target career?)
3. **Apply** (A practical, hands-on task to solidify the concept.)

## Features

- **Skill Gap Analysis**: Compare current skills with expected career standards.
- **LLM-Powered Explanations**: Uses AI to generate clear, concise details about any missing technical skill.
- **Career Connection**: Explains *why* the skill matters in the professional world.
- **Application Tasks**: Generates small, doable coding/analysis tasks for immediate practice.
- **Dynamic Roadmap**: Progress-tracker to map out the learning journey (uses `localStorage` - no signups required!)
- **Fallback Content**: Built-in offline definitions ensuring 100% uptime for demo purposes even if the LLM API limit is reached.

## Tech Stack

- **Frontend**: React + Vite + TailwindCSS
- **Backend**: Python + FastAPI
- **Data/Progress**: LocalJSON Configuration + LocalStorage
- **AI Integration**: Prepared for any generic LLM via API (simulated/offline fallbacks included out of the box).

## Setup & Run Instructions

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# Activate venv:
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate
pip install -r requirements.txt # (or fast-install via: pip install fastapi uvicorn pydantic python-dotenv httpx)
```

Create a `.env` file in the `backend/` directory referencing `.env.example`:
```ini
LLM_API_KEY=your_key_here
```

Start the API:
```bash
uvicorn main:app --reload --port 8000
```
*API will run at `http://localhost:8000`*

### 2. Frontend Setup

Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
*App will run at `http://localhost:5173`*

## Demo Flow
1. Start on the Landing Page.
2. Select your Target Career (e.g., "ML Engineer").
3. Input arbitrary pre-existing skills (e.g., "Python, Machine Learning").
4. Click Analyze Skills to enter the Dashboard.
5. Review the "Top Priority Gaps" visually highlighted on your profile.
6. Click into a missing skill (e.g. "Probability & Statistics") to reveal the AI content, career connections, and recommended practice tasks.
7. Click "Learning" status. Update reflects in Roadmap automatically.

## Limitations & Future Improvements
- Currently relying on static fallback content to guarantee demo reliability. True LLM integration can be easily swapped in `backend/main.py`.
- No database persistence. Everything runs securely on the client machine via `localStorage`. Future iteration would add simple user auth for long-term retention.
- Graph visualization for prerequisite trees are flattened into simplified Roadmaps for speed. 

## What Actually Works
- Full UI navigation (Landing -> Profile -> Dashboard -> Detail -> Roadmap)
- Real gap analysis engine (comparing User inputs against defined Career Models)
- Seamless JSON Payload delivery from FastAPI to React via REST POST `/api/analyze` 
- Client-side persistence on Learning Tracks (`Not Started -> Learning -> Completed`)
- Clean UI matching the "Professional modern AI Education platform" specs using pure React + Tailwind.
