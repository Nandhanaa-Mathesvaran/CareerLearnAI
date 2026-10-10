import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="CareerLearn AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    targetCareer: str
    currentSkills: List[str]
    experienceLevel: str

# Career Roadmap Definitions in logical prerequisite order
CAREERS_DB = {
    "ML Engineer": ["Mathematics", "Probability & Statistics", "Python", "SQL", "Data Structures & Algorithms", "Machine Learning", "Deep Learning", "Model Deployment"],
}

FALLBACK_CONTENT = {
    "Mathematics": {
        "whatIsIt": "The foundation of machine learning algorithms, primarily linear algebra (vectors/matrices) and calculus (functions/derivatives).",
        "whyNeeded": "You need to understand how algorithms optimize and transform data under the hood. Vectors represent data, matrices represent transformations, and derivatives allow models to minimize errors.",
        "careerConnection": "As an ML Engineer, you will translate mathematical models into scalable code. Diagnosing a failing model often requires understanding its mathematical properties rather than just writing code.",
        "prerequisites": ["Basic Algebra"],
        "learningSteps": ["Vectors and Dot Products", "Matrices and Matrix Multiplication", "Functions and Basic Derivatives"],
        "applicationTask": {
            "title": "Vector and Matrix Operations in Python",
            "objective": "Understand how data is mathematically represented and transformed.",
            "difficulty": "Beginner",
            "estimatedTime": "1 hour",
            "steps": [
                "Install and import numpy.",
                "Create a 1D vector representing 3 features of an object (e.g. height, width, weight).",
                "Create a 3x3 matrix representing a mathematical transformation (like scaling weights).",
                "Use np.dot() or the @ operator to multiply the matrix by the vector.",
                "Print the resulting vector and write a brief comment explaining what just changed."
            ],
            "expectedOutput": "A small Python script generating a new transformed vector.",
            "hint": "In numpy, matrices are nested lists: np.array([[1,2,3],[4,5,6],[7,8,9]])."
        }
    },
    "Probability & Statistics": {
        "whatIsIt": "The science of collecting, analyzing, and interpreting data, including random variables and probability distributions.",
        "whyNeeded": "Data is noisy. Statistics help you understand data distributions, central tendencies, and variations, ensuring your models learn meaningful patterns instead of noise.",
        "careerConnection": "When evaluating an ML model or analyzing a dataset, you rely heavily on statistical metrics (like variance or p-values) to prove your solution generalizes well to unseen real-world data.",
        "prerequisites": ["Mathematics (Algebra)"],
        "learningSteps": ["Descriptive Statistics", "Data Distributions", "Hypothesis Testing"],
        "applicationTask": {
            "title": "Calculate Descriptive Statistics",
            "objective": "Use Python to calculate mean, median, mode, and standard deviation to understand a dataset.",
            "difficulty": "Beginner",
            "estimatedTime": "45 minutes",
            "steps": [
                "Create a list of 10 generic house prices: [250k, 300k, ...].",
                "Use the 'statistics' module to calculate the mean and median.",
                "Calculate the standard deviation to understand price variation.",
                "Inject a massive outlier (e.g., 5 million) into the list and recalculate.",
                "Write a comment explaining why the median is completely different from the mean after inserting the outlier."
            ],
            "expectedOutput": "A Python script showing the metrics before and after the outlier.",
            "hint": "import statistics; median_val = statistics.median(prices)"
        }
    },
    "Machine Learning": {
        "whatIsIt": "Algorithms that parse data, learn from that data, and then apply what they've learned to make informed decisions without explicit programming. Covers supervised and unsupervised learning.",
        "whyNeeded": "It's the core of the role. You must understand how to map input features (data) to requested labels (predictions) via training, then validate via testing.",
        "careerConnection": "ML Engineers don't just build systems; they implement ML models to solve business problems, constantly tuning training pipelines and avoiding overfitting.",
        "prerequisites": ["Python", "Probability & Statistics", "Mathematics"],
        "learningSteps": ["Supervised vs Unsupervised Learning", "Features and Labels", "Training vs Testing", "Model Evaluation (MAE, RMSE)"],
        "applicationTask": {
            "title": "Train a Simple Regression Model",
            "objective": "Train a model to predict numeric values and evaluate its performance.",
            "difficulty": "Intermediate",
            "estimatedTime": "1.5 hours",
            "steps": [
                "Install scikit-learn and import LinearRegression.",
                "Generate a dummy dataset of 100 rows containing X (e.g. square footage) and Y (prices).",
                "Split the dataset into training (80%) and testing (20%) using train_test_split.",
                "Fit the LinearRegression model on the training data.",
                "Predict on the test data and calculate the Mean Absolute Error (MAE)."
            ],
            "expectedOutput": "A script outputting the MAE for the test predictions.",
            "hint": "from sklearn.metrics import mean_absolute_error"
        }
    },
    "Deep Learning": {
        "whatIsIt": "A specialized subset of machine learning concerning artificial neural networks, layers, and backpropagation.",
        "whyNeeded": "For complex, unstructured data like images, audio, and raw text, classical ML fails. Deep Learning excels by learning features autonomously.",
        "careerConnection": "Modern ML engineering heavily relies on deep learning architectures (Transformers, CNNs) for state-of-the-art results.",
        "prerequisites": ["Machine Learning", "Mathematics"],
        "learningSteps": ["Neural Network Architecture", "Activation Functions", "Backpropagation", "Loss Functions"],
        "applicationTask": {
            "title": "Build a Simple Neural Network",
            "objective": "Construct a basic sequential neural network using PyTorch or TensorFlow.",
            "difficulty": "Advanced",
            "estimatedTime": "2 hours",
            "steps": [
                "Install PyTorch.",
                "Define a sequential model with an input layer, one hidden layer (ReLU), and an output layer.",
                "Define a Loss function (MSE).",
                "Pass a dummy tensor through the network to generate an initial untuned prediction.",
                "Print the prediction shape and the calculated loss."
            ],
            "expectedOutput": "A functioning script predicting a raw tensor output.",
            "hint": "import torch.nn as nn"
        }
    },
    "Data Structures & Algorithms": {
        "whatIsIt": "The foundations of computer science dictating how data is organized (structures) and manipulated (algorithms) efficiently.",
        "whyNeeded": "Machine learning deals with enormous amounts of data. Inefficient algorithms can multiply execution time from minutes to months.",
        "careerConnection": "As an ML Engineer, you will frequently write data transformation pipelines. DSA knowledge is critical for optimizing memory and CPU usage.",
        "prerequisites": ["Python"],
        "learningSteps": ["Arrays & Hash Maps", "Trees & Graphs", "Sorting & Searching", "Time Complexity (Big-O)"],
        "applicationTask": {
            "title": "Optimize a Search Algorithm",
            "objective": "Compare the performance of linear search vs dictionary lookup.",
            "difficulty": "Beginner",
            "estimatedTime": "1 hour",
            "steps": [
                "Generate a list of 1 million random integers.",
                "Write a function to linearly search the list for a specific number.",
                "Store the same integers as keys in a dictionary.",
                "Use the 'time' module to measure searching for a number in the list vs checking if it exists in the dictionary.",
                "Print the time elapsed for both."
            ],
            "expectedOutput": "Time difference showing the massive speed advantage of Hash Maps.",
            "hint": "Dictionary lookups are O(1) complexity."
        }
    },
    "SQL": {
        "whatIsIt": "Structured Query Language, a standardized programming language that is used to manage relational databases.",
        "whyNeeded": "Before you can train a model, you need data. Almost all structured corporate data lives in SQL databases.",
        "careerConnection": "You will write complex queries daily to extract features, clean raw enterprise data, and structure it for model training.",
        "prerequisites": [],
        "learningSteps": ["SELECT & WHERE", "JOIN Operations", "Aggregations (GROUP BY)", "Subqueries"],
        "applicationTask": {
            "title": "Data Extraction & Aggregation via SQL",
            "objective": "Write queries measuring specific metrics across tables.",
            "difficulty": "Intermediate",
            "estimatedTime": "45 minutes",
            "steps": [
                "Set up an in-memory SQLite database in Python.",
                "Create a 'users' table and a 'purchases' table with dummy data.",
                "Write a query selecting all users who made a purchase.",
                "Write a query using a JOIN and GROUP BY to sum total purchase amounts per user.",
                "Fetch and print the results."
            ],
            "expectedOutput": "Console printing the aggregated results of the query.",
            "hint": "Use python's builtin 'sqlite3' module."
        }
    },
    "Git": {
        "whatIsIt": "A distributed version control system tracking changes in any set of files.",
        "whyNeeded": "You must safely manage code changes without deleting history or breaking production.",
        "careerConnection": "ML Engineers rarely work alone. You will push code, pull colleague updates, and merge model improvements constantly.",
        "prerequisites": [],
        "learningSteps": ["Commits & History", "Branching", "Pushing & Pulling", "Resolving Conflicts"],
        "applicationTask": {
            "title": "Basic Version Control Flow",
            "objective": "Initialize a repository, make branches, and simulate a feature merge.",
            "difficulty": "Beginner",
            "estimatedTime": "30 minutes",
            "steps": [
                "Run 'git init' in a new folder.",
                "Create a 'model.py' file, commit it.",
                "Create a new branch 'experiment', change the code in 'model.py', and commit it on the branch.",
                "Switch back to main.",
                "Merge the 'experiment' branch into main."
            ],
            "expectedOutput": "A git log demonstrating branching and merging history.",
            "hint": "git checkout -b <branch_name> creates and switches to a branch."
        }
    },
    "Model Deployment": {
        "whatIsIt": "The architectural processes required to take a locally trained ML model and expose it reliably to external users or systems over the internet.",
        "whyNeeded": "A model is useless if it sits isolated on your laptop. It needs an interface (like a REST API) to be valuable.",
        "careerConnection": "Closing the ML loop. You will wrap models in REST APIs (FastAPI) or containers (Docker) so that frontend apps can consume predictions.",
        "prerequisites": ["Python", "Machine Learning"],
        "learningSteps": ["REST APIs", "Serialization (Pickle)", "Docker Basics", "Cloud Hosting"],
        "applicationTask": {
            "title": "Serve a Model via API",
            "objective": "Create a local web server capable of receiving data and returning a prediction.",
            "difficulty": "Intermediate",
            "estimatedTime": "1.5 hours",
            "steps": [
                "Train an extremely tiny dummy model in Python (or just write a function that returns a static float prediction).",
                "Use FastAPI (like the backend of this app) to create a POST endpoint.",
                "Define a Pydantic schema for the input data.",
                "In the endpoint, pass the input data to your dummy model/function and return the result.",
                "Test it locally using an HTTP client (curl or Postman)."
            ],
            "expectedOutput": "A JSON payload receiving a mocked prediction via HTTP.",
            "hint": "uvicorn main:app runs the FastAPI server locally."
        }
    },
    "Python": {
         "whatIsIt": "A high-level programming language known for readability and an extensive ecosystem of data processing libraries.",
         "whyNeeded": "It's the industry standard for ML. 99% of training frameworks use Python.",
         "careerConnection": "You will write Python scripts daily for everything from data munging to model serving.",
         "prerequisites": [],
         "learningSteps": ["Syntax basics", "Data types & functions", "Object Oriented Programming"],
         "applicationTask": {
             "title": "Script Automation",
             "objective": "Automate a basic text processing task using Python.",
             "difficulty": "Beginner",
             "estimatedTime": "30 minutes",
             "steps": ["Create a text file containing random words.", "Write a python script that reads the file.", "Count the occurrence of each word.", "Print the top 3 most common words."],
             "expectedOutput": "Console printing the most common words.",
             "hint": "Use collections.Counter"
         }
    }
}

