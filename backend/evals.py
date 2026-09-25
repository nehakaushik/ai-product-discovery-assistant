from backend.retrieval import retrieve_evidence

test_cases = [
    {
        "question": "What made setup frustrating?",
        "should_find_evidence": True,
        "acceptable_sources": [
            "Customer Interview - March 14",
            "Customer Interview - March 18",
            "Customer Interview - March 21",
            "Customer Interview - April 5",
            "Customer Interview - April 9",
            "Customer Interview - April 12",
            "Customer Interview - April 23",
            "Customer Interview - April 27",
        ],
    },
    {
        "question": "Did customers have trouble connecting their account?",
        "should_find_evidence": True,
        "acceptable_sources": [
            "Customer Interview - March 21",
            "Customer Interview - April 9",
        ],
    },
    {
        "question": "Were users unclear about what they needed to do?",
        "should_find_evidence": True,
        "acceptable_sources": [
            "Customer Interview - March 18",
            "Customer Interview - April 2",
            "Customer Interview - April 12",
            "Customer Interview - April 23",
            "Customer Interview - April 27",
        ],
    },
    {
        "question": "What pricing concerns did customers report?",
        "should_find_evidence": False,
        "acceptable_sources": [],
    },
]

passed_tests = 0

for test in test_cases:
    results = retrieve_evidence(test["question"])

    retrieved_sources = [
        result["source"]
        for result in results
    ]

    if test["should_find_evidence"]:
        passed = any(
            source in test["acceptable_sources"]
            for source in retrieved_sources
        )
    else:
        passed = len(results) == 0

    if passed:
        passed_tests += 1

    print("\nQuestion:", test["question"])
    print("Retrieved sources:", retrieved_sources or "None")
    print("Acceptable sources:", test["acceptable_sources"] or "None")
    print("PASS" if passed else "FAIL")

print(
    f"\nRetrieval eval result: "
    f"{passed_tests}/{len(test_cases)} passed"
)