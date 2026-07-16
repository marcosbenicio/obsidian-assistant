"""Online LLM-as-a-judge: evaluates the relevance of each answer with
structured output and stores the verdict in the feedback table with
source='judge'. Adapted from lesson 09 and the module 4 judge.

Planned (day 8): Verdict model (RELEVANT / PARTLY_RELEVANT / NON_RELEVANT
plus explanation), llm_structured_retry, save via db.save_feedback.
"""


def judge_answer(question, answer):
    raise NotImplementedError("day 8")
