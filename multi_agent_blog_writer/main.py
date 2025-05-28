# main.py
from dotenv import load_dotenv
load_dotenv()
from agents.planner_agent import plan_steps
from agents.writer_agent import write_paragraph, generate_text
from agents.editor_agent import optimize_content
import os

def main():
    print("🤖 Multi-Agent Blog Writer\n")
    task = input("Enter the blog topic: ")

    # Generate blog title and meta description
    title = generate_text(f"Generate a catchy blog title for a blog on: {task}", max_tokens=20)
    meta = generate_text(f"Write a 2-sentence meta description for a blog on: {task}", max_tokens=50)

    print(f"\n📰 Title: {title}")
    print(f"📝 Meta Description: {meta}\n")

    print(f"\n🧠 Planning steps for: '{task}'")
    steps = plan_steps(task)

    final_output = []

    for i, step in enumerate(steps, 1):
        print(f"\n✍️ Writing Step {i}: {step}")
        paragraph = write_paragraph(step, task)

        print(f"🛠️ Optimizing Step {i}")
        optimized = optimize_content(paragraph)

        final_output.append(optimized)

    # Summarize the full blog
    full_blog = "\n\n".join(final_output)
    summary = generate_text(f"Summarize this blog in one paragraph:\n{full_blog}", max_tokens=100)
    final_output.append(f"**Summary:** {summary}")

    print("\n📄 Final Blog:\n")
    print("\n\n".join(final_output))

    # Save the blog content to a file
    output_dir = os.path.dirname(__file__)
    safe_topic = task.strip().replace(" ", "_").lower()
    filename = os.path.join(output_dir, f"{safe_topic}_blog.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Meta:** {meta}\n\n")
        f.write("\n\n".join(final_output))
    print(f"✅ Blog content saved to {filename}")

if __name__ == "__main__":
    main()