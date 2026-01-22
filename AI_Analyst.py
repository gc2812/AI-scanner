import sys
import time
import keyring
import pdfplumber
from pathlib import Path
from openai import OpenAI, APIError, RateLimitError, AuthenticationError

class AI_Analyst():
	#Initializes class and common variables
	def __init__(self, model): 
		self.model = model
		self.api_key = keyring.get_password("AI_Analyst","OpenAI")
		if not self.api_key:
			raise RuntimeError("OpenAI ERROR: keyring vault is missing the OpenAI API token")

	#extracts artifact text from provided filepath, handles PDFs
	def load_artifact(self, artifact_path):
		if artifact_path.exists() == False:
			raise RuntimeError("OpenAI ERROR: Artifact file path does not exist.")
		try:
			if artifact_path.suffix.lower() == ".pdf":
				with pdfplumber.open(artifact_path) as pdf:
					artifact_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
			else:
				artifact_text = artifact_path.read_text(encoding="utf-8", errors="ignore")
		except Exception as e:
			raise RuntimeError(f"OpenAI ERROR: Unable to read text from artifact file ({e})")
		return artifact_text

	#uses template to create prompt from the artifact text
	def build_prompt(self, artifact_text):
		prompt = f"""
You are an AI Security Analyst on a purple team.

Analyze the following security artifact and help a human analyst by:
- Identifying suspicious or malicious behavior
- Highlighting vulnerabilities or misconfigurations
- Correlating possible attacker activity or attack paths
- Calling out unknown or anomalous behavior
- Recommending next investigative steps

Respond with:
1) Executive summary
2) Key findings (severity + reasoning)
3) Possible attack paths or correlations
4) Gaps / assumptions
5) Recommended next steps

Artifact contents:
{artifact_text}
""".strip()
		if len(prompt) > 100000:
			raise RuntimeError("OpenAI ERROR: prompt is too long, may exceed API limit")
		return prompt

	#sends prompt to OpenAI and handles the response
	def send_prompt(self, prompt):
		client = OpenAI(api_key=self.api_key)
		try:
			response = client.responses.create(model=self.model, input=prompt,)
		except AuthenticationError:
			raise RuntimeError("OpenAI ERROR: issue with key") from None
		except RateLimitError:
			raise RuntimeError("OpenAI ERROR: rate limit exceeded") from None
		except Exception as e:
			raise RuntimeError(f"OpenAI ERROR: {e}") from None
		if not response.output_text or not response.output_text.strip():
			raise RuntimeError("OpenAI ERROR: LLM response was empty")
		return response.output_text

def main():
	start = time.time()
	if len(sys.argv) < 2:
		print("ERROR: Missing artifact file path argument.")
		sys.exit(-1)
	path = Path(sys.argv[1])
	AI = AI_Analyst("gpt-5.2")
	artifact_text = AI.load_artifact(path)
	prompt = AI.build_prompt(artifact_text)
	analysis = AI.send_prompt(prompt)
	end = time.time()
	output_file = f"./{path.stem}_ANALYSIS.txt"
	print(f"AI analysis took {round(end-start,1)} seconds, output written to {output_file}.")
	try:
		with open(output_file, "w", encoding="utf-8") as f:
			print(analysis, file=f)
	except Exception as e:
		print(f"ERROR: unable to output results to file, {e}")

if __name__ == "__main__":
	main()