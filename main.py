import os
import sys

from dotenv import load_dotenv
from config import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import schema_call_function
from functions.call_function import call_function

client = genai.Client(api_key=api_key)


def main():
    
    user_prompt = sys.argv[1]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
            schema_call_function,
        ]
    )

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    
    loop_count = 0

    while loop_count < LOOP_LIMIT:
    
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=SYSTEM_PROMPT
                ),
            )

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if "--verbose" in sys.argv:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.function_calls:
                for function_call_part in response.function_calls:
                    print(f"- Calling function: {function_call_part.name}({function_call_part.args})")
                    result = call_function(function_call_part)

                    messages.append(result)

                    if not result.parts[0].function_response.response:
                        raise Exception("""Error: fatal eception, ".parts[0].function_response.response" not present""")
                    if "--verbose" in sys.argv:
                        print(f"-> {result.parts[0].function_response.response}")
            else:
                if response.text:
                    print("*************************************************")
                    print("Final response:")
                    print(response.text)
                    print("*************************************************")
                    break

            loop_count += 1

        except Exception as error:
            print("******************************************************")
            print(f"""Error: unable complete "generate_content". {error}""")

if __name__ == "__main__":
    main()
