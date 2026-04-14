import argparse
import os
from dotenv import load_dotenv
from google import genai


def main():
    parser = argparse.ArgumentParser(description="AI agent powered by Gemini")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the model")
    args = parser.parse_args()

    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not found. Please set it in your .env file.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=args.user_prompt,
    )
    if response.usage_metadata is None:
        raise RuntimeError("No usage metadata in response, the API request may have failed.")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
