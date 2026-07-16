import os

from openai import OpenAI


INSTRUCTIONS = '''
You are the assistant for my personal Obsidian vault.
Answer questions using only the provided context, which contains
excerpts from my notes. Mention the source notes you used by their path.
If the answer is not in the context, say you could not find it in the vault.
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()


def create_llm_client():
    # Provider-agnostic: with LLM_BASE_URL set, any OpenAI-compatible server
    # works (Ollama: http://ollama:11434/v1). Without it, the real OpenAI API.
    base_url = os.getenv("LLM_BASE_URL")
    if base_url:
        return OpenAI(base_url=base_url, api_key=os.getenv("OPENAI_API_KEY", "ollama"))
    return OpenAI()


class RAGBase:

    def __init__(
        self,
        search_fn,
        llm_client=None,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        model=None,
    ):
        # search_fn is injected: any callable (query, num_results) -> list of
        # chunk dicts with "path" and "content". Keeps the RAG logic agnostic
        # of the retrieval engine, like llm_client keeps it agnostic of the
        # LLM provider.
        self.search_fn = search_fn
        self.llm_client = llm_client or create_llm_client()
        self.instructions = instructions
        self.prompt_template = prompt_template
        self.model = model or os.getenv("LLM_MODEL", "gpt-5.4-mini")

    def search(self, query, num_results=5):
        return self.search_fn(query, num_results=num_results)

    def build_context(self, search_results):
        lines = []

        for doc in search_results:
            lines.append(doc["path"])
            lines.append(doc["content"])
            lines.append("")

        return "\n".join(lines).strip()

    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        return self.prompt_template.format(
            question=query, context=context
        )

    def llm(self, prompt):
        # chat.completions is the API every OpenAI-compatible provider speaks
        # (OpenAI, Ollama, Groq...); the Responses API used in the course is
        # OpenAI-only, so it stays out of a multi-provider tool.
        response = self.llm_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt},
            ],
        )
        return response

    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        response = self.llm(prompt)
        return response.choices[0].message.content
