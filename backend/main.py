import os
import re
import tempfile
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# PyMuPDF — imported lazily so the rest of the API still works if not installed
try:
    import pymupdf
    _PYMUPDF_AVAILABLE = True
except ImportError:
    try:
        import fitz as pymupdf
        _PYMUPDF_AVAILABLE = True
    except ImportError:
        pymupdf = None
        _PYMUPDF_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    _SKLEARN_AVAILABLE = True
except ImportError:
    _SKLEARN_AVAILABLE = False

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
    experienceLevel: str = "Beginner"


class RecommendRequest(BaseModel):
    currentSkills: List[str]


# ─── Career Roadmaps in prerequisite order ─────────────────────────────────────
CAREERS_DB: Dict[str, List[str]] = {
    "ML Engineer": [
        "Mathematics", "Probability & Statistics", "Python",
        "SQL", "Data Structures & Algorithms",
        "Machine Learning", "Deep Learning", "Model Deployment",
    ],
    "Data Scientist": [
        "Python", "Mathematics", "Probability & Statistics",
        "SQL", "Data Wrangling", "Exploratory Data Analysis",
        "Machine Learning", "Data Visualization", "Storytelling with Data",
    ],
    "Data Analyst": [
        "Excel", "SQL", "Python",
        "Data Wrangling", "Exploratory Data Analysis",
        "Data Visualization", "Storytelling with Data",
        "Business Intelligence Tools",
    ],
    "Software Engineer": [
        "Python", "Data Structures & Algorithms",
        "Object-Oriented Programming", "System Design",
        "Databases", "Version Control (Git)",
        "REST APIs", "Testing & Debugging",
    ],
    "AI Engineer": [
        "Python", "Mathematics", "Probability & Statistics",
        "Machine Learning", "Deep Learning",
        "Natural Language Processing", "Model Deployment",
        "Cloud Platforms", "MLOps",
    ],
    "Full Stack Developer": [
        "HTML & CSS", "JavaScript", "React",
        "Node.js", "REST APIs", "Databases",
        "Version Control (Git)", "System Design",
    ],
}

# ─── Experience-level overlays ─────────────────────────────────────────────────
# Each skill's content can be tuned per level.
# Structure: LEVEL_OVERLAYS[level][skill] = { "learningSteps", "applicationTask" }
# If a skill is not listed for a level, the base FALLBACK_CONTENT is used unchanged.

LEVEL_OVERLAYS: Dict[str, Dict[str, Dict[str, Any]]] = {
    "Beginner": {},   # defaults are already beginner-friendly
    "Intermediate": {
        "Python": {
            "learningSteps": ["Decorators & Generators", "Comprehensions", "File I/O", "Virtual Environments"],
            "applicationTask": {
                "title": "Build a Data Pipeline Script",
                "objective": "Read a CSV, transform the data with list comprehensions, and write cleaned output.",
                "difficulty": "Intermediate",
                "estimatedTime": "45 minutes",
                "steps": [
                    "Read a CSV file using Python's csv module.",
                    "Filter rows where a numeric column exceeds a threshold.",
                    "Normalise text columns (strip whitespace, lowercase).",
                    "Write the cleaned rows to a new CSV.",
                    "Log the number of rows processed vs. filtered.",
                ],
                "expectedOutput": "A cleaned CSV file and a summary log.",
                "hint": "Use csv.DictReader / DictWriter for column-level access.",
            },
        },
        "Machine Learning": {
            "learningSteps": ["Pipeline with scikit-learn", "Feature Engineering", "Cross-Validation", "Hyperparameter Tuning"],
            "applicationTask": {
                "title": "End-to-End Classification Pipeline",
                "objective": "Build a complete ML pipeline with preprocessing, a classifier, and cross-validated evaluation.",
                "difficulty": "Intermediate",
                "estimatedTime": "2 hours",
                "steps": [
                    "Load the Wisconsin Breast Cancer dataset from sklearn.datasets.",
                    "Build a Pipeline: StandardScaler → LogisticRegression.",
                    "Use 5-fold StratifiedKFold cross-validation.",
                    "Print mean accuracy and standard deviation.",
                    "Swap the classifier to RandomForestClassifier and compare metrics.",
                ],
                "expectedOutput": "Cross-validation scores for two classifiers printed to console.",
                "hint": "from sklearn.pipeline import Pipeline; from sklearn.model_selection import cross_val_score",
            },
        },
        "SQL": {
            "learningSteps": ["Window Functions", "CTEs", "Indexing", "Query Optimisation"],
            "applicationTask": {
                "title": "Analyse Sales with Window Functions",
                "objective": "Use CTEs and window functions to compute running totals and rankings.",
                "difficulty": "Intermediate",
                "estimatedTime": "1 hour",
                "steps": [
                    "Create a SQLite sales table with columns: id, region, amount, sale_date.",
                    "Insert 20 sample rows across 3 regions.",
                    "Write a CTE that sums amount per region.",
                    "Add a ROW_NUMBER() window function ranking sales within each region.",
                    "Print the top sale per region.",
                ],
                "expectedOutput": "A table showing top sale per region with running rank.",
                "hint": "SQLite supports ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC).",
            },
        },
    },
    "Advanced": {
        "Python": {
            "learningSteps": ["Asyncio & Concurrency", "C extensions & Cython", "Metaclasses", "Memory Profiling"],
            "applicationTask": {
                "title": "Async Concurrent Data Fetcher",
                "objective": "Fetch data from multiple mock endpoints concurrently using asyncio.",
                "difficulty": "Advanced",
                "estimatedTime": "1.5 hours",
                "steps": [
                    "Install httpx with async support.",
                    "Define a list of 10 mock API URLs (httpbin.org/delay/1 etc.).",
                    "Use asyncio.gather() to fetch all URLs concurrently.",
                    "Time sequential vs concurrent fetch and print the speedup ratio.",
                    "Handle timeout exceptions gracefully with asyncio.wait_for().",
                ],
                "expectedOutput": "Console showing concurrency speedup and any timeout errors handled.",
                "hint": "import asyncio, httpx; async with httpx.AsyncClient() as client: ...",
            },
        },
        "Machine Learning": {
            "learningSteps": ["Custom Loss Functions", "Gradient Boosting Internals", "Model Interpretability (SHAP)", "Production Pipelines"],
            "applicationTask": {
                "title": "Gradient Boosting with SHAP Explanations",
                "objective": "Train an XGBoost model and explain individual predictions using SHAP values.",
                "difficulty": "Advanced",
                "estimatedTime": "2.5 hours",
                "steps": [
                    "pip install xgboost shap.",
                    "Load the California Housing dataset.",
                    "Train an XGBoostRegressor with early stopping on a hold-out set.",
                    "Generate SHAP values for the test set.",
                    "Plot a SHAP summary_plot and identify the top 3 influential features.",
                ],
                "expectedOutput": "An XGBoost model with printed RMSE and a SHAP feature importance plot.",
                "hint": "shap.TreeExplainer(model).shap_values(X_test) — runs locally without a GPU.",
            },
        },
        "Deep Learning": {
            "learningSteps": ["Custom Training Loops", "Attention Mechanisms", "Transfer Learning", "Model Quantisation"],
            "applicationTask": {
                "title": "Fine-Tune a Pretrained Image Classifier",
                "objective": "Fine-tune ResNet18 on a custom binary classification dataset.",
                "difficulty": "Advanced",
                "estimatedTime": "3 hours",
                "steps": [
                    "pip install torch torchvision.",
                    "Load torchvision.models.resnet18(pretrained=True).",
                    "Freeze all layers except the final FC layer.",
                    "Train on a 2-class subset of CIFAR-10 for 5 epochs.",
                    "Unfreeze the last ResNet block and fine-tune for 2 more epochs.",
                    "Compare accuracy before and after unfreezing.",
                ],
                "expectedOutput": "Training loss and accuracy logged per epoch; improvement after unfreezing shown.",
                "hint": "for param in model.parameters(): param.requires_grad = False — then reset the final layer.",
            },
        },
    },
}


