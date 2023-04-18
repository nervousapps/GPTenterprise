"""
Enterprise
"""
import json
import openai

from gpt_enterprise.manager import Manager

class Enterprise:
    """
    An enterprise is composed of several employees driven by managers and a CEO (you)
    """
    def __init__(self, 
                 keyfile: str,
                 guidelines: str,
                 output_directory: str,
                 manager_retry: int,
                 company_name: str = "GPTenterprise") -> None:
        """_summary_

        Args:
            keyfile (str): _description_
            guidelines (str): _description_
            output_directory (str): _description_
            manager_retry (int): _description_
            company_name (str, optional): _description_. Defaults to "GPTenterprise".
        """        
        # Initialize openai api_key
        with open(keyfile, 'r') as file:
            openai.api_key = file.read()
        self.company_name = company_name
        self.employees = {}
        self.tasks_board = []

        print(f"\U0001F468 {guidelines}")

        # CEO ask the manager to create a project
        self.manager = Manager(
            ceo_guidelines=guidelines,
            manager_retry=manager_retry,
            output_directory=output_directory)

    def run_enterprise(self) -> dict:
        """
        

        Returns:
            dict: _description_
        """
        # Do plan
        manager_plans = self.manager.plans()
        print(json.dumps(manager_plans, indent=4))
        self.employees = self.manager.hire_employees(employees_to_hire=manager_plans["employees"])
        self.tasks_board = manager_plans["tasks"]
        self.tasks_board = self.manager.do_plan(
            tasks=self.tasks_board,
            employees=self.employees)
        manager_plans["tasks"] = self.tasks_board
        return manager_plans
        

    

    

    