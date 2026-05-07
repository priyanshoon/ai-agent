import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompt import system_prompt


def main():
    parser = argparse.ArgumentParser(description="ChatBot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(20):
        response = generate_content(client, messages, args.verbose)
        response_can = response.candidates
        if response_can:
            for candidate in response_can:
                if candidate.content:
                    messages.append(candidate.content)
        if not response.function_calls:
            print("Final response:")
            print(response.text)
            return

        function_responses = []
        for function_call in response.function_calls:
            result = call_function(function_call, args.verbose)
            if result.parts is not None:
                function_responses.append(result.parts[0])

        messages.append(types.Content(role="user", parts=function_responses))

    print("Max iterations reached without a final response")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt, temperature=0
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.function_calls is not None:
        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if not function_call_result.parts:
                raise Exception("Something went wrong janny")
            if not function_call_result.parts[0].function_response:
                raise Exception("Something went wrong janny")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Something went wrong janny")

            function_responses.append(function_call_result.parts[0])

            # if verbose:
            #     print(f"-> {function_call_result.parts[0].function_response.response}")

    return response


if __name__ == "__main__":
    main()
