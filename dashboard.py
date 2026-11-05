
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

DB_NAME = "agent_data.db"

st.set_page_config(
    page_title="AI Agent Reliability Analytics",
    layout="wide"
)

st.title("AI Agent Reliability Analytics")
st.caption("Gemini API benchmark monitoring and performance analysis")


@st.cache_data(ttl=30)
def load_data():
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query("""
            SELECT
                run_id,
                benchmark_id,
                agent_version,
                model,
                prompt_id,
                task_type,
                status,
                duration_seconds,
                total_tokens,
                retry_count,
                error_type,
                error_message
            FROM agent_runs
            WHERE benchmark_id IS NOT NULL
            ORDER BY run_id
        """, conn)

    return df


def classify_error(row):
    if row["status"] == "success":
        return "Success"

    message = str(row["error_message"] or "")

    if "429 RESOURCE_EXHAUSTED" in message:
        return "Quota exhausted (429)"

    if "503 UNAVAILABLE" in message:
        return "Service unavailable (503)"

    if "504 DEADLINE_EXCEEDED" in message:
        return "Deadline exceeded (504)"

    return row["error_type"] or "Unknown failure"


df = load_data()

if df.empty:
    st.warning("No benchmark records found.")
    st.stop()

df["error_category"] = df.apply(classify_error, axis=1)

st.sidebar.header("Filters")

benchmarks = st.sidebar.multiselect(
    "Benchmark",
    options=sorted(df["benchmark_id"].unique()),
    default=sorted(df["benchmark_id"].unique())
)

models = st.sidebar.multiselect(
    "Model",
    options=sorted(df["model"].unique()),
    default=sorted(df["model"].unique())
)

categories = st.sidebar.multiselect(
    "Task category",
    options=sorted(df["task_type"].dropna().unique()),
    default=sorted(df["task_type"].dropna().unique())
)

filtered = df[
    df["benchmark_id"].isin(benchmarks)
    & df["model"].isin(models)
    & df["task_type"].isin(categories)
]

if filtered.empty:
    st.info("No records match the selected filters.")
    st.stop()

total = len(filtered)
successful = filtered[filtered["status"] == "success"]
failed = filtered[filtered["status"] == "failed"]

success_rate = len(successful) / total * 100

avg_latency = successful["duration_seconds"].mean()
total_tokens = successful["total_tokens"].sum()
median_latency = successful["duration_seconds"].median()
p95_latency = successful["duration_seconds"].quantile(0.95)

col1, col2, col3, col4 = st.columns(4)

st.subheader("Latency performance")

latency_col1, latency_col2 = st.columns(2)

latency_col1.metric(
    "Median latency (P50)",
    f"{median_latency:.2f}s" if pd.notna(median_latency) else "N/A"
)

latency_col2.metric(
    "P95 latency",
    f"{p95_latency:.2f}s" if pd.notna(p95_latency) else "N/A"
)

col1.metric("Total requests", total)
col2.metric("Success rate", f"{success_rate:.1f}%")
col3.metric("Avg success latency",
            f"{avg_latency:.2f}s" if pd.notna(avg_latency) else "N/A")
col4.metric("Successful-run tokens", f"{total_tokens:,.0f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Success vs failure by benchmark")

    status_counts = (
        filtered.groupby(["benchmark_id", "status"])
        .size()
        .reset_index(name="count")
    )

    fig = px.bar(
        status_counts,
        x="benchmark_id",
        y="count",
        color="status",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Failure causes")

    error_counts = (
        failed.groupby("error_category")
        .size()
        .reset_index(name="count")
    )

    if not error_counts.empty:
        fig = px.pie(
            error_counts,
            names="error_category",
            values="count",
            hole=0.45
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No failures in the selected data.")

st.subheader("Success rate by task category")

category_stats = (
    filtered.groupby("task_type")
    .agg(
        attempted=("run_id", "count"),
        successful=("status", lambda s: (s == "success").sum())
    )
    .reset_index()
)

category_stats["success_rate"] = (
    category_stats["successful"]
    / category_stats["attempted"] * 100
)

fig = px.bar(
    category_stats,
    x="task_type",
    y="success_rate",
    labels={
        "task_type": "Task category",
        "success_rate": "Success rate (%)"
    },
    range_y=[0, 100]
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Successful request latency")

if not successful.empty:
    fig = px.histogram(
        successful,
        x="duration_seconds",
        nbins=15,
        labels={"duration_seconds": "Latency (seconds)"}
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No successful requests to analyze.")

st.subheader("Benchmark records")

st.dataframe(
    filtered.drop(columns=["error_message"]),
    use_container_width=True,
    hide_index=True
)

st.subheader("Export benchmark data")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered results as CSV",
    data=csv,
    file_name="ai_agent_benchmark_results.csv",
    mime="text/csv"
)

st.caption(
    "Success rate measures completed API requests, "
    "not answer correctness. Benchmark conditions and "
    "sample sizes differ."
)
