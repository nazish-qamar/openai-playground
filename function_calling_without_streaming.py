from chatbot_config import client, assistant, thread

def get_generated_text_from_messages(messages):
    generated_texts = []
    for message in messages.data:
        if message.role == 'assistant':
            for content_block in message.content:
                if content_block.type == 'text':
                    generated_texts.append(content_block.text.value)
    return generated_texts

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
else:
    print(run.status)

tool_outputs = []

for tool in run.required_action.submit_tool_outputs.tool_calls:
    if tool.function.name == "get_current_temperature":
        tool_outputs.append({
            "tool_call_id": tool.id,
            "output": "57"
        })
    elif tool.function.name == "get_rain_probability":
        tool_outputs.append({
            "tool_call_id": tool.id,
            "output": "0.06"
        })

if tool_outputs:
    try:
        run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
        print("Tool outputs submitted successfully.")
    except Exception as e:
        print("Failed to submit tool outputs:", e)
else:
    print("No tool outputs to submit.")

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    generated_texts = get_generated_text_from_messages(messages)
    for text in generated_texts:
        print(text)
else:
    print(run.status)
