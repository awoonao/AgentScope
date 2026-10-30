SELECT *
FROM agent_runs;

SELECT
    status,
    COUNT(*) AS number_of_runs
FROM agent_runs
GROUP BY status;

SELECT
    ROUND(AVG(duration_seconds), 2) AS avg_response_time
FROM agent_runs
WHERE status = 'success';

SELECT
    ROUND(AVG(total_tokens), 2) AS avg_tokens,
    MIN(total_tokens) AS min_tokens,
    MAX(total_tokens) AS max_tokens
FROM agent_runs
WHERE status = 'success';

SELECT
    run_id,
    ROUND(duration_seconds, 2) AS duration,
    total_tokens
FROM agent_runs
WHERE status = 'success'
ORDER BY duration_seconds DESC;