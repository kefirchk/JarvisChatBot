AI_NAME = 'Jarvis'
GPT_MODEL = 'gpt-4-turbo-preview'
COMMON_ASSISTANT_INSTRUCTIONS = """You are a chat assistant. You can answer questions and participate in the 
                                conversation. Analyze the user's communications and try to determine the user's
                                core values based on your communication. If any values are found, call the 
                                save_value function. After calling the save_value function, continue the normal 
                                dialogue with the user."""

FILE_SEARCH_INSTRUCTIONS = """If a user asks a question about anxiety, then use the file_search function 
                            to find the answer After answering, add in Russian: the information was taken from 
                            'here is the file name where you got the information from'."""

AI_TOOLS = {
    'IS_VALID_VALUE':
        {
            "type": "function",
            "function": {
                "name": "is_valid_value",
                "description": "Check if the value is a valid key value",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_value": {
                            "type": "boolean",
                            "description":
                                """This value represents the answer to the user's question as to whether 
                                the provided value is a valid life value or contains nonsense.
                                Contains only the logical type "true" or "false".
                                "True" means that the values are defined correctly and do not contain nonsense.
                                "False" - the value is defined incorrectly or the string is empty.""",
                        }
                    },
                    "required": ["is_value"],
                },
            }
        },
    'SAVE_VALUE':
        {
            "type": "function",
            "function": {
                "name": "save_value",
                "description": "Check and save the identified key values",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "values": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description":
                                """The list of key values identified in the user's message.
                                All values must be in Russian and start with capital letter."""
                        }
                    },
                    "required": ["values"]
                }
            }
        }
}
