# Assignment: Classical Acoustic Modeling using GMM-HMM

## 📝 Problem Statement
This repository contains the implementation for simulating a classical Automatic Speech Recognition (ASR) pipeline using GMM-HMM architectures. Grounded in the industry domain of **Call Center Analytics and Quality Monitoring**, this project aims to process recorded speech audio for downstream transcription, simulating the lightweight acoustic models often required for high-volume customer call analysis.

**Team:** Group 3  
**Data Source:** LibriSpeech (clean subset)

## 🚀 Version 1.0 Implementation (Current)
This submission represents the complete implementation of the five core assignment tasks, combining acoustic modeling with language and lexicon constraints.

**Key Pipeline Tasks Completed:**
* **Task 1: Speech Data Loading and Visualization:** Implemented audio ingestion and generated waveform and spectrogram plots to simulate industry-standard data quality checks and noise analysis.
* **Task 2: Acoustic Feature Extraction:** Extracted Mel-Frequency Cepstral Coefficients (MFCCs) to compactly represent the speech signals and reduce raw audio complexity.
* **Task 3: Acoustic Modeling:** Trained Gaussian Mixture Models (GMM) and Hidden Markov Models (HMM) to compute log-likelihoods, bridging the gap between acoustic features and phonetic likelihoods.
* **Task 4: Language Model Usage:** Built a Bigram Language Model to compute sentence probabilities, demonstrating how grammatical and contextual constraints improve transcription accuracy.
* **Task 5: Lexicon Integration:** Integrated the CMU Pronouncing Dictionary to map words to their phoneme sequences, ensuring robust handling of domain-specific pronunciations.

## 📂 Repository Structure
```text
├── Speech_Processing_2.ipynb                   # Main implementation notebook containing all 5 tasks and inline explanations
├── Speech Processing_2.ipynb_Group_3.pdf       # Exported technical report and visual results document
└── README.md                                   # Project documentation
🛠️ How to Run (Setup & Execution)
1. Dependencies
This project requires Python and standard speech processing, machine learning, and NLP libraries. Expected dependencies include:
numpy, matplotlib, librosa, hmmlearn, nltk (for the bigram LM and CMU dict), scikit-learn, and scipy.

2. Installation
Bash
# Create and activate a virtual environment (Recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the required packages
pip install numpy matplotlib librosa hmmlearn nltk scikit-learn scipy jupyter
(Note: You will also need to download the CMU dictionary corpus via NLTK by running import nltk; nltk.download('cmudict') within your Python environment).

3. Execution
Launch Jupyter Notebook from your terminal:

Bash
jupyter notebook
Open Speech_Processing_2.ipynb.

Ensure any required LibriSpeech audio samples are accessible in the notebook's working directory.

Run the cells sequentially to visualize the audio, extract features, and train the classical ASR components.

🌱 Planned Improvements (V2.0)
[ ] Encapsulate the GMM-HMM training loop into reusable Python classes for easier scaling and hyperparameter tuning.

[ ] Expand the Bigram Language Model to a Trigram or N-gram model for improved contextual accuracy.

[ ] Implement an evaluation metric (like Word Error Rate - WER) to quantify the end-to-end performance of the simulated ASR pipeline.