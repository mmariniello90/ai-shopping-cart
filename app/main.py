import json
import logging

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import print as rprint
from rich.logging import RichHandler

from dotenv import load_dotenv

from prompts import system_prompt
from tools import tools, get_similar_items, manage_shopping_cart
from vector_db import create_chroma_persistent_client, create_collection




def get_image_embedding(client, text):

    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    return response.data[0].embedding



def run():

    load_dotenv()
    console = Console()
    client = OpenAI()

    shopping_cart = []

    conversation_history = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # --- Main Chat Loop ---
    while True:

        #user_input = console.input("\nTu: ")
        user_input = console.input("[deep_sky_blue1]You: [/deep_sky_blue1]")

        if user_input.lower() == 'quit':
            #console.print(Markdown(f"[bold red]AI: Bye Bye![/bold red]"))
            console.print(Panel(Markdown("Bye Bye!"), title="[deep_sky_blue1]AI[/deep_sky_blue1]",
                                title_align="left", border_style="#12a0d7"))
            break

        # Add user's message to the conversation history
        conversation_history.append({"role": "user", "content": user_input})



        response = client.responses.create(
            model="gpt-4o-mini",
            input=conversation_history,
            temperature=1.0,
            tools=tools,
            tool_choice="auto"
        )

        # Extract the assistant's message from the response
        assistant_message = response.output_text
        #assistant_message = response.choices[0].message

        #print("----" * 50)
        #print(response.to_json())
        #print(response.output[0].to_dict())
        #print("----" * 50)

        if "call_id" in response.output[0].to_dict():

            print("tool called")
            tool_call = response.output[0]
            print(f"TOOL CALL: {tool_call.name}")
            args = json.loads(tool_call.arguments)

            tool_result = None
            if tool_call.name == "get_similar_items":
                tool_result = get_similar_items(args["query_text"])

                conversation_history.append(tool_call)  # append model's function call message
                conversation_history.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(tool_result)
                })

                #search_response = f"I've found something: {[(item) for item in tool_result]}"

                search_response = client.responses.create(
                    model="gpt-4o-mini",
                    input=str(tool_result),
                    instructions="You will receive a JSON as input. Show and describe each item in it.",
                    temperature=1.0,
                    tools=tools
                )

                console.print(Panel(Markdown(search_response.output_text), title="[deep_sky_blue1]AI[/deep_sky_blue1]",
                                    title_align="left", border_style="#12a0d7"))

                conversation_history.append({"role": "assistant", "content": search_response.output_text})


            elif tool_call.name == "manage_shopping_cart":
                tool_result = manage_shopping_cart(shopping_cart, args["action"], args["item"])

                conversation_history.append(tool_call)  # append model's function call message
                conversation_history.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(tool_result)
                })

                response_2 = client.responses.create(
                    model="gpt-4o-mini",
                    input=conversation_history,
                    temperature=1.0,
                    tools=tools
                )


                console.print(Panel(Markdown(response_2.output_text), title="[deep_sky_blue1]AI[/deep_sky_blue1]",
                                title_align="left", border_style="#12a0d7"))

                conversation_history.append({"role": "assistant", "content": response_2.output_text})


        else:
            console.print(Panel(Markdown(assistant_message), title="[deep_sky_blue1]AI[/deep_sky_blue1]",
                            title_align="left", border_style="#12a0d7"))

            # Add assistant's message to the history for context in the next turn
            conversation_history.append({"role": "assistant", "content": assistant_message})



if __name__ == "__main__":
    run()