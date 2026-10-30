import ollama

MODEL_NAME = "qwen2.5-coder:7b"

print("Reading noisy system logs...")
with open("noisy_logs.txt", "r") as f:
    log_data = f.read()

# Prompt crafted for SRE noise reduction & root-cause analysis
prompt = f"""
You are an expert Site Reliability Engineer (SRE). 
I am feeding you a noisy block of application logs that triggered a flood of alerts. 
Please analyze these logs and provide a clean incident summary with:
1. **Root Cause Analysis:** What actually broke first? (Ignore downstream cascading noise).
2. **Alert Summary & Noise Reduction:** Group the duplicate errors into a single count instead of listing every line.
3. **Recommended Immediate Action:** What should the on-call engineer check or restart?

Here are the logs:
{log_data}
"""

print(f"Sending logs to local model ({MODEL_NAME}) for intelligent parsing...\n")

response = ollama.chat(model=MODEL_NAME, messages=[
    {
        "role": "system",
        "content": "You are a pragmatic, concise SRE assistant focused on reducing alert fatigue and finding root causes quickly."
    },
    {
        "role": "user",
        "content": prompt
    },
])

print("=== AI SRE INCIDENT REPORT ===")
print(response['message']['content'])