# doc-compliance-assessment
**Doc Compliance Assessment** is an AI-powered document analysis and correction system built with **FastAPI**, **OpenAI GPT**, and **LanguageTool** (local grammar engine).

**Prerequisites**
1. Python 3.10+
   
```sudo apt install python3 python3-venv python3-pip```

2. Java 17+ (for local LanguageTool)

```sudo apt install openjdk-17-jre```
```java -version```

You must see something like:

openjdk version "17.x.x"

🟦 **Setup & Installation**
1. Create Virtual Environment
```uv venv --python=3.10```
```source .venv/bin/activate```

2. Install Dependencies
```uv pip install -r requirements.txt```

🗝 **Environment Variables (Required)**

Create .env in the project root:

```OPENAI_API_KEY=your_api_key_here``` 

**Run LanguageTool with Java (Manual)**
```wget https://languagetool.org/download/LanguageTool-stable.zip```

```unzip LanguageTool-stable.zip```

```cd LanguageTool-*/```

```java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081```

Verify server is running:

```curl http://localhost:8081/v2/languages```

Should return JSON.

▶️ **Run FastAPI Application**

After LanguageTool is running:

```uvicorn app:app --reload```

API will be available at:

👉 http://127.0.0.1:8000

👀 Swagger UI: http://127.0.0.1:8000/docs

🧪 **Unit Tests**

Run:
```pytest -v```
