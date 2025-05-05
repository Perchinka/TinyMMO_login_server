from login_server.crypto.challenge import ChallengeManager

def test_generate_challenge_returns_string():
    cm = ChallengeManager()
    challenge = cm.generate_challenge("user1")
    assert isinstance(challenge, str)
    assert challenge != ""

def test_retrieve_challenge_matches_generated():
    cm = ChallengeManager()
    cm.generate_challenge("user2")
    stored = cm.get_challenge("user2")
    assert stored == cm._challenges["user2"]

def test_generate_challenge_overwrites_previous():
    cm = ChallengeManager()
    first = cm.generate_challenge("user3")
    second = cm.generate_challenge("user3")
    assert first != second
    assert cm.get_challenge("user3") == second

