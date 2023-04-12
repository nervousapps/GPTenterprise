# GPTenterprise :zzz: :robot:

[![python](https://img.shields.io/badge/Python-3.7-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)



First try on making an enterprise with OpenaAI GPT.

This is basically python utilities to connect to OpenaAI API and generate content with variety of system prompts to tell GPT what employee to be :brain:.

## :pinched_fingers: Requirements

- Python 3.7 or newer

- A python venv is recommended, to create one, in your terminal, dive into the repo directory and do:
```bash
python3.x -m venv gptenterprise
```
And enable it
```bash
source ./gptenterprise/bin/activate
```
- Install dependencies by executing:
```bash
pip install -r python/requirements.txt
```

- Text file called openai_key.txt with your opanai key.
```bash
nano python/gpt_enterprise/openai_key.txt
```



## :point_right: Quickstart

To see an example of what can be done with the idea of GPTenterprise, let use the webgpt.py

WebGPT is an AI driven enterprise that develop website for its clients.

It is composed of several GPT employees (prompts):
    
- :writing_hand: a subject prompter, that is responsible of formulating subjects.

- :camera_flash: a dall-e prompter, that is responsible of generating prompts to inject to dall-e for generatig images on the previously generated sibject.

- :desktop_computer: a web developer, that is responsible coding the website on previously generated subject and images.

- :superhero_man: a CEO (you), that is responsible of driving all of this and run the enterprise.

To run the enterprise please do:
```bash
python ./python/gpt_enterprise/webgpt.py
```
