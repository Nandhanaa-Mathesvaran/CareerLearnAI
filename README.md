# CareerLearn AI 🎯
### Understand Skills. Connect Careers. Apply Knowledge.

**CareerLearn AI** is an AI-powered career learning assistant designed to help engineering students identify skill gaps, understand missing concepts, and connect technical learning with real-world career requirements.

Developed as a project submission for **Horizon X 2K26 – Global Hackathon**, CareerLearn AI aims to make career preparation more structured, practical, and accessible.

Demo Video Link: https://youtu.be/LkYaCF-5U8I?si=DCJG3ol_ucVbD2r0

## 📌 Problem Statement

Engineering students often learn programming languages, technical concepts, and tools without having a clear understanding of how these skills relate to their desired careers.

Many students struggle to identify which skills they already possess, which competencies they need to improve, and what they should learn next to prepare for internships and placements.

This lack of direction can lead to unstructured learning, confusion, and difficulty translating theoretical knowledge into practical skills.

## 💡 Our Solution

CareerLearn AI provides a career-oriented learning platform that compares a student's existing skills with the requirements of a selected career.

The application helps students identify potential skill gaps, explore career-related learning guidance, and follow a more structured approach to developing relevant competencies.

Our approach follows three stages:

- **UNDERSTAND** — Identify missing skills and explore the concepts that need further learning.
- **CONNECT** — Understand how individual skills contribute to the requirements of a selected career.
- **APPLY** — Use practical learning guidance and tasks to connect theoretical knowledge with real-world applications.

The goal is to help students move beyond simply collecting learning resources and start learning with a clearer career objective.

## ✨ Key Features

### 1. Career-Based Skill Analysis
Compare existing skills with the skills associated with a selected target career.

### 2. Skill-Gap Identification
Highlight missing or underdeveloped skills that may require additional attention.

### 3. Prioritized Learning Guidance
Organize skill gaps into a more structured learning path based on the application's available career roadmaps.

### 4. Concept Understanding
Help students explore missing technical concepts and understand their relevance to career preparation.

### 5. Practical Application
Connect learning objectives with practical activities and tasks where supported by the implemented learning content.

### 6. Resume Parsing
Upload a PDF resume to extract text and identify recognized skills using the implemented resume-processing functionality.

### 7. Career Recommendations
Suggest potential career directions based on the skills submitted by the user.

### 8. Learning Progress
Use the application's available roadmap and progress-tracking features to support a more organized learning experience.

### 9. Responsive Web Interface
Provide a browser-based interface for interacting with the career analysis and learning features.

*Note: The availability of individual features depends on the current implementation and configuration.*

## 🎯 Target Users

- Engineering students preparing for internships and placements.
- Beginners exploring careers in software engineering, data analytics, and artificial intelligence.
- Students who want to identify their technical skill gaps.
- Learners looking for a more structured approach to career-oriented learning.

## 🛠️ Technology Stack

### Frontend
- React
- Vite
- Tailwind CSS
- JavaScript

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### Supporting Technologies
- PyMuPDF — PDF text extraction for resume processing.
- python-multipart — Handling uploaded files.
- scikit-learn — Text similarity functionality, where implemented.
- python-dotenv — Environment variable management, where configured.
- pytest and HTTPX — Backend testing tools.

### Development Tools
- Git and GitHub
- Visual Studio Code
- npm

## ⚙️ System Architecture

CareerLearn AI uses a frontend-backend architecture.

1. **User input:** The student selects a target career and provides their existing skills.
2. **API communication:** The React frontend sends the input to the FastAPI backend.
3. **Skill analysis:** The backend compares submitted skills against the available career requirements.
4. **Gap identification:** The application identifies skills that may need further development.
5. **Career guidance:** The backend provides available learning guidance and career recommendations.
6. **Results display:** The frontend presents the analysis and relevant learning information.

The resume-processing workflow accepts a PDF, extracts its text, and identifies recognized skills without intentionally retaining the uploaded file permanently.

## 🔄 Application Workflow

**UNDERSTAND → CONNECT → APPLY**

- **Step 1:** Choose a target career.
- **Step 2:** Enter existing skills or use the resume-upload functionality.
- **Step 3:** Review the skill analysis and identified gaps.
- **Step 4:** Explore career relevance and available learning guidance.
- **Step 5:** Use the suggested learning activities to plan the next steps.

## 🚀 Getting Started

### Prerequisites

Install the following:

- Python 3.10 or a compatible version supported by the project dependencies.
- Node.js and npm.
- Git.

### 1. Clone the Repository

```bash
git clone https://github.com/Nandhanaa-Mathesvaran/CareerLearnAI.git
cd CareerLearnAI
```

### 2. Set Up the Backend

Open a terminal in the project directory:

```powershell
cd backend
python -m venv .venv
```

Activate the virtual environment in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the backend server:

```powershell
python -m uvicorn main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/api/health

Keep this terminal running.

### 3. Set Up the Frontend

Open a second terminal in the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, usually:

http://localhost:5173

Keep both the frontend and backend servers running while testing the application.

### 4. Configure the API

The frontend uses the following default API base URL:

```javascript
http://localhost:8000/api
```

The frontend can use a different backend URL through the `VITE_API_BASE_URL` environment variable.

If a frontend environment file is required, configure the variable using the backend API's actual base URL.

Example for local development:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Restart the Vite development server after changing environment variables.

### 5. Resume Upload Requirements

Resume parsing requires the backend dependencies to be installed correctly, including PyMuPDF and python-multipart.

Use a valid, text-based PDF file within the application's configured size limit. Scanned PDFs may require OCR support, which is not assumed to be implemented.

## 🧪 Testing

Verify the backend health endpoint:

```text
http://127.0.0.1:8000/api/health
```

Check that it returns a successful status response.

Use the interactive API documentation at `/docs` to test the following endpoints:

- `POST /api/analyze` — Career skill analysis.
- `POST /api/parse-resume` — Resume parsing.
- `POST /api/recommend` — Career recommendations.
- `GET /api/health` — Backend health check.

If automated backend tests are included in the repository, run them from the backend directory:

```powershell
python -m pytest
```

Verify the actual test results and successful responses before presenting the application as fully tested.

## 🌍 Expected Impact

CareerLearn AI aims to help students:

- Identify skills relevant to their target careers.
- Recognize areas where additional learning is needed.
- Understand the connection between technical concepts and career requirements.
- Follow a more structured learning path.
- Approach internship and placement preparation with greater clarity.

By connecting skill analysis with career-oriented learning, the project seeks to reduce confusion and encourage more purposeful technical development.

## 🔮 Future Improvements

Potential future enhancements include:

- More career paths and regularly updated skill requirements.
- Personalized recommendations based on student progress.
- Integration with trusted courses and learning resources.
- More hands-on projects and assessments.
- Improved resume analysis and skill matching.
- Progress analytics and personalized learning milestones.
- Cloud deployment and broader student access.

These improvements represent possible future work rather than guaranteed existing functionality.

## 📄 Disclaimer

CareerLearn AI is a learning-oriented prototype. Career recommendations and skill-gap results depend on the career data, matching logic, and learning content implemented in the application. The platform is intended to support career exploration and learning, not guarantee employment or placement outcomes.
