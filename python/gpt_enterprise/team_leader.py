"""
\U0001F57A
Team leader
\U0001F57A
"""
import os
import ast
import json
from typing import List, Dict

from gpt_enterprise.llm_utils import LLMutils, EMPLOYEE_PROMPTS_PATH
from gpt_enterprise.employee import Employee


MANAGER_PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts", "managers")


class TeamLeader:
    """
    A team leader will try to achieve CEO guidelines by hiring employes.
    """

    def __init__(
        self,
        ceo_guidelines: str,
        manager_retry: int,
        output_directory: str,
        provider: LLMutils,
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
                "team_leader.txt",
            ),
            "r",
        ) as file:
            self.role = file.read()
        self.provider = provider
        self.ceo_guidelines = ceo_guidelines
        self.manager_retry = manager_retry
        self.output_directory = output_directory
        self.interactive = interactive
        self.emoji = "\U0001F57A"
        self.tasks = None

    def hire_employees(self) -> List[Dict[str, Employee]]:
        """
        Ask the team leader to find and hire employees

        Returns:
            List[Dict[str, Employee]]: A list containing employee CV by employee name
        """
        employees_to_hire = None
        for _ in range(self.manager_retry):
            try:
                print(
                    f"\n {self.emoji} Hey, I'm hiring employees to achieve your guidelines !\n"
                )
                response =self.provider.generate_text(
                    system_prompt=self.role,
                    user_prompt=f"Here are the CEO guidelines : {self.ceo_guidelines}",
                    temperature=1.0,
                )
                # Convert to dict
                employees_to_hire = ast.literal_eval(
                    response
                )
                if not isinstance(employees_to_hire, list):
                    employees_to_hire = [employees_to_hire]
                print(json.dumps(employees_to_hire, indent=4))
                if self.interactive:
                    if "y" in (
                        input(
                            f"\n {self.emoji} Are these employees good for you ?"
                        ).lower()
                        or "y"
                    ):
                        break
                    else:
                        continue
                else:
                    break
            except Exception as err:
                print(err)
                print(
                    f"\n {self.emoji} I've messed up, retrying to find employees... \n Error : \n {response}\n"
                )
        print(f"\n Ok, I've hired them ! Please welcome :\n")
        hired_employees = {}
        if employees_to_hire:
            for index, employee in enumerate(employees_to_hire):
                hired_employees[employee.get("name", f"GUY_{index}")] = Employee(
                    role_prompt=employee.get("role", f"Undefined_{index}"),
                    name=employee.get("name", f"GUY_{index}"),
                    role_name=employee.get("role_name", f"Undefined_{index}"),
                    creativity=float(employee.get("creativity", 1.0)),
                    emoji=employee.get("emoji", "\U0001F469"),
                    provider=self.provider
                )
        # Add a helpful employee for task assigned to a non hired one
        hired_employees["helpful"] = Employee(
            role_filename=os.path.join(EMPLOYEE_PROMPTS_PATH, "helpful_employee.txt"),
            role_name="Helpful employee",
            provider=self.provider
        )
        return hired_employees

    def fire_employees(self, employees_to_fire: List[Employee]):
        """
        Fire the given employee

        Args:
            employee (List[Employee]): _description_
        """
        pass
