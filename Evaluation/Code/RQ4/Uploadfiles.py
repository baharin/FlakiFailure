from openai import OpenAI
client = OpenAI()


# a vector store that will index docs
vector_store = client.vector_stores.create(
    name="reference-docs"
)

# path to reference docs
file_paths = [
    "autopilot handbook3.pdf",
    "autopilot handbook.pdf",   
]

file_streams = [open(p, "rb") for p in file_paths]

client.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id,
    files=file_streams,
)

#this id will be used in the queryAPI.py 
print("Vector store ID:", vector_store.id)  
