from typing import List
from openai import OpenAI

client = OpenAI()

VECTOR_STORE_ID =  # vector store id from running Uploadfiles.py

BASE_PROMPT_TEMPLATE = """
Context: The statement and documents are related to {system_spec}.  

Task: You receive a statement X and have access to a collection of documents Y through the file_search tool. Your task is to: 
Retrieve between 2 and 5 of the most related sentences from Y that best match or support X. 

Guidelines:
1. Return fewer sentences (2–3) if only a few are highly relevant.
2. Return more sentences (4–5) if multiple sentences are strongly relevant.
3. Do not include loosely related or tangential sentences.
4. Preserve the original sentence wording exactly as it appears in Y.
5. Keep the sentences exactly as they appear in the original document.
6. Return only the selected sentences, each on a new line, with no explanation.

If needed, think more.

Example:

Example statement (X):
{example_statement}

Example retrieved sentences:
{example_retrieved_sentences}

End of example.

Now process the following statement.
"""


def find_supporting_sentences(
    statement,
    system_spec,
    example_statement,
    example_retrieved_sentences):
    """
    statement:                assertion in natural language
    system_spec:              short description of the system (for the Context line)
    example_statement:        one-shot example statement X
    example_retrieved_sentences: list of sentences used as the example retrieval result
    """
    
    base_prompt = BASE_PROMPT_TEMPLATE.format(
        system_spec=system_spec,
        example_statement=example_statement,
        example_retrieved_sentences="\n".join(example_retrieved_sentences),
    )

    prompt = base_prompt + f"\n\nStatement (X): {statement}\n"

    response = client.responses.create(
        model="gpt-5",
        reasoning={"effort": "medium"},
        input=prompt,
        tools=[{
            "type": "file_search",
            "vector_store_ids": VECTOR_STORE_ID,
            "max_num_results": 20,
        }],
    )

    text = response.output_text
    return text


# Example usage for AP-DHB
assertion = "When the thrust is insufficient during the flight, the aircraft does not reach its desired altitude within the required time frame."

system_spec = "an autopilot system of an aircraft"
example_statement = (
    "When the thrust is insufficient during the flight, the aircraft does not reach its desired altitude within the required time frame."
)
example_retrieved_sentences = [
    "Climb performance is directly dependent upon the ability to produce either excess thrust or excess power.",
    "Since weight, altitude and configuration changes affect excess thrust and power, they also affect climb performance.",
]

sentences = find_supporting_sentences(
    statement=assertion,
    system_spec=system_spec,
    example_statement=example_statement,
    example_retrieved_sentences=example_retrieved_sentences,
)