# ─── Base Fallback Content (Beginner level) ────────────────────────────────────
FALLBACK_CONTENT: Dict[str, Dict[str, Any]] = {
    # ── ML Engineer / shared ──────────────────────────────────────────────────
    "Mathematics": {
        "whatIsIt": "The foundation of machine learning algorithms — primarily linear algebra (vectors/matrices) and calculus (functions/derivatives).",
        "whyNeeded": "You need to understand how algorithms optimise and transform data under the hood. Vectors represent data, matrices represent transformations, and derivatives allow models to minimise errors.",
        "careerConnection": "As an ML Engineer, diagnosing a failing model often requires understanding its mathematical properties rather than just tweaking code.",
        "prerequisites": ["Basic Algebra"],
        "learningSteps": ["Vectors and Dot Products", "Matrices and Matrix Multiplication", "Functions and Basic Derivatives"],
        "applicationTask": {
            "title": "Vector and Matrix Operations in Python",
            "objective": "Understand how data is mathematically represented and transformed.",
            "difficulty": "Beginner",
            "estimatedTime": "1 hour",
            "steps": [
                "Install and import numpy.",
                "Create a 1D vector representing 3 features (e.g. height, width, weight).",
                "Create a 3×3 matrix representing a transformation.",
                "Multiply the matrix by the vector using np.dot().",
                "Print the result and add a comment explaining what changed.",
            ],
            "expectedOutput": "A Python script generating a transformed vector.",
            "hint": "np.array([[1,2,3],[4,5,6],[7,8,9]]) creates a 3×3 matrix.",
        },
    },
    "Probability & Statistics": {
        "whatIsIt": "The science of collecting, analysing and interpreting data — including random variables, distributions and hypothesis tests.",
        "whyNeeded": "Data is noisy. Statistics help you understand distributions and trends so your models learn meaningful patterns instead of noise.",
        "careerConnection": "When evaluating an ML model or analysing a dataset you rely on statistical metrics (variance, p-values, confidence intervals) to prove generalisation.",
        "prerequisites": ["Mathematics (Algebra)"],
        "learningSteps": ["Descriptive Statistics", "Data Distributions", "Hypothesis Testing"],
        "applicationTask": {
            "title": "Calculate Descriptive Statistics",
            "objective": "Use Python to calculate mean, median, mode and standard deviation to understand a dataset.",
            "difficulty": "Beginner",
            "estimatedTime": "45 minutes",
            "steps": [
                "Create a list of 10 house prices.",
                "Use the 'statistics' module to calculate mean and median.",
                "Calculate standard deviation.",
                "Inject a large outlier and recalculate.",
                "Comment why median differs from mean after the outlier.",
            ],
            "expectedOutput": "Metrics before and after the outlier, printed to console.",
            "hint": "import statistics; statistics.median(prices)",
        },
    },
    "Python": {
        "whatIsIt": "A high-level programming language known for readability and a huge ecosystem of data and ML libraries.",
        "whyNeeded": "Python is the industry standard for data work and ML. 99 % of training frameworks use it.",
        "careerConnection": "You will write Python scripts daily for everything from data munging to model serving.",
        "prerequisites": [],
        "learningSteps": ["Syntax basics", "Data types & functions", "Object-Oriented Programming"],
        "applicationTask": {
            "title": "Script Automation",
            "objective": "Automate a basic text-processing task using Python.",
            "difficulty": "Beginner",
            "estimatedTime": "30 minutes",
            "steps": [
                "Create a text file containing random words.",
                "Write a Python script that reads the file.",
                "Count the occurrence of each word.",
                "Print the top 3 most common words.",
            ],
            "expectedOutput": "Console printing the most common words.",
            "hint": "Use collections.Counter",
        },
    },
    "SQL": {
        "whatIsIt": "Structured Query Language — the standard tool for managing and querying relational databases.",
        "whyNeeded": "Before you can train a model, you need data. Almost all structured corporate data lives in SQL databases.",
        "careerConnection": "You will write complex queries daily to extract features, clean raw data and structure it for analysis or model training.",
        "prerequisites": [],
        "learningSteps": ["SELECT & WHERE", "JOIN Operations", "Aggregations (GROUP BY)", "Subqueries"],
        "applicationTask": {
            "title": "Data Extraction & Aggregation via SQL",
            "objective": "Write queries measuring specific metrics across tables.",
            "difficulty": "Beginner",
            "estimatedTime": "45 minutes",
            "steps": [
                "Set up an in-memory SQLite database in Python.",
                "Create 'users' and 'purchases' tables with dummy data.",
                "Write a query selecting all users who made a purchase.",
                "Use JOIN + GROUP BY to sum total purchases per user.",
                "Fetch and print the results.",
            ],
            "expectedOutput": "Aggregated results printed to console.",
            "hint": "Use Python's built-in 'sqlite3' module.",
        },
    },
    "Data Structures & Algorithms": {
        "whatIsIt": "The foundations of computer science — how data is organised (structures) and manipulated (algorithms) efficiently.",
        "whyNeeded": "ML deals with enormous data volumes. Inefficient algorithms can multiply execution time from minutes to days.",
        "careerConnection": "As an ML Engineer or Software Engineer you will frequently write data transformation pipelines optimised for memory and CPU usage.",
        "prerequisites": ["Python"],
        "learningSteps": ["Arrays & Hash Maps", "Trees & Graphs", "Sorting & Searching", "Time Complexity (Big-O)"],
        "applicationTask": {
            "title": "Optimise a Search Algorithm",
            "objective": "Compare linear search vs dictionary lookup performance.",
            "difficulty": "Beginner",
            "estimatedTime": "1 hour",
            "steps": [
                "Generate a list of 1 million random integers.",
                "Write a function for linear search.",
                "Store the same integers as dictionary keys.",
                "Time both approaches using the 'time' module.",
                "Print the time difference.",
            ],
            "expectedOutput": "Console showing the speed advantage of hash maps.",
            "hint": "Dictionary lookups are O(1) complexity.",
        },
    },
    "Machine Learning": {
        "whatIsIt": "Algorithms that parse data, learn from it and apply what they've learned to make predictions — covering supervised and unsupervised learning.",
        "whyNeeded": "It is the core of ML and Data Science roles. You must understand how to map input features to labels via training and validate via testing.",
        "careerConnection": "ML Engineers and Data Scientists implement ML models to solve business problems, constantly tuning training pipelines and avoiding overfitting.",
        "prerequisites": ["Python", "Probability & Statistics", "Mathematics"],
        "learningSteps": ["Supervised vs Unsupervised Learning", "Features and Labels", "Training vs Testing", "Model Evaluation (MAE, RMSE)"],
        "applicationTask": {
            "title": "Train a Simple Regression Model",
            "objective": "Train a model to predict numeric values and evaluate its performance.",
            "difficulty": "Beginner",
            "estimatedTime": "1.5 hours",
            "steps": [
                "Install scikit-learn and import LinearRegression.",
                "Generate a dummy dataset of 100 rows (X = square footage, Y = price).",
                "Split 80/20 using train_test_split.",
                "Fit the model on training data.",
                "Predict on test data and calculate MAE.",
            ],
            "expectedOutput": "A script outputting the MAE for test predictions.",
            "hint": "from sklearn.metrics import mean_absolute_error",
        },
    },
    "Deep Learning": {
        "whatIsIt": "A specialised subset of ML using artificial neural networks, layers and backpropagation.",
        "whyNeeded": "For complex, unstructured data like images, audio and raw text, classical ML fails. Deep Learning learns features autonomously.",
        "careerConnection": "Modern ML and AI Engineering rely heavily on deep learning architectures (Transformers, CNNs) for state-of-the-art results.",
        "prerequisites": ["Machine Learning", "Mathematics"],
        "learningSteps": ["Neural Network Architecture", "Activation Functions", "Backpropagation", "Loss Functions"],
        "applicationTask": {
            "title": "Build a Simple Neural Network",
            "objective": "Construct a basic sequential neural network using PyTorch.",
            "difficulty": "Intermediate",
            "estimatedTime": "2 hours",
            "steps": [
                "Install PyTorch.",
                "Define a sequential model: input layer → hidden layer (ReLU) → output layer.",
                "Define a Loss function (MSE).",
                "Pass a dummy tensor through the network.",
                "Print the prediction shape and calculated loss.",
            ],
            "expectedOutput": "A functioning script predicting a raw tensor output.",
            "hint": "import torch.nn as nn",
        },
    },
    "Model Deployment": {
        "whatIsIt": "The processes required to take a locally trained ML model and expose it reliably to external users over the internet.",
        "whyNeeded": "A model is useless if it sits isolated on your laptop. It needs an interface (REST API or container) to be valuable.",
        "careerConnection": "Closing the ML loop — you will wrap models in REST APIs (FastAPI) or containers (Docker) so frontend apps can consume predictions.",
        "prerequisites": ["Python", "Machine Learning"],
        "learningSteps": ["REST APIs", "Serialisation (Pickle)", "Docker Basics", "Cloud Hosting"],
        "applicationTask": {
            "title": "Serve a Model via API",
            "objective": "Create a local web server capable of receiving data and returning a prediction.",
            "difficulty": "Intermediate",
            "estimatedTime": "1.5 hours",
            "steps": [
                "Train a tiny dummy model (or write a function returning a static float).",
                "Create a FastAPI POST endpoint.",
                "Define a Pydantic schema for the input.",
                "Pass input data to the model and return the result.",
                "Test with curl or Postman.",
            ],
            "expectedOutput": "A JSON payload receiving a prediction via HTTP.",
            "hint": "uvicorn main:app --reload runs the FastAPI server locally.",
        },
    },

    # ── Data Scientist / Data Analyst ────────────────────────────────────────
    "Data Wrangling": {
        "whatIsIt": "The process of cleaning, restructuring and enriching raw data into a usable format for analysis or modelling.",
        "whyNeeded": "Real-world data is messy — missing values, wrong types, duplicates. You cannot build reliable models or produce accurate insights without clean data.",
        "careerConnection": "Data Scientists and Analysts spend up to 80 % of their time wrangling data before any modelling or visualisation takes place.",
        "prerequisites": ["Python", "SQL"],
        "learningSteps": ["Handling Missing Values", "Data Type Conversion", "Merging Datasets", "Removing Duplicates"],
        "applicationTask": {
            "title": "Clean a Messy Dataset with Pandas",
            "objective": "Load a CSV with intentional errors and produce a clean, analysis-ready DataFrame.",
            "difficulty": "Beginner",
            "estimatedTime": "1 hour",
            "steps": [
                "Create a CSV with 5 columns: Name, Age, Salary, Department, JoinDate — add NaN values and duplicates.",
                "Load with pd.read_csv().",
                "Drop duplicate rows.",
                "Fill missing Age with the median; drop rows with missing Salary.",
                "Convert JoinDate to datetime and extract the year.",
                "Print the final shape and dtypes.",
            ],
            "expectedOutput": "A clean DataFrame with correct dtypes and no nulls in critical columns.",
            "hint": "df.dropna(subset=['Salary']); df['Age'].fillna(df['Age'].median())",
        },
    },
    "Exploratory Data Analysis": {
        "whatIsIt": "An approach to analysing datasets by summarising their main characteristics, often using visual methods.",
        "whyNeeded": "EDA helps you understand data distributions, detect anomalies and form hypotheses before modelling — preventing wasted model-training time.",
        "careerConnection": "Every Data Scientist and Data Analyst performs EDA as the first step of any project to discover patterns and validate assumptions.",
        "prerequisites": ["Python", "Probability & Statistics"],
        "learningSteps": ["Summary Statistics", "Correlation Analysis", "Distribution Plots", "Outlier Detection"],
        "applicationTask": {
            "title": "EDA on a Housing Dataset",
            "objective": "Perform structured EDA to understand a dataset before modelling.",
            "difficulty": "Beginner",
            "estimatedTime": "1.5 hours",
            "steps": [
                "Load the sklearn California Housing dataset.",
                "Print .describe() to get summary statistics.",
                "Plot a histogram of the target variable (house prices).",
                "Compute a correlation matrix and identify the top 3 features correlated with price.",
                "Plot a scatter: most correlated feature vs. price.",
            ],
            "expectedOutput": "A correlation matrix and scatter plot highlighting key relationships.",
            "hint": "import seaborn as sns; sns.heatmap(df.corr(), annot=True)",
        },
    },
    "Data Visualization": {
        "whatIsIt": "The graphical representation of information and data using charts, graphs and maps to reveal patterns and insights.",
        "whyNeeded": "Raw numbers are hard to interpret. Visualisations communicate insights instantly to both technical and non-technical stakeholders.",
        "careerConnection": "Data Analysts and Data Scientists use visualisation to present findings, support decisions and tell the story of the data.",
        "prerequisites": ["Python", "Exploratory Data Analysis"],
        "learningSteps": ["Line and Bar Charts", "Scatter and Bubble Plots", "Heatmaps", "Interactive Dashboards"],
        "applicationTask": {
            "title": "Build a Multi-Chart Dashboard",
            "objective": "Create a 4-panel matplotlib figure exploring a sales dataset.",
            "difficulty": "Beginner",
            "estimatedTime": "1 hour",
            "steps": [
                "Generate a synthetic sales DataFrame: region, product, month, revenue.",
                "Create a 2×2 subplot grid.",
                "Panel 1: Bar chart of total revenue by region.",
                "Panel 2: Line chart of monthly revenue trend.",
                "Panel 3: Pie chart of product share.",
                "Panel 4: Scatter plot of units_sold vs. revenue.",
            ],
            "expectedOutput": "A saved PNG with 4 labelled charts.",
            "hint": "fig, axes = plt.subplots(2, 2, figsize=(12, 8))",
        },
    },
    "Storytelling with Data": {
        "whatIsIt": "The skill of communicating data-driven insights through a clear narrative that drives decision-making.",
        "whyNeeded": "Even perfect analysis is wasted if stakeholders cannot understand it. Storytelling bridges the gap between raw numbers and action.",
        "careerConnection": "Data Analysts and Data Scientists must translate complex findings into simple, compelling presentations for management and clients.",
        "prerequisites": ["Data Visualization"],
        "learningSteps": ["Structuring a Data Narrative", "Choosing the Right Chart", "Reducing Chart Junk", "Crafting Recommendations"],
        "applicationTask": {
            "title": "Revenue Decline Root-Cause Presentation",
            "objective": "Build a 5-slide narrative explaining a fictional revenue drop.",
            "difficulty": "Beginner",
            "estimatedTime": "1.5 hours",
            "steps": [
                "Create a synthetic monthly revenue dataset with a visible Q3 dip.",
                "Slide 1: Overall trend line — highlight the dip.",
                "Slide 2: Break down by region — identify the culprit.",
                "Slide 3: Drill into the culprit region by product.",
                "Slide 4: Root cause — annotated bar chart.",
                "Slide 5: 3-bullet recommendation.",
            ],
            "expectedOutput": "A 5-chart story exported to a PDF or PNG sequence.",
            "hint": "Use plt.annotate() to add callout text to the key data point.",
        },
    },
    "Business Intelligence Tools": {
        "whatIsIt": "Software platforms (Power BI, Tableau, Looker) that allow non-coders to build interactive dashboards from connected data sources.",
        "whyNeeded": "Most organisations use BI tools for self-service analytics. Analysts who master them unlock insights for the entire company without writing code.",
        "careerConnection": "Data Analysts are frequently responsible for maintaining company dashboards and delivering KPI reports through BI platforms.",
        "prerequisites": ["SQL", "Data Visualization"],
        "learningSteps": ["Connecting Data Sources", "Building Calculated Fields", "Creating Interactive Filters", "Publishing Reports"],
        "applicationTask": {
            "title": "Build a KPI Dashboard in Power BI (or Metabase)",
            "objective": "Connect a CSV, build 4 KPI cards and 2 charts in a free BI tool.",
            "difficulty": "Beginner",
            "estimatedTime": "2 hours",
            "steps": [
                "Download Power BI Desktop (free) or sign up for Metabase Cloud.",
                "Upload a sales CSV with columns: date, region, category, revenue, units.",
                "Create KPI cards: Total Revenue, Total Units, Avg Order Value, Top Region.",
                "Add a monthly revenue line chart.",
                "Add a category bar chart.",
                "Publish or export the report.",
            ],
            "expectedOutput": "A published or exported BI report with 4 KPIs and 2 charts.",
            "hint": "Metabase is free and browser-based — no install required.",
        },
    },
    "Excel": {
        "whatIsIt": "Microsoft Excel — the world's most widely used spreadsheet tool for data entry, analysis and basic reporting.",
        "whyNeeded": "Excel is the universal language of business data. Most entry-level Analyst roles require strong Excel proficiency.",
        "careerConnection": "Data Analysts use Excel daily for quick calculations, pivot tables and dashboards before graduating to SQL or Python for larger datasets.",
        "prerequisites": [],
        "learningSteps": ["Formulas & Functions", "VLOOKUP & XLOOKUP", "Pivot Tables", "Basic Charts"],
        "applicationTask": {
            "title": "Sales Analysis with Pivot Tables",
            "objective": "Use Excel pivot tables to summarise a sales dataset by region and product.",
            "difficulty": "Beginner",
            "estimatedTime": "45 minutes",
            "steps": [
                "Create a table with 50 rows: Region, Product, Units, Revenue.",
                "Insert a Pivot Table summarising Revenue by Region.",
                "Add Product as a column field.",
                "Add a calculated field: Average Revenue per Unit.",
                "Insert a Bar Chart from the pivot table.",
            ],
            "expectedOutput": "A pivot table + bar chart showing regional sales breakdown.",
            "hint": "Use Insert → PivotTable and drag fields into Rows / Values.",
        },
    },

    # ── Software Engineer ─────────────────────────────────────────────────────
    "Object-Oriented Programming": {
        "whatIsIt": "A programming paradigm organising code into objects — encapsulating data (attributes) and behaviour (methods) together.",
        "whyNeeded": "OOP makes large codebases maintainable, reusable and testable — essential for professional software development.",
        "careerConnection": "Software Engineers write OOP code daily. Understanding classes, inheritance and polymorphism is required for any backend, game or systems role.",
        "prerequisites": ["Python"],
        "learningSteps": ["Classes & Objects", "Inheritance", "Encapsulation", "Polymorphism"],
        "applicationTask": {
            "title": "Model a Library System with OOP",
            "objective": "Design a multi-class system representing Books, Members and a Library.",
            "difficulty": "Beginner",
            "estimatedTime": "1.5 hours",
            "steps": [
                "Create a Book class with title, author, isbn attributes and a __repr__ method.",
                "Create a Member class with name, member_id and a borrowed_books list.",
                "Create a Library class with a catalogue dict.",
                "Add checkout(member, isbn) and return_book(member, isbn) methods.",
                "Demonstrate checkout and return with 3 books and 2 members.",
            ],
            "expectedOutput": "Console log showing checkout and return operations with state changes.",
            "hint": "Use isinstance() to validate types before checkout.",
        },
    },
    "System Design": {
        "whatIsIt": "The process of defining the architecture, components and data flow of a large-scale software system.",
        "whyNeeded": "Building features that scale to millions of users requires deliberate design choices — databases, caching, load balancing, APIs.",
        "careerConnection": "Software Engineers and AI Engineers are evaluated on system design in interviews and rely on it daily to build reliable, scalable services.",
        "prerequisites": ["REST APIs", "Databases"],
        "learningSteps": ["Requirements Gathering", "High-Level Architecture", "Database Selection", "Scalability Patterns"],
        "applicationTask": {
            "title": "Design a URL Shortening Service",
            "objective": "Produce a written system design with diagrams for a URL shortener.",
            "difficulty": "Intermediate",
            "estimatedTime": "2 hours",
            "steps": [
                "List functional requirements: shorten URL, redirect, track clicks.",
                "Estimate traffic: 100 M URLs, 1 B redirects/day.",
                "Choose a database (SQL vs NoSQL) and justify.",
                "Draw a component diagram: client → API → cache → DB.",
                "Define the short URL encoding strategy (Base62).",
            ],
            "expectedOutput": "A 1-page design doc with a component diagram and justified decisions.",
            "hint": "Consider Redis for caching hot URLs to reduce DB load.",
        },
    },
    "Databases": {
        "whatIsIt": "Systems for storing, organising and retrieving structured or unstructured data — covering both SQL (relational) and NoSQL databases.",
        "whyNeeded": "Every application needs to persist data. Choosing the right database and designing schemas correctly determines performance and scalability.",
        "careerConnection": "Software Engineers design schemas, write queries, manage migrations and optimise slow queries throughout their careers.",
        "prerequisites": ["SQL"],
        "learningSteps": ["Relational Schema Design", "Indexing & Query Performance", "Transactions & ACID", "NoSQL Concepts"],
        "applicationTask": {
            "title": "Design and Query a Blog Database",
            "objective": "Create a normalised relational schema for a blogging platform and write complex queries.",
            "difficulty": "Beginner",
            "estimatedTime": "1.5 hours",
            "steps": [
                "Design tables: users, posts, comments, tags, post_tags.",
                "Create them in SQLite with proper foreign keys.",
                "Insert 3 users, 5 posts and 10 comments.",
                "Query: all posts with comment count, ordered by most commented.",
                "Query: all tags for a specific post.",
            ],
            "expectedOutput": "Query results showing posts ranked by comment count.",
            "hint": "LEFT JOIN posts p ON c.post_id = p.id; GROUP BY p.id",
        },
    },
    "Version Control (Git)": {
        "whatIsIt": "A distributed version control system tracking changes in files, enabling collaboration and safe experimentation.",
        "whyNeeded": "You must safely manage code changes without deleting history or breaking production — Git is non-negotiable in any professional team.",
        "careerConnection": "Software and ML Engineers use Git daily: pushing code, reviewing pull requests and resolving merge conflicts.",
        "prerequisites": [],
        "learningSteps": ["Commits & History", "Branching", "Pushing & Pulling", "Resolving Conflicts"],
        "applicationTask": {
            "title": "Feature Branch Workflow",
            "objective": "Simulate a real Git workflow with branches, commits and a merge.",
            "difficulty": "Beginner",
            "estimatedTime": "30 minutes",
            "steps": [
                "git init in a new folder.",
                "Create main.py, commit it to main.",
                "git checkout -b feature/login — add a login function, commit.",
                "Switch back to main.",
                "Merge the feature branch and resolve any conflict.",
                "Print git log --oneline --graph.",
            ],
            "expectedOutput": "A git log showing branching and merging history.",
            "hint": "git checkout -b <name> creates and switches to the branch.",
        },
    },
    "REST APIs": {
        "whatIsIt": "An architectural style for building web services using HTTP methods (GET, POST, PUT, DELETE) to expose and consume resources.",
        "whyNeeded": "REST APIs are the lingua franca of the web — every modern application communicates through them, whether mobile, frontend or microservices.",
        "careerConnection": "Software Engineers build and consume REST APIs daily. Full Stack Developers connect frontend UIs to backend services exclusively through APIs.",
        "prerequisites": ["Python"],
        "learningSteps": ["HTTP Methods & Status Codes", "JSON Serialisation", "Authentication (JWT)", "Versioning & Error Handling"],
        "applicationTask": {
            "title": "Build a Todo REST API",
            "objective": "Create a full CRUD REST API for a Todo list using FastAPI.",
            "difficulty": "Beginner",
            "estimatedTime": "1.5 hours",
            "steps": [
                "pip install fastapi uvicorn.",
                "Define a Todo model with id, title, completed.",
                "Create in-memory storage (a dict).",
                "Implement GET /todos, POST /todos, PUT /todos/{id}, DELETE /todos/{id}.",
                "Test all endpoints with curl or the built-in Swagger UI at /docs.",
            ],
            "expectedOutput": "A working CRUD API with 4 endpoints tested via Swagger UI.",
            "hint": "FastAPI auto-generates Swagger docs at http://localhost:8000/docs.",
        },
    },
    "Testing & Debugging": {
        "whatIsIt": "The practice of writing automated tests and using debugging tools to verify code correctness and find defects.",
        "whyNeeded": "Untested code is unreliable code. Automated tests catch regressions early and give confidence when refactoring.",
        "careerConnection": "Professional Software Engineers write unit tests, integration tests and use debuggers as core parts of daily development.",
        "prerequisites": ["Python"],
        "learningSteps": ["Unit Testing with pytest", "Mocking Dependencies", "Test-Driven Development", "Debugging with pdb"],
        "applicationTask": {
            "title": "Test a Shopping Cart with pytest",
            "objective": "Write a full pytest test suite for a simple shopping cart class.",
            "difficulty": "Beginner",
            "estimatedTime": "1 hour",
            "steps": [
                "Write a ShoppingCart class: add_item(), remove_item(), total().",
                "Write tests: add item, remove item, total calculation, remove non-existent item.",
                "Use pytest.raises() to test the error case.",
                "Run pytest -v and achieve 100 % pass rate.",
                "Add a parameterised test with 3 different quantities.",
            ],
            "expectedOutput": "pytest output showing all tests passing.",
            "hint": "pip install pytest; pytest.raises(ValueError)",
        },
    },

    # ── AI Engineer ───────────────────────────────────────────────────────────
    "Natural Language Processing": {
        "whatIsIt": "A subfield of AI focused on enabling computers to understand, interpret and generate human language.",
        "whyNeeded": "Text is the most abundant form of data. NLP powers chatbots, search engines, translation and content classification — all core AI products.",
        "careerConnection": "AI Engineers build NLP pipelines for tasks such as sentiment analysis, named-entity recognition and LLM-powered question answering.",
        "prerequisites": ["Python", "Machine Learning"],
        "learningSteps": ["Tokenisation & Text Preprocessing", "TF-IDF & Word Embeddings", "Transformer Models (BERT)", "Prompt Engineering"],
        "applicationTask": {
            "title": "Sentiment Classifier with HuggingFace",
            "objective": "Run a zero-shot sentiment analysis pipeline on movie reviews.",
            "difficulty": "Intermediate",
            "estimatedTime": "1.5 hours",
            "steps": [
                "pip install transformers torch.",
                "Load pipeline('sentiment-analysis') from HuggingFace.",
                "Classify 10 hard-coded movie reviews.",
                "Print the label and confidence score for each.",
                "Try pipeline('zero-shot-classification') with custom labels: Positive, Negative, Neutral.",
            ],
            "expectedOutput": "A printed table of review → label → confidence.",
            "hint": "from transformers import pipeline; classifier = pipeline('sentiment-analysis')",
        },
    },
    "Cloud Platforms": {
        "whatIsIt": "Web-based computing services (AWS, GCP, Azure) providing on-demand infrastructure, storage, AI services and managed databases.",
        "whyNeeded": "AI models need significant compute for training and serving. Cloud platforms provide scalable GPU instances and managed ML services.",
        "careerConnection": "AI Engineers deploy models to cloud platforms, configure auto-scaling inference endpoints and monitor cost and latency in production.",
        "prerequisites": ["Model Deployment", "REST APIs"],
        "learningSteps": ["Cloud Provider Basics (GCP/AWS)", "Object Storage (S3 / GCS)", "Managed ML Services (Vertex AI / SageMaker)", "Cost Management"],
        "applicationTask": {
            "title": "Deploy a Model to Google Cloud Run",
            "objective": "Containerise a FastAPI model server and deploy to Cloud Run.",
            "difficulty": "Advanced",
            "estimatedTime": "3 hours",
            "steps": [
                "Build a FastAPI app with a /predict endpoint.",
                "Write a Dockerfile: FROM python:3.11-slim, copy requirements, expose port 8080.",
                "Build the Docker image locally and test with docker run.",
                "Push the image to Google Container Registry (gcr.io).",
                "Deploy with gcloud run deploy and note the public HTTPS URL.",
            ],
            "expectedOutput": "A public URL returning predictions from your containerised model.",
            "hint": "Cloud Run auto-scales to zero — perfect for low-traffic demos.",
        },
    },
    "MLOps": {
        "whatIsIt": "A set of practices combining ML, DevOps and Data Engineering to reliably deploy and maintain ML models in production.",
        "whyNeeded": "Models degrade over time (data drift). MLOps provides the infrastructure to retrain, monitor and redeploy models automatically.",
        "careerConnection": "AI Engineers set up automated training pipelines, model registries and monitoring dashboards so models remain accurate in production.",
        "prerequisites": ["Model Deployment", "Cloud Platforms"],
        "learningSteps": ["Model Versioning (MLflow)", "CI/CD for ML Pipelines", "Data Drift Monitoring", "Feature Stores"],
        "applicationTask": {
            "title": "Track Experiments with MLflow",
            "objective": "Log multiple model experiments and compare them in the MLflow UI.",
            "difficulty": "Intermediate",
            "estimatedTime": "1.5 hours",
            "steps": [
                "pip install mlflow scikit-learn.",
                "Train 3 LogisticRegression models with different 'C' values.",
                "Use mlflow.log_param() and mlflow.log_metric() for each run.",
                "Launch the MLflow UI: mlflow ui.",
                "Compare runs and identify the best 'C' value.",
            ],
            "expectedOutput": "MLflow UI showing 3 runs with logged params and accuracy metrics.",
            "hint": "with mlflow.start_run(): wraps each experiment.",
        },
    },

    # ── Full Stack Developer ───────────────────────────────────────────────────
    "HTML & CSS": {
        "whatIsIt": "HTML structures web page content (elements, semantics) while CSS controls visual presentation (layout, colours, typography).",
        "whyNeeded": "Every web page starts with HTML and CSS. Without them you cannot build any user interface.",
        "careerConnection": "Full Stack Developers write HTML and CSS when building frontend views, fixing layout bugs or optimising for mobile devices.",
        "prerequisites": [],
        "learningSteps": ["HTML5 Semantic Elements", "CSS Box Model", "Flexbox & Grid", "Responsive Design"],
        "applicationTask": {
            "title": "Build a Responsive Portfolio Page",
            "objective": "Create a single-page portfolio using HTML and CSS Grid/Flexbox.",
            "difficulty": "Beginner",
            "estimatedTime": "2 hours",
            "steps": [
                "Create index.html with semantic elements: header, main, section, footer.",
                "Add a navigation bar with 3 links.",
                "Build a 3-column CSS Grid project gallery.",
                "Use Flexbox to centre the hero section vertically.",
                "Add a media query to collapse to 1 column on mobile.",
            ],
            "expectedOutput": "A responsive page that works on desktop and mobile.",
            "hint": "@media (max-width: 768px) { .grid { grid-template-columns: 1fr; } }",
        },
    },
    "JavaScript": {
        "whatIsIt": "The programming language of the web — runs in the browser (and on servers via Node.js) to make pages interactive.",
        "whyNeeded": "Every interactive element on a web page is driven by JavaScript. It is mandatory for any Full Stack Developer.",
        "careerConnection": "Full Stack Developers write JavaScript for both frontend logic (event handlers, fetch calls) and backend routes (Node.js / Express).",
        "prerequisites": ["HTML & CSS"],
        "learningSteps": ["Variables, Functions & Scope", "DOM Manipulation", "Promises & Async/Await", "ES6+ Features"],
        "applicationTask": {
            "title": "Build a Real-Time Todo App",
            "objective": "Create a vanilla JS todo app with add, complete and delete functionality.",
            "difficulty": "Beginner",
            "estimatedTime": "1.5 hours",
            "steps": [
                "Create index.html with an input, Add button and an empty <ul>.",
                "Write addTodo() that appends a <li> on button click.",
                "Add a click listener to each <li> to toggle a 'completed' CSS class.",
                "Add a Delete button inside each <li>.",
                "Persist the todo list to localStorage.",
            ],
            "expectedOutput": "A working todo app with add, complete and delete — persisted on refresh.",
            "hint": "document.getElementById('input').value; JSON.stringify() for localStorage.",
        },
    },
    "React": {
        "whatIsIt": "A JavaScript library for building fast, component-based user interfaces — maintained by Meta.",
        "whyNeeded": "React is the dominant frontend framework in industry. It makes building complex, stateful UIs manageable through reusable components.",
        "careerConnection": "Full Stack Developers use React to build the customer-facing side of products — dashboards, forms, real-time feeds.",
        "prerequisites": ["JavaScript"],
        "learningSteps": ["JSX & Components", "Props & State (useState)", "useEffect & Side Effects", "Component Composition"],
        "applicationTask": {
            "title": "Build a GitHub Profile Viewer",
            "objective": "Fetch and display GitHub user data using React hooks.",
            "difficulty": "Beginner",
            "estimatedTime": "2 hours",
            "steps": [
                "Create a Vite React project.",
                "Build a SearchBar component with controlled input.",
                "Use useEffect + fetch to call https://api.github.com/users/{username}.",
                "Display avatar, name, bio, followers and public repos.",
                "Show a loading spinner while fetching and an error message on failure.",
            ],
            "expectedOutput": "A React app displaying live GitHub profile data.",
            "hint": "useEffect(() => { fetch(...).then(r => r.json()).then(setUser) }, [username])",
        },
    },
    "Node.js": {
        "whatIsIt": "A JavaScript runtime built on Chrome's V8 engine — allows you to run JavaScript on the server side.",
        "whyNeeded": "Full Stack Developers use Node.js to write backend APIs in the same language as the frontend, reducing context switching.",
        "careerConnection": "Full Stack Developers build REST APIs, handle authentication and connect to databases using Node.js with Express or Fastify.",
        "prerequisites": ["JavaScript"],
        "learningSteps": ["Node.js Basics & npm", "Express.js Routing", "Middleware", "Environment Variables"],
        "applicationTask": {
            "title": "Build a REST API with Express",
            "objective": "Create a 4-route CRUD API for a 'notes' resource using Express.",
            "difficulty": "Beginner",
            "estimatedTime": "1.5 hours",
            "steps": [
                "npm init -y && npm install express.",
                "Create server.js with an in-memory notes array.",
                "Implement GET /notes, POST /notes, PUT /notes/:id, DELETE /notes/:id.",
                "Add express.json() middleware.",
                "Test all routes with curl or Postman.",
            ],
            "expectedOutput": "A running server with 4 working CRUD routes.",
            "hint": "app.use(express.json()); app.listen(3000)",
        },
    },
}


