import ollama

MODEL_NAME = "qwen2.5-coder:7b"

# Simulate the data an SRE investigation tool would pull during an outage
incident_context = """
[INCIDENT METRICS & TELEMETRY AT 02:11 UTC]
- Alert Triggered: High Error Rate on CheckoutAPI (HTTP 500 spike > 15%)
- Recent Deployments: 'PaymentService v2.1.4' deployed 12 minutes ago by CI/CD pipeline.
- Infrastructure Health: 
  - Kubernetes Pods: payment-service-7b89f (Restart Count: 3, Status: CrashLoopBackOff)
  - Database CPU Usage: 45% (Normal)
  - Redis Cache Hit Rate: 99.1% (Normal)
- Recent Error Log Snippet: 
  "NullPointerException in PaymentService.processPayment(): merchant_config is null after config reload."
"""

prompt = f"""
You are an expert SRE Incident Commander AI. 
Analyze the following automated investigation telemetry gathered during a production incident. 
Provide a rapid triage report covering:
1. **Blast Radius:** Which specific services, components, or user flows are impacted?
2. **Likely Culprit & Timeline:** Based on the recent deployment and error logs, what likely caused this?
3. **Recommended Next Steps:** What are the exact diagnostic or rollback commands the engineer should take right now?

Here is the telemetry data:
{incident_context}
"""

print("Running automated SRE incident investigation...\n")

response = ollama.chat(model=MODEL_NAME, messages=[
    {
        "role": "system",
        "content": "You are a fast, decisive SRE incident commander assistant."
    },
    {
        "role": "user",
        "content": prompt
    },
])

print("=== AUTOMATED INVESTIGATION REPORT ===")
print(response['message']['content'])