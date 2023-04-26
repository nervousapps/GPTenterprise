"""
Test manager
"""
import os
import ast
import pytest

from .conftest import EMPLOYEES_FILES_DIR, mock_open_ai_response_object


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "plan_path, nb_employees, fail",
    [
        (os.path.join(EMPLOYEES_FILES_DIR, "employees.txt"), 3, False),
        (os.path.join(EMPLOYEES_FILES_DIR, "employees_malformed_json.txt"), None, True),
        (os.path.join(EMPLOYEES_FILES_DIR, "employees_wrong_fields.txt"), None, True),
    ],
)
async def test_hire_employees(mocker, team_leader_test, plan_path, nb_employees, fail):
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
    mocker.patch("gpt_enterprise.team_leader.generate_text", mock_generate_text)
    if fail:
        with pytest.raises(Exception) as err:
            hired_employees = team_leader_test.hire_employees()
    else:
        hired_employees = team_leader_test.hire_employees()
        assert hired_employees
        assert len(hired_employees.items()) == nb_employees
