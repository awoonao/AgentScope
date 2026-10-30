import sqlite3

conn = sqlite3.connect("agent_data.db")
cursor = conn.cursor()

# 1. Total runs
cursor.execute("""
    SELECT COUNT(*)
    FROM agent_runs
""")

total_runs = cursor.fetchone()[0]


# 2. Success and failure counts
cursor.execute("""
    SELECT
        status,
        COUNT(*)
    FROM agent_runs
    GROUP BY status
""")

status_counts = cursor.fetchall()


# 3. Average successful response time
cursor.execute("""
    SELECT AVG(duration_seconds)
    FROM agent_runs
    WHERE status = 'success'
""")

avg_latency = cursor.fetchone()[0]


# 4. Fastest and slowest successful response
cursor.execute("""
    SELECT
        MIN(duration_seconds),
        MAX(duration_seconds)
    FROM agent_runs
    WHERE status = 'success'
""")

min_latency, max_latency = cursor.fetchone()


# 5. Average token usage
cursor.execute("""
    SELECT AVG(total_tokens)
    FROM agent_runs
    WHERE status = 'success'
""")

avg_tokens = cursor.fetchone()[0]


print("\n--- AGENT V1 ANALYSIS ---\n")

print(f"Total runs: {total_runs}")

print("\nStatus:")
for status, count in status_counts:
    percentage = count / total_runs * 100
    print(f"{status}: {count} ({percentage:.1f}%)")

print(f"\nAverage successful latency: {avg_latency:.2f} seconds")
print(f"Fastest successful request: {min_latency:.2f} seconds")
print(f"Slowest successful request: {max_latency:.2f} seconds")
print(f"Average tokens per successful request: {avg_tokens:.2f}")

conn.close()