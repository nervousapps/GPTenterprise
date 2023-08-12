"""
\U0001F9E0
LLM utils
\U0001F9E0
"""
import os
import requests
from typing import Tuple, List

import openai
from gpt_enterprise.gpt4all_utils import GPT4ALLUtils


EMPLOYEE_PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts", "employees")

class LLMutils:
    """
    LLMutils
    """
    def __init__(self, provider: str, **kwargs) -> None:
        if provider not in ["gpt4all", "openai"]:
            raise Exception("Only gpt4all and openai are supported providers for now !")
        if provider == "openai":
            # Initialize openai api_key
            with open(kwargs.get("keyfile"), "r") as file:
                openai.api_key = (file.read()).strip()
            self.provider = openai
        print(kwargs)
        if provider == "gpt4all":
            self.provider = GPT4ALLUtils(
                model_name=kwargs.get("model_name") if kwargs.get("model_name") else "ggml-gpt4all-j-v1.3-groovy",
                model_path=kwargs.get("model_path"),
                model_type=kwargs.get("model_type"),
                allow_download=kwargs.get("allow_download", True)
            )

    def generate_text(
        self, system_prompt: str, user_prompt: str, model: str = "gpt-4", temperature: float = None
    ) -> str:
        """


        Args:
            system_prompt (str): Initialize the system with the given system prompt
            user_prompt (str): Assistant will try to give the best answer for the given user prompt
            model (str): OpenAI model to be used
            temperature (float): Temperature

        Returns:
            Generator: GPT response object
        """
        response = self.provider.ChatCompletion.create(
            model=model,
            messages=[
                # Initialize GPT with system prompt
                {
                    "role": "system",
                    "content": system_prompt,  # + " Use less words as possible."
                },
                # Generate text relating to the user's prompt
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )

        if self.provider == openai:
            response = response.choices[0].message.content

        if isinstance(self.provider, GPT4ALLUtils):
            response = response["choices"][0]["message"]["content"]

        return str(response)


    def generate_image(
        self,
        base_name: str,
        user_prompt: str,
        output_directory: str,
        system_prompt: str = "",
        nb_image: int = 1,
    ) -> Tuple[str, List[str]]:
        """
        Generate a prompt base on user_prompt and inject it to DALL-E
        to generate images.

        Args:
            system_prompt (str): Initialize the system with the given system prompt
            user_prompt (str): Assistant will try to give the best answer for the given user prompt
            base_name (str): Images' base name
            output_directory (str): Images' output directory
            nb_image (_type_): Number of image to generate

        Returns:
            list: Generated image names
        """
        # Ask ChatGPT a prompt to generate image with DALL-E
        with open(os.path.join(EMPLOYEE_PROMPTS_PATH, "dall_e_prompter.txt"), "r") as file:
            response = self.provider.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    # Initialize ChatGPT to be a helpful assistant but that it remains the employee
                    {
                        "role": "system",
                        "content": f"{file.read()}"
                        + f" You are also {system_prompt} But keep in mind that {file.read()}"
                        if system_prompt
                        else "",
                    },
                    # Generate a subject
                    {"role": "user", "content": f"SUBJECT {user_prompt}"},
                ],
            )

        if self.provider == openai:
            response = response.choices[0].message.content
        
        if isinstance(self.provider, GPT4ALLUtils):
            response = response["choices"][0]["message"]["content"]

        # Create images, troncate prompt to 70 characters
        # to be sure it will be accepted by DALL-E
        image_response = self.provider.Image.create(
            prompt=response[:70],
            n=nb_image,
            size="1024x1024",
        )

        generated_image_names = []

        # Download images
        for index, image in enumerate(image_response["data"]):
            img_data = requests.get(image["url"]).content
            img_name = f"{base_name}_{index}.jpg"
            img_path = os.path.join(output_directory, img_name)
            with open(img_path, "wb") as handler:
                handler.write(img_data)
                generated_image_names.append(f"./{img_name}")

        return response, generated_image_names
