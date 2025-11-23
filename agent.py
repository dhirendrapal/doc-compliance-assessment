# agent.py — CLEAN, CORRECT, SINGLE-PARAGRAPH AI AGENT

import json
from typing import List, Dict, Any
import language_tool_python
from openai_client import llm_chat, OPENAI_MODEL


# ----------------------------------------------------------------------
# 1. LANGUAGE TOOL (local preferred)
# ----------------------------------------------------------------------
try:
    tool = language_tool_python.LanguageTool(
        "en-US",
        remote_server="http://localhost:8081"
    )
except Exception:
    tool = language_tool_python.LanguageTool("en-US")


# ----------------------------------------------------------------------
# 2. LLM PROMPT FOR PARAGRAPH ANALYSIS
# ----------------------------------------------------------------------
PARAGRAPH_PROMPT = """
You are an English compliance agent. Evaluate ONLY the paragraph provided.

Guidelines:
1) Use active voice where possible.
2) Keep sentences typically under 25 words.
3) Use formal, professional tone.
4) Avoid ambiguous pronouns.
5) Preserve meaning; do not add facts.
6) Maintain correctness of names, numbers, dates.

Input paragraph:
\"\"\"{text}\"\"\"

LanguageTool issues:
{lt_json}

Return STRICT JSON:
{{
  "sentences": [
    {{
      "orig": "...",
      "violations": ["grammar","clarity","tone"],
      "explanation": "...",
      "suggested": "..."
    }}
  ],
  "rewritten": "corrected paragraph only",
  "chunk_score": 0.0
}}
"""


# ----------------------------------------------------------------------
# 3. APPLY LLM TO SINGLE PARAGRAPH
# ----------------------------------------------------------------------
def analyze_paragraph_with_llm(text: str, lt_issues: List[Dict]) -> Dict:
    filled_prompt = PARAGRAPH_PROMPT.format(
        text=text,
        lt_json=json.dumps(lt_issues, ensure_ascii=False)
    )

    raw = llm_chat(filled_prompt, model=OPENAI_MODEL, max_tokens=1000)

    try:
        return json.loads(raw)
    except Exception:
        # fallback in case LLM returns non-JSON
        return {
            "sentences": [],
            "rewritten": text,
            "chunk_score": 1.0,
            "parse_raw": raw
        }


# ----------------------------------------------------------------------
# 4. MAIN ANALYZER (PER PARAGRAPH)
# ----------------------------------------------------------------------
def analyze_paragraphs(paragraphs: List[Dict[str, Any]]) -> Dict:
    results = []
    total_score = 0.0

    for p in paragraphs:
        text = p["text"]

        # --- A: LanguageTool ---
        lt_matches = tool.check(text)
        lt_json = []
        for m in lt_matches:
            lt_json.append({
                "rule_id": getattr(m, "rule_id", None),
                "message": m.message,
                "offset": m.offset,
                "length": getattr(m, "error_length", getattr(m, "errorLength", None)),
                "replacements": getattr(m, "replacements", [])
            })

        # --- B: LLM ---
        llm_data = analyze_paragraph_with_llm(text, lt_json)

        # --- C: Score calculation ---
        lt_penalty = len(lt_json) / max(1, len(text.split()) / 5)
        llm_score = float(llm_data.get("chunk_score", 1.0))
        final_score = max(0.0, min(1.0, (1.0 - lt_penalty) * llm_score))

        results.append({
            "text": text,
            "language_tool": lt_json,
            "llm": llm_data,
            "score": round(final_score, 3)
        })

        total_score += final_score

    overall_score = round((total_score / max(1, len(results))) * 100, 2)

    return {
        "overall_score": overall_score,
        "paragraphs": results
    }
