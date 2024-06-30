import logging


class AIFileManager:
    def __init__(self, client):
        self.__client = client
        logging.basicConfig(level=logging.INFO)

    async def create_vector_store(self):
        # Create a vector store called "Anxiety"
        vector_store = await self.__client.beta.vector_stores.create(name="Anxiety")

        # Ready the files for upload to OpenAI
        file_paths = ["Anxiety.docx"]
        file_streams = [open(path, "rb") for path in file_paths]

        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = await self.__client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )

        # Print the status and the file counts of the batch to see the result of this operation.
        logging.info(f"File batch status: {file_batch.status}")
        logging.info(f"File counts: {file_batch.file_counts}")

        return vector_store
