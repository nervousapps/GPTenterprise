"""
Module setup
"""
from setuptools import setup, find_packages

requirements = [
    "python-dotenv",
    "openai",
]

setup(name='GPTenterprise',
      version='1.0-b1',
      description='Emulating an enterprise with OpenaAI GPT.',
      author='Achille Pénet',
      author_email='achille.penet@icloud.com',
      url='https://github.com/nervousapps/GPTenterprise',
      packages = find_packages(),  
      package_data = {
            # If any package contains *.txt or *.rst files, include them:
            '': ['*.txt', './managers_prompts/*.txt'],
            '': ['*.txt', './employees_prompts/*.txt'],
      },
      include_package_data=True,
      install_requires=requirements,
      entry_points={
            "console_scripts": [
                  "gpt_enterprise = gpt_enterprise:main",
            ],
      },
      python_requires='>= 3.7',
     )