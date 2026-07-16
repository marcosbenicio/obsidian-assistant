import time
from dataclasses import dataclass, field
from datetime import datetime

from rag import RAGBase


@dataclass
class LLMCallRecord:
    model: str
    prompt: str
    instructions: str
    answer: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    response_time: float
    cost: float
    timestamp: datetime = field(
        default_factory=lambda: datetime.now().astimezone()
    )


def calculate_cost(model, usage):
    # Local models (Ollama) cost zero; API models get their rate here.
    cost = 0
    if "gpt-5.4-mini" in model:
        cost = (usage.prompt_tokens * 0.15 + usage.completion_tokens * 0.60) / 1_000_000
    return cost


class RAGWithMetrics(RAGBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_call: LLMCallRecord = None

    def llm(self, prompt):
        start_time = time.time()
        response = super().llm(prompt)
        response_time = time.time() - start_time
        self._log_response(prompt, response, response_time)
        return response

    def _log_response(self, prompt, response, response_time):
        usage = response.usage
        cost = calculate_cost(self.model, usage)

        self.last_call = LLMCallRecord(
            model=self.model,
            prompt=prompt,
            instructions=self.instructions,
            answer=response.choices[0].message.content,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            response_time=response_time,
            cost=cost,
        )
