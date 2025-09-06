from ..scripts.commit_agent import CommitAgent
def test_critique_identifies_issues():
    agent = CommitAgent()
    critiques = agent.critique(["fix bug"])
    assert critiques == ["'fix bug' -> too short, should start with uppercase, should end with period"]


def test_critique_accepts_good_message():
    agent = CommitAgent()
    critiques = agent.critique(["Good message."])
    assert critiques == []


def test_critique_flags_long_message():
    agent = CommitAgent()
    long_msg = "A" * 73 + "."
    critiques = agent.critique([long_msg])
    assert any("too long" in c for c in critiques)
