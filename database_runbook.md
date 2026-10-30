# Runbook: Handling Database Connection Exhaustion (INC-DB-01)

## Symptoms
- Applications throwing `ConnectionTimeoutException` or HTTP 500 errors.
- Database CPU utilization spikes above 85%.

## Troubleshooting Steps
1. **Check Active Connections:** Run the following SQL query to see active sessions:
   `SELECT count(*), state FROM pg_stat_activity GROUP BY state;`
2. **Identify Runaway Queries:** Look for queries running longer than 60 seconds:
   `SELECT pid, query, age(clock_timestamp(), query_start) FROM pg_stat_activity WHERE state = 'active' AND age(clock_timestamp(), query_start) > interval '60 seconds';`
3. **Safe Mitigation:**
    - If a specific user or microservice is flooding the database with dead connections, restart that specific service pod using Kubernetes:
      `kubectl rollout restart deployment/payment-service`
    - **DO NOT** restart the core database cluster unless explicitly instructed by the DBA lead, as it will cause a total global outage.