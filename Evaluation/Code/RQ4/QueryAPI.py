from typing import List
from openai import OpenAI

client = OpenAI()

VECTOR_STORE_ID =  # vector store id from running Uploadfiles.py

BASE_PROMPT_TEMPLATE = """
Context: The assertion and documents are related to {system_spec}.  

Task: Given a natural-language assertion X and a collection of documents Y through the file_search tool, your task is to identify and return sentencens that address the same condition, behaviour or outcome as the assertion.

Instructions:
1. Retrieve between 2 and 5 sentences from the documentation that best support the assertion. Return 2–3 sentences if only a few are highly related. Return 4–5 sentences if several sentences are strongly related.
2. Exclude sentences that are loosely related or tangential.
3. Preserve the original sentence wording exactly as it appears in the documents Y.
4. Output only the selected sentences, each on a new line, with no explanations or metadata.

If needed, think more.

Example:

Example assertion (X):
{example_assertion}

Example retrieved sentences:
{example_retrieved_sentences}

End of example.

Now process the following assertion.
"""


def find_supporting_sentences(
    assertion,
    system_spec,
    example_assertion,
    example_retrieved_sentences):
    """
    assertion:                assertion in natural language
    system_spec:              short description of the system (for the Context line)
    example_assertion:        one-shot example assertion X
    example_retrieved_sentences: list of sentences used as the example retrieval result
    """
    
    base_prompt = BASE_PROMPT_TEMPLATE.format(
        system_spec=system_spec,
        example_assertion=example_assertion,
        example_retrieved_sentences="\n".join(example_retrieved_sentences),
    )

    prompt = base_prompt + f"\n\nAssertion (X): {assertion}\n"

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
example_assertion = (
    "When the thrust is insufficient during the flight, the aircraft does not reach its desired altitude within the required time frame."
)
example_retrieved_sentences = [
    "Climb performance is directly dependent upon the ability to produce either excess thrust or excess power.",
    "Since weight, altitude and configuration changes affect excess thrust and power, they also affect climb performance.",
]

sentences = find_supporting_sentences(
    assertion=assertion,
    system_spec=system_spec,
    example_assertion=example_assertion,
    example_retrieved_sentences=example_retrieved_sentences,
)
