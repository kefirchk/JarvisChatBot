import json
import logging
from .ai_config import AI_TOOLS
from database import Database


class AIValueManager:
    __db = Database()

    """Initialize object of UserValuesManager."""
    def __init__(self, client):
        self._client = client
        logging.basicConfig(level=logging.INFO)

    async def get_values(self, run, thread):
        """Get life values of user from conversation."""
        tool_outputs = []
        values = []

        # Loop through each tool in the required action section
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "save_value":
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": tool.function.arguments
                })
            values = json.loads(tool.function.arguments).get('values', [])
            logging.info(f"Values: {values}")

        # Submit all tool outputs at once after collecting them in a list
        if tool_outputs:
            try:
                run = await self._client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                logging.info('Tool outputs submitted successfully.')
            except Exception as e:
                logging.error(f'Failed to submit tool outputs: {e}')
        else:
            logging.warning("No tool outputs to submit.")
        return run, values

    async def validate_values(self, values, user_id):
        """Validate life values of user from conversation."""
        valid_values = []
        for value in values:
            logging.info(f"Validate: {value}")
            is_valid = await self.is_valid_value(value)
            logging.info(f"Valid status of '{value}': {is_valid}, user ID: {user_id}")
            if is_valid:
                valid_values.append(value)
        logging.info(f"Valid values: {valid_values}")
        return valid_values

    async def is_valid_value(self, value):
        """Check if value is real life value of user from conversation."""

        # Step #1: Prompt with content that may result in function call.
        messages = [{"role": "user", "content": f"Is \"{value}\" a real key value? Answer only true or false."}]
        tools = [AI_TOOLS['IS_VALID_VALUE']]
        try:
            response = await self._client.chat.completions.create(
                model="gpt-4", messages=messages, tools=tools,
                tool_choice={"type": "function", "function": {"name": "is_valid_value"}}
            )
            tool_calls = response.choices[0].message.tool_calls

            # Step 2: determine if the response from the model includes a tool call.
            for tool_call in tool_calls:
                if tool_call.function:
                    is_value = json.loads(tool_call.function.arguments)['is_value']
                    return is_value
            return False
        except Exception as e:
            logging.error(f"Exception while checking if '{value}' is a real key value: {e}")
            return False

    async def save_values_in_db(self, user_id, values):
        """Save valid user's values in database."""
        logging.info(f"Saving in the database values: {values}, user ID: {user_id}")
        await self.__db.create_table()
        for value in values:
            await self.__db.insert_data(user_id, value)
