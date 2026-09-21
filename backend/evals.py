from backend.retrieval import retrieve_evidence


test_cases = [
    {
        "question": "What made setup frustrating?",
        "should_find_evidence": True,
        "expected_source": "Customer Interview - March 18"
    },
    {
        "question": "Did customers have trouble connecting their account?",
        "should_find_evidence": True,
        "expected_source": "Customer Interview - March 21"
    },
    {
        "question": "Were users unclear about what they needed to do?",
        "should_find_evidence": True,
        "expected_source": "Customer Interview - March 18"
    },
    {
        "question": "What pricing concerns did customers report?",
        "should_find_evidence": False,
        "expected_source": None
    }
]


for test in test_cases:

    results = retrieve_evidence(test["question"])

    found_evidence = len(results) > 0

    if test["should_find_evidence"]:
        retrieved_sources = [
            result["source"]
            for result in results
        ]

        passed = (
            found_evidence
            and test["expected_source"] in retrieved_sources
        )

    else:
        passed = not found_evidence

    print("\nQuestion:", test["question"])
    print("Expected source:", test["expected_source"])

    if results:
        print(
            "Retrieved sources:",
            [result["source"] for result in results]
        )
    else:
        print("Retrieved sources: None")

    print("PASS" if passed else "FAIL")