<h1 align="center">
:office: GPTenterprise :zzz: :robot:
</h1>
<h1 align="center">
<img width="200" src="https://raw.githubusercontent.com/nervousapps/GPTenterprise/master/logo.png" alt="GPTenterprise">
</h1>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.7-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![openai](https://img.shields.io/badge/openai%20-GPT-yellowgreen)](https://www.openai.com)

[![Pylint](https://github.com/nervousapps/GPTenterprise/actions/workflows/pylint.yaml/badge.svg)](https://github.com/nervousapps/GPTenterprise/actions/workflows/pylint.yaml)
[![Pytest](https://github.com/nervousapps/GPTenterprise/actions/workflows/tests.yaml/badge.svg)](https://github.com/nervousapps/GPTenterprise/actions/workflows/tests.yaml)
[![Docs](https://github.com/nervousapps/GPTenterprise/actions/workflows/pdoc.yaml/badge.svg)](https://nervousapps.github.io/GPTenterprise/gpt_enterprise)

First try on emulating an enterprise with OpenaAI GPT.

This is basically a python package emulating an enterprise. It requests OpenaAI API and generate a sequence of tasks each associated to an employee. Employees are automatically generated (system prompts to tell GPT what employee to be) :brain:.

## :night_with_stars: Summary
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [:artificial_satellite: About the enterprise (by GPT)](#artificial_satellite-about-the-enterprise-by-gpt)
- [:pinched_fingers: Requirements](#pinched_fingers-requirements)
- [:surfing_woman: Installation](#surfing_woman-installation)
- [:unicorn: OpenAI key configuration](#unicorn-openai-key-configuration)
- [:point_right: Quickstart v1](#point_right-quickstart-v1)
- [:books: Documentation](#books-documentation)
  - [General functioning](#general-functioning)
  - [Managers prompt and object structure](#managers-prompt-and-object-structure)
  - [CEO guidelines](#ceo-guidelines)
  - [:label: Environement variables (config file)](#label-environement-variables-config-file)
- [:roller_coaster: Going further](#roller_coaster-going-further)
- [:white_check_mark: Tests](#white_check_mark-tests)
- [:recycle: Formatter](#recycle-formatter)
- [:raccoon: Miscelleneous](#raccoon-miscelleneous)
  - [:older_woman: Quickstart POC](#older_woman-quickstart-poc)
- [:carousel_horse: Disclaimers](#carousel_horse-disclaimers)
- [:ledger: License](#ledger-license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## :artificial_satellite: About the enterprise (by GPT)
<p>Our innovative company uses advanced artificial intelligence technology to bring products and services to the next level. Our employees are AI instances created with the powerful GPT language model that can perform various roles like engineers, designers, and even marketers. This enables us to develop products faster and more efficiently than traditional companies while also providing a unique experience for our customers.</p>
		
		
<p>Our AI employees are equipped with the latest technology and are constantly learning and adapting to new situations. This allows us to be more agile and responsive to market changes, ensuring that our products and services are always at the forefront of innovation.</p>
		
<p>If you're interested in experiencing the future of AI technology, check out our product.</p>

<p>Disclaimer: Our AI employees are not intended to replace human workers and are designed to be used as a supplement to human teams. We believe in the power of human creativity and intelligence when combined with advanced technology.</p>

## :pinched_fingers: Requirements

- Python 3.9 or newer (needs of [asyncio.to_thread()](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread))

- [Open API key](https://platform.openai.com/account/api-keys)

## :surfing_woman: Installation
1 - Clone this repository
```bash
git clone https://github.com/nervousapps/GPTenterprise.git
```

2 - Go in the repo directory
```bash
cd GPTenterprise
```

3 - A python venv is recommended, to create one, in your terminal:
```bash
python3 -m venv gptenterprise
```
And enable it
```bash
source ./gptenterprise/bin/activate
```

4 - Install GPTenterprise package and dependencies by executing:
```bash
pip install ./python
```

## :unicorn: OpenAI key configuration
- Fill openai_key.txt.template with your opanai key and rename it to openai_key.txt. Or create a new one using:
```bash
nano ./openai_key.txt
```


## :point_right: Quickstart v1
To see an example of what can be done with the idea of GPTenterprise : 

1 - Tweek config file in order to give :superhero_man: CEO guidelines (and other parameters if you want but default one should be ok)

```bash
nano ./config
```

2 - Run the enterprise

```bash
GPTenterprise ./config
```

Then the enterprise will be created with your guidelines, a team leader and scrum master will be hired. They will do his best to achieve guidelines.

## :books: Documentation

[HTML documentation here](https://nervousapps.github.io/GPTenterprise/gpt_enterprise).

Documentation generated with [PDOC](https://pdoc.dev/)

### General functioning
An enterprise is composed of a team leader, a scrum master, and  several employees.
At the beginning, the CEO will create the enterprise giving his guidelines to team leader and scrum master.
Each employee will be hired by the team leader for their skills. An employee is defined as a system prompt, automatically generated by the team leader, that describe his skills.
The scrum master will then create a sequence of tasks, each associated to an employee previously hired by the team leader.

### Managers prompt and object structure
:warning:Managers prompts (team leader and scrum master) defines the object structure for employees and tasks. These structures must not be changed as they are used in the code.

:red_haired_woman: Employee structure
```python
{
    "name": "Employee's name",
    "role_name": "Employee's role name",
    "role": "Employee's role (system prompt)"
    "creativity": 1.0
    "emoji": "Emoji code"
}
```
Name and role_name must be unique.

:bookmark: Task structure
```python
{
    "task_name": "The task name"
    "employee_name": "The assigned amployee name"
    "todo": "The work description that has to be done"
    "type": "The type of the task (text or image)"
    "requirements": "The index of the required task or no if no task result is required"
}
```
At each task, the scrum master will add a result field with the employee's work.

:newspaper_roll: Production structure
```python
{
    "employees": [employee1, employee2],
    "tasks": [task1, task2],
    "ceo_guidelines":
    "final_product":
}
```
A field "ceo_guidelines" will be added automatically when creating the enterprise.
The final product can be found in the final_product field of the json object contained in "production_<company_name>.json" file in the specified output directory.

### CEO guidelines
CEO guidelines must be precise and describe the company and the final product wanted.
Number of images to generate can be specified if guidelines, if not, it will be a random number (max 5).
Guidelines must have "PRODUCT" word at the end, followed by the description of the desired final product.
An example can be given with the keyword "EXAMPLE:", it will be added to employees tasks.


### :label: Environement variables (config file)
| env name                       | description     | default value      |
| -------------------------------| ----------------| -------------------|
| COMPANY_NAME                   | Enterprise name                                                       | GPTenterprise   | 
| KEYFILE                        | Path to openai keyfile.txt                                            | ./openai_key.txt|
| OUTPUT_DIRECTORY               | Output directory                                                      | ./generated/v2  |
| MANAGER_RETRY                  | How many times managers will retry to do the plans if failing          | 1               |
| CUSTOM_MANAGER_PROMPTS_PATH    | Give a custom managers prompt (be careful to keep objects structure definitions) | ""              |
| CEO_GUIDELINES                 | "As a CEO, I want ... PRODUCT ... "                                         | Default guidelines |
| INTERACTIVE                    | Wait for user entry (basic for now), no employee interaction if asynchronous mode is activated                                        | "no" |
| ASYNCHRONOUS                    | Asynchronous mode, employees can work in parallel                                        | "yes" |

## :roller_coaster: Going further
- rework managers prompt :curly_loop:
- enhanced employees interactions
- asynchronous operations :heavy_check_mark:
- multi managers enterprise
- keep previous responses in memory (maybe use https://github.com/acheong08/ChatGPT)
- internet search (python only to avoid using openAI's token)
- use https://python.langchain.com/en/latest/index.html to simplify code

## :white_check_mark: Tests
1 - Install tests requirements
```bash
pip install -r ./python/requirements-tests.txt
```

2 - Run tests
```bash
pytest
```

## :recycle: Formatter

[BLACK](https://pypi.org/project/black/)


## :raccoon: Miscelleneous
### :older_woman: Quickstart POC

To see an example of what can be done with the idea of GPTenterprise, let use the webgpt.py

WebGPT is an AI driven enterprise that develop website for its clients.

It is composed of several GPT employees (prompts):
    
- :writing_hand: a subject prompter, that is responsible of formulating subjects.

- :camera_flash: a dall-e prompter, that is responsible of generating prompts to inject to dall-e for generating images on the previously generated sibject.

- :desktop_computer: a web developer, that is responsible of coding the website on previously generated subject and images.

- :superhero_man: a CEO (you), that is responsible of driving all of this and run the enterprise.

To run the enterprise please do:
```bash
python ./examples/webgpt.py
```

## :carousel_horse: Disclaimers
This is not an official OpenAI product. This is a personal project and it is not affiliated with OpenAI in any way.

## :ledger: License
[License MIT](./LICENSE)
