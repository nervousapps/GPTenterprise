"""
\U0001F3E2
Enterprise
\U0001F3E2
"""
import os

from gpt_enterprise.llm_utils import LLMutils
from gpt_enterprise.team_leader import TeamLeader
from gpt_enterprise.scrum_master import ScrumMaster


class Enterprise:
    """
    An enterprise is composed of several employees driven by managers and a CEO (you)
    """

    def __init__(
        self,
        guidelines: str,
        output_directory: str,
        manager_retry: int,
        provider: LLMutils,
        company_name: str = "GPTenterprise",
        interactive: bool = False,
        asynchronous: bool = True,
    ):
        """
        Create an enterprise with CEO guidelines and hire:
            - a team leader that wil be responsible of managing employees
            - a scrum master that wil be responsible of managing tasks

        Args:
            keyfile (str): Pth to openai key file
            guidelines (str): CEO guidelines
            output_directory (str): Output directory
            manager_retry (int): How many times manager will retry to do the plan
            company_name (str, optional): Enterprise's name. Defaults to "GPTenterprise".
            interactive (bool): Defaults to False
            asynchronous (bool): Defaults to True
        """
        self.provider = provider
        self.company_name = company_name
        self.employees = {}
        self.tasks_board = []
        self.interactive = interactive
        self.asynchronous = asynchronous
        self.ceo_guidelines = guidelines

        print(f"\U0001F468 {self.ceo_guidelines}")

        # Create output directory if not exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory, exist_ok=True)

        # Create the team leader
        self.team_leader = TeamLeader(
            ceo_guidelines=guidelines,
            manager_retry=manager_retry,
            output_directory=output_directory,
            interactive=interactive,
            provider=self.provider
        )
        # Create the scrum master
        self.scrum_master = ScrumMaster(
            ceo_guidelines=guidelines,
            manager_retry=manager_retry,
            output_directory=output_directory,
            interactive=interactive,
            provider=self.provider
        )

    async def run_enterprise(self) -> dict:
        """
        Run the enterprise:
            - Ask the team leader to hire employees
            - Ask the scrum master to plan tasks
            - Ask the scrum master to do tasks
            - Return the employees production

        Returns:
            dict: Production wih employess and update tasks with result
        """
        production = {}
        # Hire needed employees
        self.employees = self.team_leader.hire_employees()
        # Extract tasks from manager plan
        self.tasks_board = self.scrum_master.plan_tasks(
            [employee for _, employee in self.employees.items()]
        )
        # Do the plan asynchronously
        if not self.asynchronous:
            production_tasks_board = self.scrum_master.do_plan(
                tasks=self.tasks_board, employees=self.employees
            )
        else:
            production_tasks_board = await self.scrum_master.do_plan_async(
                tasks=self.tasks_board, employees=self.employees
            )
        # Add CEO guidelines to the plan
        production["ceo_guidelines"] = self.ceo_guidelines
        # Return the result of the plan
        production["tasks"] = production_tasks_board
        # Add final result
        production["final_result"] = production_tasks_board[-1]["result"]
        if self.interactive:
            if (
                "y"
                in input(
                    f"{self.scrum_master.emoji} Here is the final result: \n {production['final_result']} \n Is this final result correct? (y/n) \n \U0001F468"
                ).lower()
            ):
                print(
                    f"{self.scrum_master.emoji} Great ! Nice to have worked with you !"
                )
            else:
                if "y" in (
                    input("Do you want me to retry ? (y/n)\n \U0001F468").lower()
                    or "no"
                ):
                    return await self.run_enterprise()

        return production