def _get_task_for_level(base_content: Dict[str, Any], skill: str, level: str) -> Dict[str, Any]:
    """Return the application task and learning steps appropriate for the given experience level."""
    overlay_skill = LEVEL_OVERLAYS.get(level, {}).get(skill, {})
    task = overlay_skill.get("applicationTask", base_content.get("applicationTask"))
    steps = overlay_skill.get("learningSteps", base_content.get("learningSteps", []))
    return task, steps


@app.post("/api/analyze")
async def analyze_skills(req: AnalysisRequest):
    target = req.targetCareer
    current = set(req.currentSkills)
    level = req.experienceLevel if req.experienceLevel in ("Beginner", "Intermediate", "Advanced") else "Beginner"

    if target not in CAREERS_DB:
        supported = sorted(CAREERS_DB.keys())
        raise HTTPException(
            status_code=422,
            detail={
                "error": f"Career '{target}' is not supported.",
                "supported_careers": supported,
            },
        )

    required: List[str] = CAREERS_DB[target]

    knownSkills = [r for r in required if r in current]
    missingSkills = [r for r in required if r not in current]
    # Skills the user knows that aren't in the required list (bonus)
    additionalKnown = [s for s in current if s not in required]
    allKnown = knownSkills + additionalKnown

    # Real numeric readiness (percentage of required skills already known)
    readinessPct: int = int((len(knownSkills) / len(required)) * 100) if required else 100

    if readinessPct > 75:
        readinessEstimate = "High"
    elif readinessPct > 40:
        readinessEstimate = "Medium"
    else:
        readinessEstimate = "Low"

    # Priority rules: first 2-3 skills in the roadmap are HIGH priority
    high_priority = set(required[:3])

    explanations = []
    for skill in missingSkills:
        base = FALLBACK_CONTENT.get(skill)
        priority = "HIGH" if skill in high_priority else "MEDIUM"

        if base:
            task, steps = _get_task_for_level(base, skill, level)
            entry = {
                "skill": skill,
                "priority": priority,
                "experienceLevel": level,
                "whatIsIt": base["whatIsIt"],
                "whyNeeded": base["whyNeeded"],
                "careerConnection": base["careerConnection"],
                "prerequisites": base.get("prerequisites", []),
                "learningSteps": steps,
                "applicationTask": task,
            }
        else:
            # Generic fallback for skills without curated content
            entry = {
                "skill": skill,
                "priority": priority,
                "experienceLevel": level,
                "whatIsIt": f"Core concept: {skill}.",
                "whyNeeded": f"{skill} is a required skill for {target}.",
                "careerConnection": f"Professionals in {target} use {skill} regularly.",
                "prerequisites": [],
                "learningSteps": ["Fundamentals", "Applied Practice", "Advanced Topics"],
                "applicationTask": {
                    "title": f"Explore {skill}",
                    "objective": f"Build hands-on familiarity with {skill}.",
                    "difficulty": {"Beginner": "Beginner", "Intermediate": "Intermediate", "Advanced": "Advanced"}[level],
                    "estimatedTime": "1 hour",
                    "steps": ["Set up your environment", "Follow official documentation", "Build a small project", "Review what you built"],
                    "expectedOutput": f"A small working demo using {skill}.",
                    "hint": "Refer to the official documentation for best practices.",
                },
            }
        explanations.append(entry)

    return {
        "targetCareer": target,
        "knownSkills": allKnown,
        "weakSkills": [],
        "missingSkills": missingSkills,
        "readinessEstimate": readinessEstimate,
        "readinessPct": readinessPct,          # ← real numeric value
        "experienceLevel": level,
        "skillExplanations": explanations,
        "roadmap": required,
    }



