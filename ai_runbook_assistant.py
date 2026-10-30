import ollama

MODEL_NAME = "qwen2.5-coder:7b"

print("Loading internal company runbooks...")
with open("database_runbook.md", "r") as f:
    runbook_content = f.read()

# Simulate an on-call engineer asking a question during an incident
engineer_query = "Help! I am seeing database connection timeout errors and high CPU. What commands should I run to find runaway queries, and can I restart the database?"

prompt = f"""
You are an expert SRE on-call assistant. 
You must answer the engineer's question USING ONLY the provided runbook below. 
If the answer is in the runbook, give clear step-by-step instructions and explicitly highlight any safety warnings (like what NOT to do).

--- RUNBOOK CONTENT ---
{runbook_content}
--- END OF RUNBOOK ---

Engineer's Question: {engineer_query}
"""

print(f"Querying local model ({MODEL_NAME}) with runbook context...\n")

response = ollama.chat(model=MODEL_NAME, messages=[
    {
        "role": "system",
        "content": "You are a precise, safety-conscious SRE assistant that strictly follows internal documentation."
    },
    {
        "role": "user",
        "content": prompt
    },
])

print("=== AI RUNBOOK ASSISTANT RESPONSE ===")
print(response['message']['content'])