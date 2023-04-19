"""
Enterprise
"""
import os
import json
import openai

from gpt_enterprise.manager import Manager


class Enterprise:
    """
    \U0001F3E2
    An enterprise is composed of several employees driven by managers and a CEO (you)
    """

    def __init__(
        self,
        keyfile: str,
        guidelines: str,
        output_directory: str,
        manager_retry: int,
        company_name: str = "GPTenterprise",
        interactive: bool = False,
    ):
        """
        Create an enterprise with CEO guidelines and hire a manager.

        Args:
            keyfile (str): Pth to openai key file
            guidelines (str): CEO guidelines
            output_directory (str): Output directory
            manager_retry (int): How many times manager will retry to do the plan
            company_name (str, optional): Enterprise's name. Defaults to "GPTenterprise".
            interactive (bool): Defaults to False
        """
        # Initialize openai api_key
        with open(keyfile, "r") as file:
            openai.api_key = (file.read()).strip()
        self.company_name = company_name
        self.employees = {}
        self.tasks_board = []
        self.interactive = interactive

        print(f"\U0001F468 {guidelines}")

        # Create output directory if not exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory, exist_ok=True)

        # CEO ask the manager to create a project
        self.manager = Manager(
            ceo_guidelines=guidelines,
            manager_retry=manager_retry,
            output_directory=output_directory,
            interactive=interactive,
        )

    def run_enterprise(self) -> dict:
        """
        Run the enterprise:
            - Ask the manager to create a project
            - Hire employees
            - Do the plan
            - Return the result of the plan

        Returns:
            dict: Plan wih employess and update tasks with result
        """
        # Do plan
        manager_plans = self.manager.plans()
        print(json.dumps(manager_plans, indent=4))
        # Hire needed employees
        self.employees = self.manager.hire_employees(
            employees_to_hire=manager_plans["employees"]
        )
        # Extract tasks from manager plan
        self.tasks_board = manager_plans["tasks"]
        # Do the plan
        production_tasks_board = self.manager.do_plan(
            tasks=self.tasks_board, employees=self.employees
        )
        # Return the result of the plan
        manager_plans["tasks"] = production_tasks_board
        # Add final result
        manager_plans["final_result"] = production_tasks_board[-1]["result"]
        if self.interactive:
            if (
                "y"
                in input(
                    f"{self.manager.emoji} Here is the final result: \n {manager_plans['final_result']} \n Is this final result correct? (y/n) \n \U0001F468"
                ).lower()
            ):
                print(f"{self.manager.emoji} Great ! Nice to have worked with you !")
            else:
                if "y" in input("Do you want me to retry ? (y/n)\n \U0001F468").lower():
                    return self.run_enterprise()
                else:
                    quit()
        return manager_plans
