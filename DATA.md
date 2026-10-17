# Input contract

The orchestration core accepts caller-provided worker, reviewer, and embedding callbacks. Reviewers must return Review(passed: bool, feedback: str). run_project executes stories, features, then tasks, stopping if an earlier review gate fails. No external-model client, client brief, credential, or generated provider transcript is included. Model availability and authorization belong to the caller's adapter.
