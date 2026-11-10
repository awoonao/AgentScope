# AI Agent Reliability & Quality Analytics

A Python-based AI agent evaluation and analytics system designed to measure the reliability, performance, and response quality of large language models (LLMs).

The project integrates Google's Gemini API, SQLite-based experiment tracking, automated benchmark testing, SQL execution-based evaluation, rubric-based response assessment, and an interactive Streamlit dashboard.

## Project Objectives

- Build a working AI agent using an external LLM API.
- Track API requests, latency, token usage, errors, and retry attempts.
- Evaluate model reliability across different benchmark categories.
- Assess response quality using automated and rubric-based methods.
- Visualize performance metrics and evaluation results.
- Develop a reproducible workflow for analyzing AI system performance.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application and evaluation logic |
| Google Gemini API | LLM inference |
| SQLite | Experiment and evaluation storage |
| Pandas | Data analysis and aggregation |
| Streamlit | Interactive analytics dashboard |
| Plotly | Data visualization |
| Git and GitHub | Version control and portfolio hosting |

## System Workflow

1. A user submits a question or a benchmark prompt.
2. The application sends the request to the Gemini API.
3. The system records request status, latency, token usage, and errors.
4. Request and retry data are stored in SQLite.
5. Evaluation scripts assess selected successful responses.
6. Streamlit displays reliability, performance, and quality metrics.

## Benchmark Design

The benchmark contains 60 prompts across six task categories:

- Factual questions
- Explanations
- Coding
- Writing
- Reasoning
- Recommendations

Each category contains 10 prompts.

The benchmark runner supports randomized execution, skipping previously attempted prompts, and stopping under specified API error conditions.

## Reliability and Performance Metrics

The system tracks:

- Total requests and successful requests
- Request success and failure rates
- Average and median response latency
- P95 response latency
- Input, output, and total token usage
- Retry counts
- API error types
- Performance by model, benchmark, and task category

### Preliminary Benchmark Results

| Benchmark | Attempts | Successful | Success Rate |
|---|---:|---:|---:|
| V1 | 60 | 0 | 0% |
| V2 | 5 | 0 | 0% |
| V3 | 5 | 3 | 60% |

The V3 benchmark recorded an average successful response latency of approximately 1.81 seconds.

**Interpretation:** These results are preliminary and heavily influenced by API availability, quota restrictions, and small sample sizes. They should not be interpreted as a controlled comparison of model quality.

## Answer Quality Evaluation

The project includes multiple evaluation approaches.

### Heuristic Evaluation

Rule-based checks evaluate selected responses and classify them as:

- Correct
- Incorrect
- Needs review

These checks are suitable only for limited answer formats and are not a general-purpose factual correctness evaluator.

### SQL Execution Evaluation

Generated SQL queries are executed against controlled SQLite test datasets.

The evaluator compares actual query results against expected outcomes and includes tests involving empty datasets and NULL values.

This provides stronger validation for selected SQL tasks than comparing generated SQL strings alone.

The current evaluator is intended for controlled testing, not as a fully secure sandbox for arbitrary untrusted SQL.

### Rubric-Based Evaluation

Selected writing and recommendation responses are assessed using criteria such as:

- Relevance
- Brevity
- Tone
- Completeness
- Actionability

Each criterion is scored from 0 to 2.

Rubric scores are stored with evaluator metadata and rubric versions for traceability.

Current rubric assessments are preliminary assistant-reviewed judgments, not independently validated human evaluations.

## Interactive Dashboard

The Streamlit dashboard provides:

- Benchmark and model filters
- Reliability KPIs
- Latency analysis
- Error distribution
- Task-category comparisons
- Answer-quality evaluation summaries
- Rubric-based evaluation analytics
- Detailed request records and CSV export

## Project Limitations

- The available benchmark results are limited by API quotas and availability.
- Successful response counts are currently too small for robust model comparisons.
- Heuristic evaluation does not generalize reliably to complex open-ended answers.
- Rubric assessments are subjective and require additional validation.
- The SQL evaluator requires stronger isolation before processing arbitrary untrusted queries.
- Benchmark results may vary with API conditions and model availability.

## Future Improvements

- Complete more benchmark runs under comparable conditions.
- Expand automated evaluation coverage.
- Introduce independently reviewed evaluation datasets.
- Improve statistical reporting and confidence intervals.
- Strengthen SQL evaluation isolation.
- Add reproducible sample datasets and automated tests.
- Improve deployment and documentation.

## Project Status

**Active development — portfolio project**

This project demonstrates Python application development, API integration, database design, automated testing, experimental evaluation, and interactive data analytics.