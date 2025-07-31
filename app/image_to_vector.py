import base64
import io
import os
from uuid import uuid4

from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv

from vector_db import create_chroma_persistent_client, create_collection

def resize_image(image_path: str, scale_factor: float) -> Image:


    with Image.open(f"{image_path}") as img:

        original_width, original_height = img.size

        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        new_size = (new_width, new_height)
        resized_img = img.resize(new_size)

    return resized_img


def encode_image(image: Image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def get_image_description(client: OpenAI, b64_image: Image) -> str:

    instructions = """
        You are involved in a Fashion Company as describer of images depicting clothes of any type.
        You goal is to provide a clear description of the clothe in the image.
        You must ignore the image background but just focus on the clothe itself. 
        
        You have to focus on the following particulars and add them in your description:
        - color of the clothe
        - any print of image on the clothe
        - texture of the clothe (if you can identify it)
        - if the clothe is for Male, Female or Unisex
        
        Don't start the description with "the image shows" or "the clothes is" or similar but just
        provide the description of the clothe. 
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0.3,
        max_output_tokens=300,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": instructions},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{b64_image}",
                    },
                ],
            }
        ],
    )

    return response.output_text

def get_image_embedding(client, text):

    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )

    return response.data[0].embedding



def main():
    load_dotenv()
    images_path = "app/images/"

    client = OpenAI()
    emb_client = OpenAI()

    chroma_client = create_chroma_persistent_client(path="app/chroma_db")
    chroma_collection = create_collection(client=chroma_client, collection_name="app_collection")


    for file in os.listdir(images_path):
        print(file)

        img = resize_image(image_path=f"{images_path}/{file}", scale_factor=0.90)
        print(img.size)

        b64_encode = encode_image(image=img)

        image_description = get_image_description(client=client, b64_image=b64_encode)

        image_embedding = get_image_embedding(client=emb_client, text=image_description)

        chroma_collection.add(
            ids=[str(uuid4())],
            embeddings=[image_embedding],
            metadatas=[{"image_name": file, "image_description": image_description}]
        )


    print(chroma_collection.count())



if __name__ == "__main__":
    main()
