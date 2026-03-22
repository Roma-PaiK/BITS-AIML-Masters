````md id="k9d42p"
# Assignment 1: Problem Statement 9 (PS9)

## 📝 Problem Statement
This repository contains the deliverables for **Assignment 1 (Problem Statement 9)** for the course **AIMLCZG519**. The project involves a full-stack implementation along with comprehensive academic research, including a literature survey and enhancement documentation.

**Course:** AIMLCZG519 - BITS Pilani
**Team:** Group 65

## 🚀 Version 1.0 Implementation (Current)
This submission represents our complete Version 1.0 system. It features a decoupled architecture with a Python-based backend and a modern React frontend powered by Vite. 

**Key Project Components:**
* **Backend (`app.py`):** The core application logic and API endpoints handling the primary computational tasks.
* **Frontend (`src/`):** A lightweight, high-performance web interface built with React (`.jsx`), utilizing custom UI components (cards, inputs, scroll-areas) and a modular component architecture (Chat, Search, References).
* **Literature Survey:** A detailed academic review of existing methodologies and state-of-the-art approaches related to our problem domain.
* **Enhancement Documentation:** A comprehensive guide detailing the optimizations, custom improvements, and architectural decisions made beyond the baseline requirements.

## 📂 Repository Structure
```text
├── src/                                                                   # React frontend source code
│   ├── assets/                                                            # Static assets (images, icons)
│   ├── components/                                                        # Reusable React components
│   │   ├── ui/                                                            # Base UI elements
│   │   │   ├── card.jsx
│   │   │   ├── input.jsx
│   │   │   └── scroll-area.jsx
│   │   ├── ChatMessage.jsx                                                # Chat interface component
│   │   ├── Header.jsx                                                     # Application header
│   │   ├── ReferencePanel.jsx                                             # Document/reference display
│   │   └── SearchBar.jsx                                                  # Query input component
│   ├── App.jsx                                                            # Main React application component
│   ├── index.css                                                          # Global styles
│   └── main.jsx                                                           # React DOM rendering entry point
├── .gitignore                                                             # Git ignored files configuration
├── app.py                                                                 # Python backend server
├── Assignment-1_PS9 (1).pdf                                               # Original assignment problem statement
├── eslint.config.js                                                       # ESLint configuration for code quality
├── index.html                                                             # Main HTML template
├── package-lock.json                                                      # Locked npm dependencies
├── package.json                                                           # Node.js dependencies and scripts
├── README.md                                                              # Project documentation
├── requirements.txt                                                       # Python backend dependencies
├── S1_25_AIMLCZG519_Group_65_Assignment_1_Enhancement_Documentation.pdf   # System improvements & architecture details
├── S1_25_AIMLCZG519_Group_65_Assignment_1_Literature_Survey.pdf           # Research & literature review
└── vite.config.js                                                         # Vite bundler configuration
🛠️ How to Run (Setup & Execution)
1. Backend Setup (Python)
Ensure you have Python installed on your system.

Bash
# Create and activate a virtual environment (Recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt 

# Run the backend server
python app.py
2. Frontend Setup (React & Vite)
Ensure you have Node.js installed on your system.

Bash
# Install required npm packages
npm install

# Start the Vite development server
npm run dev
🌱 Planned Improvements (V2.0)
[ ] Refactor the backend API endpoints for better error handling and response formatting.

[ ] Expand the frontend UI to include loading states and better error surfacing.

[ ] Add unit tests for both the React components and Python functions.
````