@app.get("/api/health")
async def health_check():
    return {"status": "ok", "careers": list(CAREERS_DB.keys())}


# ─── Skill alias table ────────────────────────────────────────────────────────
# Maps every detectable text variant (lowercase) → canonical skill name in CAREERS_DB.
# Longer / more-specific entries must come first to avoid shadowing sub-strings.
SKILL_ALIASES: Dict[str, str] = {
    # Mathematics
    "linear algebra": "Mathematics",
    "calculus": "Mathematics",
    "mathematics": "Mathematics",
    "math": "Mathematics",
    # Probability & Statistics
    "probability & statistics": "Probability & Statistics",
    "probability and statistics": "Probability & Statistics",
    "statistics": "Probability & Statistics",
    "probability": "Probability & Statistics",
    "statistical analysis": "Probability & Statistics",
    # Python
    "python": "Python",
    # SQL
    "sql": "SQL",
    "mysql": "SQL",
    "postgresql": "SQL",
    "sqlite": "SQL",
    # Data Structures & Algorithms
    "data structures & algorithms": "Data Structures & Algorithms",
    "data structures and algorithms": "Data Structures & Algorithms",
    "data structures": "Data Structures & Algorithms",
    "algorithms": "Data Structures & Algorithms",
    "dsa": "Data Structures & Algorithms",
    # Machine Learning
    "machine learning": "Machine Learning",
    "scikit-learn": "Machine Learning",
    "sklearn": "Machine Learning",
    "ml": "Machine Learning",
    # Deep Learning
    "deep learning": "Deep Learning",
    "neural network": "Deep Learning",
    "neural networks": "Deep Learning",
    "pytorch": "Deep Learning",
    "tensorflow": "Deep Learning",
    "keras": "Deep Learning",
    # Model Deployment
    "model deployment": "Model Deployment",
    "fastapi": "Model Deployment",
    "flask": "Model Deployment",
    "docker": "Model Deployment",
    "kubernetes": "Model Deployment",
    # Data Wrangling
    "data wrangling": "Data Wrangling",
    "pandas": "Data Wrangling",
    "data cleaning": "Data Wrangling",
    "data preprocessing": "Data Wrangling",
    "numpy": "Data Wrangling",
    # EDA
    "exploratory data analysis": "Exploratory Data Analysis",
    "eda": "Exploratory Data Analysis",
    # Data Visualization
    "data visualization": "Data Visualization",
    "data visualisation": "Data Visualization",
    "matplotlib": "Data Visualization",
    "seaborn": "Data Visualization",
    "plotly": "Data Visualization",
    "power bi": "Data Visualization",
    "tableau": "Data Visualization",
    # Storytelling with Data
    "storytelling with data": "Storytelling with Data",
    "data storytelling": "Storytelling with Data",
    # Business Intelligence Tools
    "business intelligence": "Business Intelligence Tools",
    "bi tools": "Business Intelligence Tools",
    "looker": "Business Intelligence Tools",
    "metabase": "Business Intelligence Tools",
    # Excel
    "excel": "Excel",
    "microsoft excel": "Excel",
    "spreadsheet": "Excel",
    # OOP
    "object-oriented programming": "Object-Oriented Programming",
    "object oriented programming": "Object-Oriented Programming",
    "oop": "Object-Oriented Programming",
    # System Design
    "system design": "System Design",
    # Databases
    "databases": "Databases",
    "database design": "Databases",
    "mongodb": "Databases",
    "redis": "Databases",
    "nosql": "Databases",
    # Version Control (Git)
    "version control (git)": "Version Control (Git)",
    "version control": "Version Control (Git)",
    "git": "Version Control (Git)",
    "github": "Version Control (Git)",
    "gitlab": "Version Control (Git)",
    # REST APIs
    "rest apis": "REST APIs",
    "rest api": "REST APIs",
    "restful": "REST APIs",
    "api development": "REST APIs",
    # Testing & Debugging
    "testing & debugging": "Testing & Debugging",
    "testing and debugging": "Testing & Debugging",
    "unit testing": "Testing & Debugging",
    "pytest": "Testing & Debugging",
    "debugging": "Testing & Debugging",
    # NLP
    "natural language processing": "Natural Language Processing",
    "nlp": "Natural Language Processing",
    "huggingface": "Natural Language Processing",
    "transformers": "Natural Language Processing",
    "bert": "Natural Language Processing",
    # Cloud Platforms
    "cloud platforms": "Cloud Platforms",
    "aws": "Cloud Platforms",
    "gcp": "Cloud Platforms",
    "azure": "Cloud Platforms",
    "google cloud": "Cloud Platforms",
    "amazon web services": "Cloud Platforms",
    "cloud computing": "Cloud Platforms",
    # MLOps
    "mlops": "MLOps",
    "mlflow": "MLOps",
    "kubeflow": "MLOps",
    "model monitoring": "MLOps",
    # HTML & CSS
    "html & css": "HTML & CSS",
    "html and css": "HTML & CSS",
    "html": "HTML & CSS",
    "css": "HTML & CSS",
    # JavaScript
    "javascript": "JavaScript",
    "typescript": "JavaScript",
    "es6": "JavaScript",
    # React
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    # Node.js
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "express": "Node.js",
    "express.js": "Node.js",
}

