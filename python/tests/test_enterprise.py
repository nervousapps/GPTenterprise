"""
Test enterprise class
"""
import os
import ast
import asyncio
import time
from typing import Tuple, List
from gpt_enterprise.enterprise import Enterprise
from gpt_enterprise.employee import Employee


from .conftest import EMPLOYEES_FILES_DIR, TASKS_FILES_DIR, mock_open_ai_response_object


def test_enterprise():
    enterprise = Enterprise(
        keyfile=os.path.join(
            os.path.dirname(__file__), "..", "..", "openai_key.txt.template"
        ),
        guidelines="test",
        output_directory="test",
        manager_retry=1,
        company_name="test",
    )

    assert enterprise.company_name == "test"
    assert enterprise.ceo_guidelines == "test"
    assert enterprise.team_leader.output_directory == "test"
    assert enterprise.scrum_master.manager_retry == 1


def test_run_enterprise(mocker):
    """
    Test to run a fake enterprise
    """

    def mock_generate_text(
        system_prompt: str, user_prompt: str, model: str, temperature: float
    ) -> str:
        time.sleep(1)  # random.random()*10)
        return mock_open_ai_response_object(mocker=mocker, content="Do something")

    def mock_generate_image(
        base_name: str,
        user_prompt: str,
        output_directory: str,
        system_prompt: str = "",
        nb_image: int = 1,
    ) -> Tuple[str, List[str]]:
        time.sleep(1)  # random.random()*10)
        return ("Test", ["img1.jpg"])

    # Mock function and method that requests openai API (to avoid costs)
    mocker.patch("gpt_enterprise.employee.generate_text", mock_generate_text)
    mocker.patch("gpt_enterprise.employee.generate_image", mock_generate_image)
    # Use a previously generated employees list (to avoid costs)
    with open(os.path.join(EMPLOYEES_FILES_DIR, "employees.txt"), "r") as file:
        employees = ast.literal_eval(file.read())
        hired_employees = {}
        for employee in employees:
            hired_employees[employee["name"]] = Employee(
                role_prompt=employee["role"],
                name=employee["name"],
                role_name=employee["role_name"],
                creativity=float(employee["creativity"]),
                emoji=employee["emoji"],
            )
    mocker.patch(
        "gpt_enterprise.team_leader.TeamLeader.hire_employees",
        return_value=hired_employees,
    )
    # Use a previously generated plan_tasks (to avoid costs)
    with open(os.path.join(TASKS_FILES_DIR, "tasks.txt"), "r") as file:
        plan_tasks = ast.literal_eval(file.read())
    mocker.patch(
        "gpt_enterprise.scrum_master.ScrumMaster.plan_tasks", return_value=plan_tasks
    )

    # Run asynchronously
    enterprise_async = Enterprise(
        keyfile=os.path.join(
            os.path.dirname(__file__), "..", "..", "openai_key.txt.template"
        ),
        guidelines="test",
        output_directory="test",
        manager_retry=1,
        company_name="test",
    )

    start_time = time.time()
    production_async = asyncio.run(enterprise_async.run_enterprise())
    duration_async = time.time() - start_time
    assert production_async
    assert all(task.get("result") for task in production_async.get("tasks"))

    # Run sequentially
    # Use a previously generated plan (to avoid costs)
    with open(os.path.join(TASKS_FILES_DIR, "tasks.txt"), "r") as file:
        plan_tasks = ast.literal_eval(file.read())
    mocker.patch(
        "gpt_enterprise.scrum_master.ScrumMaster.plan_tasks", return_value=plan_tasks
    )
    enterprise_seq = Enterprise(
        keyfile=os.path.join(
            os.path.dirname(__file__), "..", "..", "openai_key.txt.template"
        ),
        guidelines="test",
        output_directory="test",
        manager_retry=1,
        company_name="test",
        asynchronous=False,
    )

    start_time = time.time()
    production_seq = asyncio.run(enterprise_seq.run_enterprise())
    duration_seq = time.time() - start_time
    assert production_seq
    assert all(task.get("result") for task in production_seq.get("tasks"))

    print(f"Async duration: {duration_async}")
    print(f"Sequencial duration: {duration_seq}")
