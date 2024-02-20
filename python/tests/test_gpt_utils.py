"""
Test gpt utilities
"""

import time
import pytest
from gpt_enterprise.gpt_utils import generate_image, generate_text

from .conftest import mock_open_ai_response_object


def test_generate_text(mocker):
    """
    Test generate_text
    """

    def mock_generate_text(model: str, messages, temperature: float) -> str:
        time.sleep(1)  # random.random()*10)
        return mock_open_ai_response_object(mocker=mocker, content="Do something")

    mocker.patch(
        "gpt_enterprise.gpt_utils.openai.chat.completions.create", mock_generate_text
    )
    response = generate_text(
        system_prompt="test", user_prompt="test", model="test", temperature=1.0
    )
    assert response.choices[0].message.content == "Do something"


def test_generate_image(mocker):
    """
    Test generate_image
    """

    def mock_generate_text(model: str, messages) -> str:
        time.sleep(1)  # random.random()*10)
        return mock_open_ai_response_object(mocker=mocker, content="Do something")

    mocker.patch(
        "gpt_enterprise.gpt_utils.openai.chat.completions.create", mock_generate_text
    )
    mocker.patch(
        "gpt_enterprise.gpt_utils.openai.Image.create", return_value={"data": []}
    )
    prompt, image = generate_image(
        system_prompt="test",
        base_name="test",
        user_prompt="test",
        output_directory="test",
        nb_image=1,
    )
    assert (prompt, image) == ("Do something", [])
