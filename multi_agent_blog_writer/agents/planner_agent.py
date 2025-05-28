import os

def plan_steps(topic):
    """
    Break down a blog topic into logical writing steps.
    If a topic-specific file exists, use its content as steps.
    Otherwise, use a default structure.
    """
    safe_topic = topic.strip().replace(" ", "_").lower()
    filename = f"{safe_topic}_blog.txt"

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            steps = [line.strip() for line in f if line.strip()]
        return steps

    # Default structure
    return [
        f"Introduction to {topic}",
        f"Key concepts and background of {topic}",
        f"Main discussion points about {topic}",
        f"Real-world applications or examples of {topic}",
        f"Conclusion and future outlook on {topic}"
    ]