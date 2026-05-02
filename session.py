import time

def create_session() -> str:
    """Create a session return the session_id"""
    return f"session_{int(time.time())}"

print(create_session())