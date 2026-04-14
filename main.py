import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function


def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata in response, the API request may have failed.")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    return response


def main():
    parser = argparse.ArgumentParser(description="AI agent powered by Gemini")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not found. Please set it in your .env file.")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        response = generate_content(client, messages, verbose=args.verbose)

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            function_responses = []
            for fc in response.function_calls:
                function_call_result = call_function(fc, verbose=args.verbose)
                if not function_call_result.parts:
                    raise RuntimeError(f"Function call '{fc.name}' returned no parts")
                function_response = function_call_result.parts[0].function_response
                if function_response is None:
                    raise RuntimeError(f"Function call '{fc.name}' returned no function_response")
                if function_response.response is None:
                    raise RuntimeError(f"Function call '{fc.name}' returned no response data")
                if args.verbose:
                    print(f"-> {function_response.response}")
                function_responses.append(function_call_result.parts[0])
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print("Final response:")
            print(response.text)
            return

    print("Error: maximum iterations reached without a final response.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
