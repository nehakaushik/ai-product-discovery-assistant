from backend.generator import generate_answer


test_cases = [
    {
        "name": "Supported yes answer",
        "question": "Were users unclear about what they needed to do?",
        "evidence": [
            {
                "text": "Some of the onboarding instructions were confusing. I wasn't sure what I was supposed to do next."
            }
        ],
        "acceptable_phrases": ["yes"]
    },
    {
        "name": "Account connection problem",
        "question": "What problem did the customer have during setup?",
        "evidence": [
            {
                "text": "I had trouble connecting my account during setup and had to contact support."
            }
        ],
        "acceptable_phrases": [
            "connecting",
            "connection",
            "connectivity"
        ]
    },
    {
        "name": "Slow onboarding",
        "question": "What frustrated the customer about onboarding?",
        "evidence": [
            {
                "text": "The onboarding process took much longer than I expected. I almost gave up before finishing."
            }
        ],
        "acceptable_phrases": [
            "long",
            "longer",
            "slow",
            "time"
        ]
    },
    {
        "name": "Unsupported question",
        "question": "What pricing concerns did the customer have?",
        "evidence": [
            {
                "text": "The dashboard was easy to understand once I completed onboarding."
            }
        ],
        "acceptable_phrases": [
            "not enough information"
        ]
    }
]


passed_tests = 0


for test in test_cases:

    answer = generate_answer(
        test["question"],
        test["evidence"]
    )

    answer_lower = answer.lower() if answer else ""

    passed = any(
        phrase in answer_lower
        for phrase in test["acceptable_phrases"]
    )

    if passed:
        passed_tests += 1

    print("\nTest:", test["name"])
    print("Question:", test["question"])
    print("Generated answer:", answer)
    print("Acceptable phrases:", test["acceptable_phrases"])
    print("PASS" if passed else "FAIL")


print(
    f"\nGeneration eval result: {passed_tests}/{len(test_cases)} passed"
)