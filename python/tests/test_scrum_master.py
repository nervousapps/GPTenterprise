"""
Test manager
"""

import os
import ast
import pytest

from .conftest import TASKS_FILES_DIR, mock_open_ai_response_object


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "plan_path, fail",
    [
        (os.path.join(TASKS_FILES_DIR, "tasks.txt"), False),
        (os.path.join(TASKS_FILES_DIR, "tasks_malformed_json.txt"), True),
        (os.path.join(TASKS_FILES_DIR, "tasks_wrong_fields.txt"), True),
    ],
)
async def test_plan_tasks(mocker, scrum_master_test, fake_employees, plan_path, fail):
    """
    Test manager
    """

    def mock_generate_text(
        system_prompt: str, user_prompt: str, model: str, temperature: float
    ) -> str:
        # Use a previously generated plan (to avoid costs)
        with open(plan_path, "r") as file:
            generated_text = file.read()
            return mock_open_ai_response_object(mocker=mocker, content=generated_text)

    # Mock function and method that requests openai API (to avoid costs)
    mocker.patch("gpt_enterprise.scrum_master.generate_text", mock_generate_text)
    fake_employees = [employee for _, employee in fake_employees.items()]
    if fail:
        with pytest.raises(Exception) as err:
            plan = scrum_master_test.plan_tasks(fake_employees)
    else:
        plan = scrum_master_test.plan_tasks(fake_employees)
        assert plan


# TODO: add parametrize with test files
def test_do_plan(mocker, scrum_master_test, fake_employees):
    # Mock function and method that requests openai API (to avoid costs)
    mocker.patch(
        "gpt_enterprise.employee.generate_text",
        return_value=mock_open_ai_response_object(
            mocker=mocker, content="This is only a test"
        ),
    )
    mocker.patch(
        "gpt_enterprise.employee.generate_image",
        return_value=("Do something", ["./img.jpg"]),
    )
    with open(os.path.join(TASKS_FILES_DIR, "tasks.txt"), "r") as file:
        plan = ast.literal_eval(file.read())

    production = scrum_master_test.do_plan(plan, fake_employees)

    assert production


# TODO: add parametrize with test files
@pytest.mark.asyncio
@pytest.mark.parametrize("test_file", ["tasks.txt", "tasks_requirements_list.txt"])
async def test_do_plan_async(mocker, scrum_master_test, fake_employees, test_file):
    # Mock function and method that requests openai API (to avoid costs)
    mocker.patch(
        "gpt_enterprise.employee.generate_text",
        return_value=mock_open_ai_response_object(
            mocker=mocker, content="This is only a test"
        ),
    )
    mocker.patch(
        "gpt_enterprise.employee.generate_image",
        return_value=("Do something", ["./img.jpg"]),
    )
    with open(os.path.join(TASKS_FILES_DIR, test_file), "r") as file:
        plan = ast.literal_eval(file.read())

    production = await scrum_master_test.do_plan_async(plan, fake_employees)

    assert production
