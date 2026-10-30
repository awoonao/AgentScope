from app import ask_agent


test_prompts = [
    "What is 25 * 4?",

    "Explain customer churn in simple terms.",

    "What are three reasons customers abandon online shopping carts?",

    "Write a Python function that checks whether a number is even.",

    "Explain the difference between mean and median.",

    "Give me three ways an online store could improve customer retention.",

    "What is overfitting in machine learning?",

    "Summarize the benefits of using SQL for data analysis.",

    "Write a short paragraph explaining why customer feedback is important.",

    "Compare supervised and unsupervised machine learning."
]


print("\n--- STARTING AUTOMATED AGENT TEST ---\n")

for number, prompt in enumerate(test_prompts, start=1):

    print(f"\n{'=' * 60}")
    print(f"TEST {number}/{len(test_prompts)}")
    print(f"Prompt: {prompt}")
    print("=" * 60)

    answer = ask_agent(prompt)

    print("\nResponse:")
    print(answer)


print("\n--- TEST COMPLETE ---")