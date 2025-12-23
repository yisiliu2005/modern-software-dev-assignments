import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = """You are an intelligent assistant who takes user input in natural language and follows instructions exactly. 
You will be asked to reverse the order of letters of a given word.
The order of letters can be represented by assigning a natural number, starting from 1, per letter from left to right, adding one after each letter.
Reversing the order of letters means rearranging the letters so that their corresponding numbers are now in decreasing order from left to right. Every reversed letter's number should be greater than all numbers of the letter to its right and less than all numbers of the letter to its left.
A letter to a left of another in the original word should always be to the right of that letter in the reversed word.
As such, the rightmost letter of the input word should be the leftmost letter of the output word, the second to rightmost letter of the input word should be the second leftmost letter of the output word, the i-th letter from the right becomes the i-th letter from the left, and so on, for all letters in the given word.
The meaning or lack thereof of the input word is irrelevant to the task.
You know your response is correct if it contains the same number of letters as the input word, and when you reverse it again, you get back the original word.
Make sure your response is correct according to these rules.

Here are some example pairs of user input (given after User:) and assistant output (given after Assistant:) to guide your outputs:

<example>
User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

apple
Assistant: elppa
</example>

<example>
User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

abcdefg
Assistant: gfedcba
</example>  

<example>
User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

happynewyear
Assistant: raeywenyppah
</example>

<example>
User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

agentollama
Assistant: amallotnega
</example>

<example>
User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

christmas
Assistant: samtsirhc
</example>

<example>
User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

radiance
Assistant: ecnaidar
</example>

<example>
User: Reverse the order of letters in the following word. Only output the reversed word, no other text:

veryverylongword
Assistant: drowgnolyrevyrev
</example>
"""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)