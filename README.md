# AI-scanner
AI_Analyst – AI-Assisted Security Artifact Analyzer

A simple lightweight Python script that ingests a security artifact 
(such as a vulnerability scan report or log file), 
extracts its text, and uses a Large Language Model (LLM) to generate 
a clear, human-readable security analysis for a purple-team analyst.

DESIGN OVERVIEW
- Ingest a security artifact from disk
- Normalize the artifact into text (handles PDF text extraction)
- Build a structured "AI Security Analyst" prompt
- Send the prompt to an LLM via API
- Output a single analyst-friendly report

FEATURES
- Accepts PDF and text-based security artifacts
- Local PDF text extraction using pdfplumber
- Structured analyst-style prompt
- OpenAI API integration via the official Python SDK
- Explicit handling of authentication and quota errors
- UTF-8 encoded output to avoid Windows character issues
- Minimal dependencies and simple execution flow

REQUIREMENTS
- Python 3.10+
- OpenAI API key
- Internet access for API calls

INSTALLATION
- pip install -r requirements.txt

API KEY SETUP (KEYRING)
- The script retrieves the OpenAI API key securely from the operating system keyring.
- Set the key once using Python:
	import keyring
	keyring.set_password("AI_Analyst", "OpenAI", "sk-...")

USAGE
- python AI_Analyst.py <path_to_artifact>
- Example:
	python AI_Analyst.py SampleNetworkVulnerabilityScanReport.pdf

OUTPUT
- <artifact_name>_ANALYSIS.txt
