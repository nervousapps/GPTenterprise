"""
\U0001F469
Employee
\U0001F469
"""

import os
from typing import List, Tuple

from gpt_enterprise.gpt_utils import generate_text, generate_image


class Employee:
    """
    The Employee class represents an employee that act as the given system prompt.
    It can be used to do all you want, just tell him how to act.
    """

    def __init__(
        self,
        role_name: str,
        role_filename: str = None,
        role_prompt: str = None,
        name: str = "GUY",
        emoji: str = "\U0001F469",
        creativity: float = 1.0,
        gpt_version: str = os.getenv("GPT_VERSION", "gpt-3.5-turbo"),  # TODO
    ):
        """
        Give your employee a role file for him to read it and act like you want.

        Employe name and role name form the unique identifier for the employee.

        Args:
            role_filename (str): Path to prompt file
            role_prompt (str): Prompt string
            role_name (str): Role name
            name (str, optional): _description_. Defaults to "GUY".
            creativity (float, optional): _description_. Defaults to 1.0.
            gpt_version (str, optional): _description_. Defaults to "gpt-3.5-turbo".
        """
        if not role_prompt and role_filename:
            with open(role_filename, "r") as file:
                self.role = file.read()
        elif role_prompt:
            self.role = role_prompt
        else:
            print(
                "Your employee role prompt is not clear, please provide a role_filename or a role_prompt. "
                "He will just be a helpfull amployee."
            )
            self.role = "You are a helpfull employee."
        self.role_name = role_name
        if not role_name:
            self.role_name = "employee"
        self.name = name
        self.emoji = emoji
        try:
            print(
                f"\n {self.emoji} Hi, I'm a {self.role_name}, my name is {self.name}.\n"
            )
        except Exception:
            self.emoji = "\U0001F469"
            print(
                f"\n {self.emoji} Hi, I'm a {self.role_name}, my name is {self.name}.\n"
            )
        self.creativity = creativity
        self.gpt_version = gpt_version

    def ask_task(self, manager_request: str) -> str:
        """
        Ask employee to do the given task.

        Args:
            manager_request (str): The manager request (it can be rude... but may not ^^)

        Returns:
            str: The employee response as text string
        """
        response = ""
        try:
            response = generate_text(
                system_prompt=self.role,
                user_prompt=manager_request,
                model=self.gpt_version,
                temperature=self.creativity,
            )
            response = response.choices[0].message.content
        except Exception as err:
            print(f"\n {self.emoji} {self.name}: {err}\n")
        print(
            f"\n {self.emoji} {self.name}: As a {self.role_name}, here is my work: {response}\n"
        )
        return response

    def ask_image(
        self,
        manager_request: str,
        output_directory: str,
        base_name: str = "img",
        nb_image: int = 1,
    ) -> Tuple[str, List[str]]:
        """
        Ask the employee to create an image with the specified manager request.
        The employee will generate a prompt and ask DALL-E to generate the specified
        number of images.

        Args:
            manager_request (str): The manager request (it can be rude... but may not ^^)
            output_directory (str): Output directory
            base_name (str): The base name of the image. Defaults to img
            nb_image (int, optional): _description_. Defaults to 1.

        Returns:
            Tuple[str, List[str]]: The generated prompt and list of images paths
        """
        prompt = ""
        image_paths = []
        try:
            prompt, image_paths = generate_image(
                system_prompt=self.role,
                base_name=base_name,
                user_prompt=manager_request,
                output_directory=output_directory,
                nb_image=nb_image,
            )
        except Exception as err:
            print(f"\n {self.emoji} {self.name}: {err}\n")
        print(
            f"\n {self.emoji} {self.name}: As a {self.role_name} "
            f"image generator, here is the image description I made: {prompt}. \n "
            f"Image paths are {image_paths} \n"
        )
        return prompt, image_paths
