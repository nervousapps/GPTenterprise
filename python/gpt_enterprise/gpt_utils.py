"""
GPT utils
"""
import os
import openai
import requests
from typing import Tuple, List

# Prompts base path
PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "employees_prompts")

# Output directory base path
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "generated")

# Initialize openai api_key
with open(os.path.join(os.path.dirname(__file__), "openai_key.txt"), 'r') as file:
    openai.api_key = file.read()
    

def generate_text(system_prompt: str, user_prompt: str, **kwargs) -> str:
    """_summary_

    Args:
        system_content (str): Initialize the system with the given system prompt
        system_prompt (str): Assistant will try to give the best answer for the given user prompt

    Returns:
        _type_: _description_ 
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            # Initialize ChatGPT with system prompt
            {
                "role": "system",
                "content": system_prompt
            },
            # Generate text relating to the user's prompt
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=kwargs.get("temperature", 1.0)
    )

    # Delete invalid links if any

    return response.choices[0].message.content


def generate_image(base_name: str, prompt: str, nb_image: int = 1) -> Tuple[str, List[str]]:
    """Generate a prompt and inject it to DALL-E

    Args:
        base_name (str): Images' base name
        prompt (_type_): Prompt to generate
        nb_image (_type_): number of image to generate

    Returns:
        list: Generated image names
    """
    # Ask ChatGPT a prompt to generate image with DALL-E
    with open(os.path.join(PROMPTS_PATH, "dall_e_prompter.txt"), "r") as file:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                # Initialize ChatGPT to be a helpful assistant
                {
                    "role": "system",
                    "content": file.read()
                },
                # Generate a subject
                {
                    "role": "user",
                    "content": f"SUBJECT {prompt}"
                }
            ],
        )

    # Create images
    image_response = openai.Image.create(
        prompt=response.choices[0].message.content,
        n=nb_image,
        size="1024x1024",
    )

    generated_image_names = []

    # Download image
    for index, image in enumerate(image_response['data']):
        img_data = requests.get(image['url']).content
        img_name = f'{base_name}_{index}.jpg'
        img_path = os.path.join(OUTPUT_PATH, img_name)
        with open(img_path, 'wb') as handler:
            handler.write(img_data)
            generated_image_names.append(f"./{img_name}")

    return response.choices[0].message.content ,generated_image_names