# Sort aliases by length descending so longer terms match before shorter substrings
_SORTED_ALIASES = sorted(SKILL_ALIASES.keys(), key=len, reverse=True)

_MAX_PDF_SIZE = 5 * 1024 * 1024  # 5 MB


def _extract_skills_from_text(text: str) -> List[str]:
    """Return unique canonical skill names found in `text` (case-insensitive)."""
    lower = text.lower()
    found: Dict[str, bool] = {}
    for alias in _SORTED_ALIASES:
        # Match alias as a whole word / phrase to avoid partial hits
        pattern = r'(?<![\w.])' + re.escape(alias) + r'(?![\w.])'
        if re.search(pattern, lower):
            canonical = SKILL_ALIASES[alias]
            found[canonical] = True
    return sorted(found.keys())


def _extract_sections(text: str) -> Dict[str, str]:
    """Extract education, projects, certifications sections from resume text."""
    section_patterns = [
        ("education", r'(?i)\b(education|academic|qualification)\b'),
        ("projects", r'(?i)\b(projects?|work experience|experience)\b'),
        ("certifications", r'(?i)\b(certifications?|certificates?|credentials?)\b'),
    ]
    result: Dict[str, str] = {}
    lines = text.splitlines()
    current_section: Optional[str] = None
    buffer: List[str] = []

    for line in lines:
        stripped = line.strip()
        matched = False
        for sec_name, pattern in section_patterns:
            if re.match(pattern, stripped) and len(stripped) < 60:
                if current_section and buffer:
                    result[current_section] = "\n".join(buffer).strip()
                current_section = sec_name
                buffer = []
                matched = True
                break
        if not matched and current_section:
            buffer.append(stripped)

    if current_section and buffer:
        result[current_section] = "\n".join(buffer).strip()

    return result


