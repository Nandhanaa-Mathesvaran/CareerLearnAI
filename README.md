# CareerLearn AI

An AI-powered personalized learning assistant that identifies skill gaps for a target career, explains missing concepts, connects them to real-world applications, and provides practical tasks to help learners move from theory to practice.

**Built for ForgeHacks 2026 — AI + Education Track.**

Video Demo Link: https://drive.google.com/file/d/13T09Mf4767jfmCVh7gnsruSJPlDnu2Ec/view?usp=sharing

## Problem Statement

Learners often struggle to connect theoretical knowledge with real-world career requirements. They may know what to learn but not why a concept matters or how to apply it professionally. This can lead to endless tutorials without meaningful hands-on practice.

## Our Solution

CareerLearn AI helps learners build career-relevant skills through personalized skill-gap analysis and actionable learning guidance.

Users select a target career and enter their existing skills. The platform identifies missing skills and organizes learning guidance into three stages:

1. **Understand:** Learn what a concept means and why it matters.
2. **Connect:** Discover how the concept is used in the selected career.
3. **Apply:** Practice through a small, practical coding or analytical task.

## Key Features

- **Skill Gap Analysis:** Compares a learner's existing skills against the defined requirements of a target career.
- **Concept Explanations:** Provides explanations for missing technical skills using the configured AI integration or available fallback content.
- **Career-Relevant Learning:** Connects concepts to practical professional applications.
- **Hands-on Practice Tasks:** Recommends manageable activities to reinforce learning.
- **Personalized Learning Roadmap:** Organizes identified gaps into a structured learning journey.
- **Progress Tracking:** Tracks learning status from Not Started to Learning to Completed.
- **Fallback Support:** Provides predefined learning content when AI-generated responses are unavailable.
- **No Sign-up Required:** Stores learning progress locally in the browser.

## Technology Stack

- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** Python, FastAPI
- **API Communication:** REST API using JSON
- **Data and Progress:** JSON-based career and skill configuration, browser localStorage
- **AI Integration:** Configurable LLM API integration with fallback content

## How It Works

1. Open the landing page.
2. Select a target career, such as ML Engineer.
3. Enter your existing skills, such as Python and Machine Learning.
4. Click **Analyze Skills**.
5. Review the identified skill gaps and priority areas.
6. Select a missing skill, such as Probability and Statistics.
7. Explore the concept explanation, career connection, and suggested practice task.
8. Update the learning status and track progress on the roadmap.

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version
- Node.js and npm
- A modern web browser

### 1. Set Up the Backend

Open a terminal in the project root:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

If the project uses an LLM API, configure the required API key using the environment-variable names documented in `.env.example`. Do not commit API keys or other secrets to GitHub.

Start the backend:

```bash
uvicorn main:app --reload --port 8000
```

Backend URL: http://localhost:8000

### 2. Set Up the Frontend

Open a second terminal in the project root:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, typically:

http://localhost:5173

## What Works in the Current Version

- Navigation between the landing page, profile, dashboard, skill details, and roadmap.
- Skill-gap analysis based on the configured career models and user-provided skills.
- JSON-based communication between FastAPI and React through the `/api/analyze` endpoint.
- Learning-status updates and browser-based progress persistence.
- Fallback learning content for supported skills when AI-generated content is unavailable.

## Limitations and Future Improvements

- Expand and validate career skill models using reliable industry requirements.
- Improve recommendation accuracy through testing and user feedback.
- Expand AI-generated explanations and practical tasks across more skills.
- Introduce user authentication and database-backed progress synchronization.
- Add prerequisite-aware learning paths and interactive skill-dependency graphs.

## Why CareerLearn AI?

CareerLearn AI focuses on more than identifying what learners are missing. It helps them understand why each skill matters, how it connects to their career, and what they can do to practice it.

**Our goal is to turn skill gaps into actionable learning journeys.**