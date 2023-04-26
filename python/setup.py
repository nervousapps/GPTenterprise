"""
Module setup
"""
from setuptools import setup, find_packages

REQUIREMENTS = [
    "python-dotenv",
    "openai",
]

setup(
    name="GPTenterprise",
    version="1.0-b1",
    description="Emulating an enterprise with OpenaAI GPT.",
    author="nervousapps (Achille Pénet)",
    author_email="achille.penet@icloud.com",
    url="https://github.com/nervousapps/GPTenterprise",
    packages=find_packages(),
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "./prompts/*/*.txt"],
    },
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "GPTenterprise = gpt_enterprise:main",
        ],
    },
    python_requires=">= 3.9",
)
