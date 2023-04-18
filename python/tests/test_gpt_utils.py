"""
Test gpt utilities
"""
import pytest
from gpt_enterprise.gpt_utils import generate_image, generate_text


def test_generate_text(mocker):
    """
    Test generate_text
    """
    mocker.patch(
        "gpt_enterprise.gpt_utils.openai.ChatCompletion.create", return_value="test"
    )
    text = generate_text(
        system_prompt="test", user_prompt="test", model="test", temperature=1.0
    )
    assert text == "test"


@pytest.mark.skip(reason="Find a way to return response object")
def test_generate_image(mocker):
    """
    Test generate_image
    """
    mocker.patch(
        "gpt_enterprise.gpt_utils.openai.ChatCompletion.create", return_value="test"
    )
    mocker.patch("gpt_enterprise.gpt_utils.openai.Image.create", return_value="test")
    image = generate_image(
        system_prompt="test",
        base_name="test",
        user_prompt="test",
        output_directory="test",
        nb_image=1,
    )
    assert image == "test"
