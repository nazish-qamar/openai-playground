from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    instructions="You are a funny weather bot. You reply for the answer with additional advice for activities which a person can do. Use the provided functions to answer questions.",
    model="gpt-4o",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_current_temperature",
                "description": "Get the current temperature for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g., San Francisco, CA"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["Celsius", "Fahrenheit"],
                            "description": "The temperature unit to use. Infer this from the user's location."
                        }
                    },
                    "required": ["location", "unit"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_rain_probability",
                "description": "Get the probability of rain for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g., San Francisco, CA"
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]
)

thread = client.beta.threads.create()

# Create the initial message in the thread
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What's the weather in Paris today and the likelihood it'll rain?",
)