@app.post("/api/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """Extract skills from an uploaded PDF resume.
    Returns matched canonical skills, detected sections, and a short summary.
    Does NOT store the file permanently.
    """
    if not _PYMUPDF_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Resume parsing is unavailable — PyMuPDF not installed on this server.",
        )

    # ── Validate file type ────────────────────────────────────────────────────
    if file.content_type not in ("application/pdf", "application/x-pdf"):
        # Some browsers send octet-stream; check filename extension as fallback
        if not (file.filename or "").lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are accepted. Please upload a .pdf file.",
            )

    # ── Read and validate size ────────────────────────────────────────────────
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(content) > _MAX_PDF_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is 5 MB.",
        )

    # Parse in memory so Windows does not lock a temp path. Bytes are never saved.
    doc = None
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            doc = pymupdf.open(stream=content, filetype="pdf")
        except Exception as exc:
            raise HTTPException(
                status_code=422,
                detail=f"Could not open PDF: {type(exc).__name__}: {exc}",
                )

        if getattr(doc, "is_encrypted", False):
            raise HTTPException(
                status_code=422,
                detail="Could not open the PDF. The file may be corrupted or password-protected.",
            )

        if doc.page_count == 0:
            raise HTTPException(status_code=422, detail="The PDF has no pages.")

        full_text = ""
        for page in doc:
            full_text += page.get_text() or ""

        if not full_text.strip():
            raise HTTPException(
                status_code=422,
                detail=(
                    "No text could be extracted. This PDF may be scanned or image-based. "
                    "Please upload a text-based PDF."
                ),
            )
    finally:
        if doc is not None:
            try:
                doc.close()
            except Exception:
                pass
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    # ── Extract skills and sections ───────────────────────────────────────────
    matched_skills = _extract_skills_from_text(full_text)
    sections = _extract_sections(full_text)

    # Build a brief summary: first non-empty line(s) up to 300 chars
    summary_lines = [l.strip() for l in full_text.splitlines() if l.strip()][:5]
    summary = " | ".join(summary_lines)[:300]

    return {
        "filename": file.filename,
        "extractedSkills": matched_skills,
        "sections": sections,
        "summary": summary,
        "charCount": len(full_text),
    }


def _skill_token(skill: str) -> str:
    return skill.lower().replace("&", "and").replace("(", "").replace(")", "").replace(" ", "_")


def _recommend_from_skills(current_skills: List[str], top_n: int = 3) -> List[Dict[str, Any]]:
    """Rank careers by TF-IDF cosine similarity of confirmed skills vs career skill lists."""
    unique_skills = [s for i, s in enumerate(current_skills) if s and s not in current_skills[:i]]
    if not unique_skills:
        raise HTTPException(status_code=400, detail="Add at least one skill before requesting career suggestions.")

    career_names = list(CAREERS_DB.keys())
    skill_set = set(unique_skills)

    if _SKLEARN_AVAILABLE:
        career_docs = [" ".join(_skill_token(s) for s in CAREERS_DB[name]) for name in career_names]
        user_doc = " ".join(_skill_token(s) for s in unique_skills)
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(career_docs + [user_doc])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    else:
        scores = []
        user_tokens = {_skill_token(s) for s in unique_skills}
        for name in career_names:
            career_tokens = {_skill_token(s) for s in CAREERS_DB[name]}
            denom = (len(user_tokens) * len(career_tokens)) ** 0.5
            overlap = len(user_tokens & career_tokens)
            scores.append(overlap / denom if denom else 0.0)

    ranked = sorted(zip(career_names, scores), key=lambda item: item[1], reverse=True)[:top_n]
    recommendations = []
    for name, score in ranked:
        required = CAREERS_DB[name]
        recommendations.append({
            "career": name,
            "similarityScore": round(float(score), 4),
            "matchingSkills": [s for s in required if s in skill_set],
            "missingSkills": [s for s in required if s not in skill_set],
        })
    return recommendations


@app.post("/api/recommend")
async def recommend_careers(req: RecommendRequest):
    return {
        "recommendations": _recommend_from_skills(req.currentSkills),
        "method": "tfidf_cosine" if _SKLEARN_AVAILABLE else "token_overlap_cosine",
        "note": "Scores measure skill-list similarity, not hiring probability.",
    }

