"""
GPTenterprise is an AI driven enterprise.
"""
import os
import sys
import json
from dotenv import load_dotenv
from gpt_enterprise.enterprise import Enterprise


def main():
    load_dotenv(dotenv_path=sys.argv[1])

    keyfile = os.getenv("KEYFILE")
    company_name = os.getenv("COMPANY_NAME")
    guidelines = os.getenv("CEO_GUIDELINES")
    output_directory = os.getenv("OUTPUT_DIRECTORY")
    manager_retry = int(os.getenv("MANAGER_RETRY"))

    enterprise = Enterprise(
        keyfile=keyfile,
        company_name=company_name,
        guidelines=guidelines,
        output_directory=output_directory,
        manager_retry=manager_retry
    )
    production = enterprise.run_enterprise()
    # Write the production in a file
    with open(os.path.join(output_directory, "production"), "w") as file:
        file.write(json.dumps(production, indent=4))

if __name__ == "__main__":
    main()