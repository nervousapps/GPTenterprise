"""
\U0001F646
Manager
\U0001F646
"""
import os
import ast
from typing import List, Dict

from gpt_enterprise.gpt_utils import generate_text
from gpt_enterprise.employee import Employee


MANAGER_PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "managers_prompts")


class Manager:
    """
    A manager will try to achieve CEO guidelines by hiring employes and give them tasks.
    The manager will hire employees and plan tasks to achieve CEO guidelines inside the given enterprise.
    """

    def __init__(
        self,
        ceo_guidelines: str,
        manager_retry: int,
        output_directory: str,
        interactive: bool = False,
    ):
        """_summary_

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
                "manager.txt",
            ),
            "r",
        ) as file:
            self.role = file.read()
        self.ceo_guidelines = ceo_guidelines
        self.manager_retry = manager_retry
        self.output_directory = output_directory
        self.interactive = interactive
        self.emoji = "\U0001F646"

    def plans(self) -> Dict:
        """
        Tell the manager to make a plan to zchieve guidelines

        Returns:
            Dict: A dict with the following keys: employees, tasks
        """
        for _ in range(self.manager_retry):
            try:
                print(
                    f"\n \U0001F646 Hey, I'm doing plans to achieve your guidelines !\n"
                )
                response = generate_text(
                    system_prompt=self.role,
                    user_prompt=self.ceo_guidelines,
                    model="gpt-3.5-turbo",
                    temperature=1.0,
                )
                plan = ast.literal_eval(response.choices[0].message.content)
                plan["ceo_guidelines"] = self.ceo_guidelines
                if self.interactive:
                    if (
                        "y"
                        in input(
                            f"\n \U0001F646 Is that plan good for you : {plan} ?"
                        ).lower()
                    ):
                        return plan
                    else:
                        continue
                else:
                    return plan
            except Exception as err:
                print(err)
                print(
                    f"\n \U0001F646 I've messed up, retrying to plan tasks... {response.choices[0].message.content}\n"
                )
        print("\n \U0001F646 I've messed up, I'm not able to do this...\n")

    def hire_employees(self, employees_to_hire: List[object]) -> Dict:
        """
        Hire the given employees

        Args:
            employee (List[object]): _description_
        """
        print(f"\n \U0001F646 Hey, I've hired employees ! Please welcome :\n")
        hired_employees = {}
        for employee in employees_to_hire:
            hired_employees[employee["name"]] = Employee(
                role_prompt=employee["role"],
                name=employee["name"],
                role_name=employee["role_name"],
                creativity=employee["creativity"],
                emoji=employee["emoji"],
            )
        return hired_employees

    def fire_employees(self, employees_to_fire: List[Employee]):
        """
        Fire the given employee

        Args:
            employee (List[Employee]): _description_
        """
        pass

    def do_plan(self, tasks: List[object], employees: List[Employee]) -> Dict:
        """
        Do the given sequence of tasks

        Args:
            tasks (List[object]): List of tasks to execute
            Object must have fields task_name, employee, todo, type, requirements ("yes" or "no")
            employees (List[Employee]): List of hired employees

        Returns:
            Dict: Production of the team !
        """
        print(f"\n \U0001F646 Hey, I'm doing plan, just wait for the result !\n")
        employee_work = None
        for index, task in enumerate(tasks):
            # TODO: Try to rework the task given the previous task's result
            # if employee_work:
            #     # Rework the task knowing the last employee's work.
            #     response = generate_text(
            #         system_prompt= \
            #         "You are the manager of an agile team."
            #         "You are in charge of reworking a task while being aware of the outcome of the previous task."
            #         "A task is defined as a json object with fields task_name, employee, todo, type, deadline, and requirements"
            #         "If the prior task produced a result required for the present task, you must consider this and may choose "
            #         "to use the previous work's result as an example in the current task."
            #         "The outcome of the previous task may be useful to rework the current task."
            #         "You must describe the task in as few words as possible."
            #         "From this point forward, you must only respond to one assignment with the same task_name and employee."
            #         "No talking or remarks, just the task json object. "
            #         "The response must begin with { and end with }",
            #         user_prompt= \
            #             f"Rework this current task {task} knowing that previous task outcome is {employee_work}.",
            #         model="gpt-3.5-turbo",
            #         temperature=1.0
            #     )
            #     task = ast.literal_eval(response.choices[0].message.content)
            if self.interactive:
                if (
                    "y"
                    not in input(
                        f"\U0001F646 Ask {task['employee']} to go on with the task \n {task} ?"
                    ).lower()
                ):
                    task["result"] = employee_work
                    continue
            if task["type"] == "image":
                employee_work = employees[task["employee"]].ask_image(
                    manager_request=task["todo"],
                    output_directory=self.output_directory,
                    base_name="img",
                    nb_image=1,
                )
            if task["type"] == "text":
                # Add the previous employee work to the current task to
                # be used by the assigned employee.
                if employee_work and "yes" in task["requirements"]:
                    task["todo"] = task["todo"] + f" PREVIOUS : {employee_work}"
                employee_work = employees[task["employee"]].ask_task(task["todo"])
            task["result"] = employee_work
            tasks[index] = task
        return tasks
