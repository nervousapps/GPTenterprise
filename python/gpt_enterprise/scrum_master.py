"""
\U0001F3C2
Scrum Master
\U0001F3C2
"""
import os
import ast
import time
import json
import asyncio
from typing import List, Dict

from gpt_enterprise.gpt_utils import generate_text
from gpt_enterprise.employee import Employee


MANAGER_PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts", "managers")


class ScrumMaster:
    """
    A scrum master will try to achieve CEO guidelines by creating tasks.
    The scrum master will plan tasks and assign them to employees to achieve
    CEO guidelines inside the given enterprise.
    """

    def __init__(
        self,
        ceo_guidelines: str,
        manager_retry: int,
        output_directory: str,
        interactive: bool = False,
    ):
        """

        Args:
            ceo_guidelines (str): _description_
            manager_retry (int): _description_
            output_directory (str): _description_
            interactive (bool): Defaults to False
        """
        with open(
            os.path.join(
                MANAGER_PROMPTS_PATH
                if not os.getenv("CUSTOM_MANAGER_PROMPTS_PATH")
                else os.getenv("CUSTOM_MANAGER_PROMPTS_PATH"),
                "scrum_master.txt",
            ),
            "r",
        ) as file:
            self.role = file.read()
        self.ceo_guidelines = ceo_guidelines
        self.manager_retry = manager_retry
        self.output_directory = output_directory
        self.interactive = interactive
        self.emoji = "\U0001F3C2"
        self.tasks = None

    def plan_tasks(self, employees: List[Employee]) -> List[Dict]:
        """
        Tell the scrum master to make create and plan tasks to achieve guidelines

        Returns:
            List[object]: A list with all tasks
        """
        # Build the list of hired employees with their role name and name
        hired_employees = [
            {"name": employee.name, "role_name": employee.role_name}
            for employee in employees
        ]
        self.ceo_guidelines += f"AVAILABLE_EMPLOYEES: {hired_employees}"
        for _ in range(self.manager_retry):
            try:
                print(
                    f"\n {self.emoji} Hey, I'm doing plans to achieve your guidelines !\n"
                )
                response = generate_text(
                    system_prompt=self.role,
                    user_prompt=self.ceo_guidelines,
                    model=os.getenv("GPT_VERSION", "gpt-3.5-turbo"),  # TODO
                    temperature=1.0,
                )
                # Convert to dict
                task_plan = ast.literal_eval(response.choices[0].message.content)
                print(json.dumps(task_plan, indent=4))
                if self.interactive:
                    if "y" in (
                        input(
                            f"\n {self.emoji} Is that task plan good for you ?"
                        ).lower()
                        or "y"
                    ):
                        return task_plan
                    else:
                        continue
                return task_plan
            except Exception as err:
                print(err)
                print(
                    f"\n {self.emoji} I've messed up, retrying to plan tasks... \n Error : \n {response.choices[0].message.content}\n"
                )
        print(f"\n {self.emoji} I've messed up, I'm not able to do this...\n")
        raise err

    def do_plan(self, tasks: List[object], employees: List[Employee]) -> List[Dict]:
        """
        Do the given sequence of tasks

        Args:
            tasks (List[object]): List of tasks to execute
            Object must have fields task_name, employee_name, todo, type, requirements ("yes" or "no")
            employees (List[Employee]): List of hired employees

        Returns:
            List[Dict]: Production of the team ! All tasks have the result field
        """
        self.tasks = tasks
        print(f"\n {self.emoji} Hey, I'm doing plan, just wait for the result !\n")
        # Do until all tasks have the result field set
        while not all(task.get("result") for task in self.tasks):
            for index, task in enumerate(self.tasks):
                # Do tasks without any requirements
                # TODO: Do it asynchronously
                if "no" in str(task.get("requirements", "")) and not task.get("result"):
                    if self.interactive and "y" not in (
                        input(
                            f"{self.emoji} Ask {task['employee_name']} to go on with the task \n {task} ?"
                        ).lower()
                        or "y"
                    ):
                        continue
                    self._employee_task(index, task, employees[task["employee_name"]])
                # Do tasks that requires result of other tasks
                elif (
                    "no" not in str(task.get("requirements", "no"))
                    and not task.get("result")
                    and self.tasks[int(task["requirements"])].get("result")
                ):
                    # Add the previous employee work to the current task to
                    # be used by the assigned employee.
                    task[
                        "todo"
                    ] += f" Here is the work done by {self.tasks[int(task['requirements'])]['employee_name']} : {self.tasks[int(task['requirements'])]['result']}"
                    if self.interactive and "y" not in (
                        input(
                            f"{self.emoji} Ask {task['employee_name']} to go on with the task \n {task} ?"
                        ).lower()
                        or "y"
                    ):
                        continue
                    self._employee_task(index, task, employees[task["employee_name"]])
        return self.tasks

    async def do_plan_async(
        self, tasks: List[object], employees: List[Employee]
    ) -> List[Dict]:
        """
        Do the given sequence of tasks asynchronously (not compatible with interactive mode).

        Args:
            tasks (List[object]): List of tasks to execute
            Object must have fields task_name, employee_name, todo, type, requirements ("yes" or "no")
            employees (List[Employee]): List of hired employees

        Returns:
            List[Dict]: Production of the team ! All tasks have the result field
        """
        print(f"\n {self.emoji} Hey, I'm doing plan, just wait for the result !\n")
        self.tasks = tasks
        # Create futures
        all_tasks = []
        for task_index, task in enumerate(tasks):
            # employee_name field may be a list of employe name
            if isinstance(task["employee_name"], list):
                for employee_name in task["employee_name"]:
                    all_tasks.append(
                        asyncio.to_thread(
                            self._wait_for_result,
                            task_index,
                            task,
                            employees[employee_name],
                        )
                    )
            else:
                all_tasks.append(
                    asyncio.to_thread(
                        self._wait_for_result,
                        task_index,
                        task,
                        employees[task["employee_name"]],
                    )
                )
        # Run all futures in parallel
        await asyncio.gather(*all_tasks)
        return self.tasks

    def _wait_for_result(self, task_index: int, task: dict, employee: Employee) -> dict:
        """
        Wait for required task result to be available if the current task requires it.

        Args:
            task (dict): _description_
            employee (Employee): _description_

        Returns:
            dict: _description_
        """
        if "no" not in str(task.get("requirements", "no")):
            counter = 0
            while not self.tasks[int(task["requirements"])].get("result"):
                time.sleep(0.01)
                counter += 1
                if counter >= 2000:
                    print(
                        f"Waiting for {self.tasks[int(task['requirements'])]['employee_name']} to finish..."
                    )
                    counter = 0
            # Add the previous employee work to the current task to
            # be used by the assigned employee.
            task[
                "todo"
            ] += f" Here is the work done by {self.tasks[int(task['requirements'])]['employee_name']} : {self.tasks[int(task['requirements'])]['result']}"

        print(
            f"{self.emoji} {employee.name} is doing task {task_index} : {task['todo']}"
        )
        self._employee_task(task_index, task, employee)

    def _employee_task(self, task_index: int, task: dict, employee: Employee):
        """
        Ask given employee to do the task and set the result field.
        The global list of tasks is then updated with the modified task.

        Args:
            task_index (int): _description_
            task (dict): _description_
            employee (Employee): _description_
        """
        todo = task["todo"]
        if task["type"] == "image":
            # Get number of images to ask from the task todo
            nb_image = 2
            if "NB_IMAGES" in todo:
                nb_image = int(todo.split("NB_IMAGES")[1][-1])
                todo = todo.split("NB_IMAGES")[0]
            task["result"] = employee.ask_image(
                manager_request=todo,
                output_directory=self.output_directory,
                base_name=employee.name,
                nb_image=max(nb_image, 5),
            )
        elif task["type"] == "text":
            task["result"] = employee.ask_task(todo)
        self.tasks[task_index] = task
