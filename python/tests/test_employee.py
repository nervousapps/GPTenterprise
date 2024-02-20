"""
Test cases for the employee module
"""

import os
import pytest
from gpt_enterprise.employee import Employee

from .conftest import TEST_FILES_DIR, mock_open_ai_response_object


@pytest.mark.parametrize(
    "role_name, role_filename, role_prompt",
    [
        ("developer", "developer.txt", "What is your task?"),
        ("developer", os.path.join(TEST_FILES_DIR, "developer.txt"), None),
        ("designer", None, "What is your image?"),
        ("designer", None, None),
        (None, None, None),
    ],
)
def test_employee_creation(role_name, role_filename, role_prompt):
    """
    Test case for employee creation
    """
    employee = Employee(role_name, role_filename, role_prompt)
    if not role_name:
        assert employee.role_name == "employee"
    else:
        assert employee.role_name == role_name
    assert employee.name == "GUY"
    if role_filename and not role_prompt:
        with open(role_filename, "r") as file:
            assert employee.role == file.read()
    elif role_prompt:
        assert employee.role == role_prompt
    else:
        assert employee.role == "You are a helpfull employee."


def test_employee_ask_task(mocker):
    """
    Test case for employee asking task
    """
    employee = Employee("developer", role_prompt="What is your task?")
    mocker.patch(
        "gpt_enterprise.employee.generate_text",
        return_value=mock_open_ai_response_object(
            mocker=mocker, content="Do something"
        ),
    )
    assert employee.ask_task("Do something") == "Do something"


def test_employee_ask_image(mocker):
    """
    Test case for employee asking image
    """
    employee = Employee("developer", role_prompt="What is your task?")
    mocker.patch(
        "gpt_enterprise.employee.generate_text",
        return_value=mock_open_ai_response_object(
            mocker=mocker, content="Do something"
        ),
    )
    assert employee.ask_task("Do something") == "Do something"
