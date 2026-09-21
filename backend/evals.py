from backend.retrieval import retrieve_evidence


test_cases = [
    {
        "question": "What made setup frustrating?",
        "should_find_evidence": True
    },
    {
        "question": "Did customers have trouble connecting their account?",
        "should_find_evidence": True
    },
    {
        "question": "Were users unclear about what they needed to do?",
        "should_find_evidence": True
    },
    {
        "question": "What pricing concerns did customers report?",
        "should_find_evidence": False
    }
]


for test in test_cases:

    results = retrieve_evidence(test["question"])

    found_evidence = len(results) > 0

    passed = found_evidence == test["should_find_evidence"]

    print("\nQuestion:", test["question"])
    print("Expected evidence:", test["should_find_evidence"])
    print("Found evidence:", found_evidence)
    print("PASS" if passed else "FAIL")