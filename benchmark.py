BENCHMARK_ID = "benchmark_v3"

BENCHMARK_PROMPTS = [

    # =========================
    # FACTUAL
    # =========================

    {
        "prompt_id": "F01",
        "task_type": "factual",
        "prompt": "What is 25 multiplied by 4?"
    },
    {
        "prompt_id": "F02",
        "task_type": "factual",
        "prompt": "What is the capital of Japan?"
    },
    {
        "prompt_id": "F03",
        "task_type": "factual",
        "prompt": "How many days are in a leap year?"
    },
    {
        "prompt_id": "F04",
        "task_type": "factual",
        "prompt": "What does CPU stand for?"
    },
    {
        "prompt_id": "F05",
        "task_type": "factual",
        "prompt": "What is the largest planet in the Solar System?"
    },
    {
        "prompt_id": "F06",
        "task_type": "factual",
        "prompt": "How many bytes are in a kilobyte using the binary convention?"
    },
    {
        "prompt_id": "F07",
        "task_type": "factual",
        "prompt": "What is the chemical symbol for gold?"
    },
    {
        "prompt_id": "F08",
        "task_type": "factual",
        "prompt": "What is 144 divided by 12?"
    },
    {
        "prompt_id": "F09",
        "task_type": "factual",
        "prompt": "What does SQL stand for?"
    },
    {
        "prompt_id": "F10",
        "task_type": "factual",
        "prompt": "How many minutes are in two hours?"
    },

    # =========================
    # EXPLANATION
    # =========================

    {
        "prompt_id": "E01",
        "task_type": "explanation",
        "prompt": "Explain customer churn in simple terms."
    },
    {
        "prompt_id": "E02",
        "task_type": "explanation",
        "prompt": "Explain the difference between mean and median."
    },
    {
        "prompt_id": "E03",
        "task_type": "explanation",
        "prompt": "Explain overfitting in machine learning."
    },
    {
        "prompt_id": "E04",
        "task_type": "explanation",
        "prompt": "Explain what a database index does."
    },
    {
        "prompt_id": "E05",
        "task_type": "explanation",
        "prompt": "Explain correlation in simple terms."
    },
    {
        "prompt_id": "E06",
        "task_type": "explanation",
        "prompt": "Explain what an API is to a beginner."
    },
    {
        "prompt_id": "E07",
        "task_type": "explanation",
        "prompt": "Explain the difference between classification and regression."
    },
    {
        "prompt_id": "E08",
        "task_type": "explanation",
        "prompt": "Explain why data cleaning is important."
    },
    {
        "prompt_id": "E09",
        "task_type": "explanation",
        "prompt": "Explain what customer retention means."
    },
    {
        "prompt_id": "E10",
        "task_type": "explanation",
        "prompt": "Explain the purpose of data visualization."
    },

    # =========================
    # CODING
    # =========================

    {
        "prompt_id": "C01",
        "task_type": "coding",
        "prompt": "Write a Python function that checks whether a number is even."
    },
    {
        "prompt_id": "C02",
        "task_type": "coding",
        "prompt": "Write a Python function that returns the largest number in a list."
    },
    {
        "prompt_id": "C03",
        "task_type": "coding",
        "prompt": "Write a SQL query that selects all customers from a customers table."
    },
    {
        "prompt_id": "C04",
        "task_type": "coding",
        "prompt": "Write a Python loop that prints the numbers 1 through 10."
    },
    {
        "prompt_id": "C05",
        "task_type": "coding",
        "prompt": "Write a SQL query that counts the number of rows in an orders table."
    },
    {
        "prompt_id": "C06",
        "task_type": "coding",
        "prompt": "Write a Python function that calculates the average of a list of numbers."
    },
    {
        "prompt_id": "C07",
        "task_type": "coding",
        "prompt": "Write a SQL query that groups sales by product category and calculates total sales."
    },
    {
        "prompt_id": "C08",
        "task_type": "coding",
        "prompt": "Write Python code that removes duplicate values from a list."
    },
    {
        "prompt_id": "C09",
        "task_type": "coding",
        "prompt": "Write a SQL query that returns customers whose total_spend is greater than 1000."
    },
    {
        "prompt_id": "C10",
        "task_type": "coding",
        "prompt": "Write a Python function that converts Celsius to Fahrenheit."
    },

    # =========================
    # WRITING
    # =========================

    {
        "prompt_id": "W01",
        "task_type": "writing",
        "prompt": "Write a short product description for a reusable water bottle."
    },
    {
        "prompt_id": "W02",
        "task_type": "writing",
        "prompt": "Write a short welcome message for a new customer."
    },
    {
        "prompt_id": "W03",
        "task_type": "writing",
        "prompt": "Write a professional email thanking a customer for their feedback."
    },
    {
        "prompt_id": "W04",
        "task_type": "writing",
        "prompt": "Write a short social media caption promoting a coffee shop."
    },
    {
        "prompt_id": "W05",
        "task_type": "writing",
        "prompt": "Write a short description for an online clothing store."
    },
    {
        "prompt_id": "W06",
        "task_type": "writing",
        "prompt": "Write a polite message informing a customer that their order is delayed."
    },
    {
        "prompt_id": "W07",
        "task_type": "writing",
        "prompt": "Write a short introduction for a report about online shopping behaviour."
    },
    {
        "prompt_id": "W08",
        "task_type": "writing",
        "prompt": "Write a short advertisement for a fitness app."
    },
    {
        "prompt_id": "W09",
        "task_type": "writing",
        "prompt": "Write a brief thank-you message for a repeat customer."
    },
    {
        "prompt_id": "W10",
        "task_type": "writing",
        "prompt": "Write a short paragraph describing the benefits of remote work."
    },

    # =========================
    # REASONING
    # =========================

    {
        "prompt_id": "R01",
        "task_type": "reasoning",
        "prompt": "A company has rising sales but falling profit. Give two possible explanations."
    },
    {
        "prompt_id": "R02",
        "task_type": "reasoning",
        "prompt": "Website traffic increased but purchases stayed the same. What might this indicate?"
    },
    {
        "prompt_id": "R03",
        "task_type": "reasoning",
        "prompt": "A store lowered prices but revenue decreased. Give two possible reasons."
    },
    {
        "prompt_id": "R04",
        "task_type": "reasoning",
        "prompt": "Customer satisfaction increased but retention decreased. Give possible explanations."
    },
    {
        "prompt_id": "R05",
        "task_type": "reasoning",
        "prompt": "An advertising campaign generated many clicks but few sales. What might be happening?"
    },
    {
        "prompt_id": "R06",
        "task_type": "reasoning",
        "prompt": "A product has high ratings but low sales. Give three possible explanations."
    },
    {
        "prompt_id": "R07",
        "task_type": "reasoning",
        "prompt": "An online store has many cart additions but few completed purchases. What could explain this?"
    },
    {
        "prompt_id": "R08",
        "task_type": "reasoning",
        "prompt": "A business gained more customers but average revenue per customer fell. What might explain this?"
    },
    {
        "prompt_id": "R09",
        "task_type": "reasoning",
        "prompt": "A website redesign increased session duration but reduced conversions. Give possible explanations."
    },
    {
        "prompt_id": "R10",
        "task_type": "reasoning",
        "prompt": "Support tickets decreased while customer complaints on social media increased. What might this suggest?"
    },

    # =========================
    # RECOMMENDATION
    # =========================

    {
        "prompt_id": "REC01",
        "task_type": "recommendation",
        "prompt": "Suggest three ways an online retailer could improve customer retention."
    },
    {
        "prompt_id": "REC02",
        "task_type": "recommendation",
        "prompt": "Recommend three ways a small business could collect customer feedback."
    },
    {
        "prompt_id": "REC03",
        "task_type": "recommendation",
        "prompt": "Suggest three ways to reduce online shopping cart abandonment."
    },
    {
        "prompt_id": "REC04",
        "task_type": "recommendation",
        "prompt": "Recommend three metrics for measuring customer satisfaction."
    },
    {
        "prompt_id": "REC05",
        "task_type": "recommendation",
        "prompt": "Suggest three ways a website could improve its checkout experience."
    },
    {
        "prompt_id": "REC06",
        "task_type": "recommendation",
        "prompt": "Recommend three ways an ecommerce company could increase repeat purchases."
    },
    {
        "prompt_id": "REC07",
        "task_type": "recommendation",
        "prompt": "Suggest three ways a company could improve email campaign performance."
    },
    {
        "prompt_id": "REC08",
        "task_type": "recommendation",
        "prompt": "Recommend three useful KPIs for an online store."
    },
    {
        "prompt_id": "REC09",
        "task_type": "recommendation",
        "prompt": "Suggest three ways a mobile app could improve user retention."
    },
    {
        "prompt_id": "REC10",
        "task_type": "recommendation",
        "prompt": "Recommend three ways a company could improve customer support."
    }
]