def generate_llm_response(skill: str, priority: str) -> Dict[str, Any]:
    return {
        "skill": skill,
        "priority": priority,
        "whatIsIt": f"Concept explanation for: {skill}",
        "whyNeeded": "Understanding this ensures robust technical capability in specific scenarios.",
        "careerConnection": "Relevant for the workflow of this particular subset of engineering tasks.",
        "prerequisites": ["Fundamentals"],
        "learningSteps": ["Basics", "Advanced Topics"],
        "applicationTask": {
            "title": f"Explore {skill}",
            "objective": f"Familiarize yourself with {skill}.",
            "difficulty": "Intermediate",
            "estimatedTime": "1 hour",
            "steps": ["Setup environment", "Follow standard API docs", "Output result"],
            "expectedOutput": "Familiarity with the tech.",
            "hint": "Refer to official documentation."
        }
    }

@app.post("/api/analyze")
async def analyze_skills(req: AnalysisRequest):
    target = req.targetCareer
    current = set(req.currentSkills)
    
    # Generate roadmap array mapped to ML Engineer standard template if exists, else dynamic.
    required = CAREERS_DB.get(target, CAREERS_DB["ML Engineer"])
    
    knownSkills = [r for r in required if r in current]
    missingSkills = [r for r in required if r not in current]
    # For skills user listed that aren't in required (optional)
    additionalKnown = [r for r in current if r not in required]
    knownSkills.extend(additionalKnown)
    
    readinessScore = int((len(knownSkills) / len(required)) * 100) if required else 0
    if readinessScore > 75:
        estimate = "High"
    elif readinessScore > 40:
        estimate = "Medium"
    else:
        estimate = "Low"

    explanations = []
    # Generate content for ALL missing required skills
    for skill in missingSkills:
        content = FALLBACK_CONTENT.get(skill)
        priority = "HIGH" if skill in ["Mathematics", "Python", "Machine Learning"] else "MEDIUM"
        if content:
            content_cpy = dict(content)
            content_cpy["skill"] = skill
            content_cpy["priority"] = priority
            explanations.append(content_cpy)
        else:
            explanations.append(generate_llm_response(skill, priority))
            
    roadmap = missingSkills + [k for k in knownSkills if k in required]
    
    return {
        "targetCareer": target,
        "knownSkills": knownSkills,
        "weakSkills": [],
        "missingSkills": missingSkills,
        "readinessEstimate": estimate,
        "skillExplanations": explanations,
        "roadmap": required # ALWAYS present the full required ML path in roadmap
    }

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
