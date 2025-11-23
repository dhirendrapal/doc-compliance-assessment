from agent import analyze_paragraphs

def test_agent_basic():
    paragraphs = [{"text": "I goes to school daily."}]
    report = analyze_paragraphs(paragraphs)

    assert "overall_score" in report
    assert len(report["paragraphs"]) == 1
    assert "llm" in report["paragraphs"][0]
    assert "rewritten" in report["paragraphs"][0]["llm"]
