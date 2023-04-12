"""
WebGPT is an AI driven enterprise that develop website for its clients.
"""
import os

from gpt_utils import (
    generate_text,
    generate_image,
    PROMPTS_PATH,
    OUTPUT_PATH
)


def main():
    # Enterprise creativity
    temperature = 0.9

    # Tell subject prompter to generate a random subject
    print("\n \U0001F9B8  Hey Cartman, give me a subject for yesturday please.")
    with open(os.path.join(PROMPTS_PATH, "subject_prompter.txt")) as file:
        random_subject = generate_text(
            # Split # in case of  comments after the prompt
            system_prompt=file.read().split("#")[0],
            user_prompt="Give me a subject.",
            temperature=temperature)
    print("\n\t\t\t\t \N{writing hand}", f"Hey I have a subject, {random_subject} !")

    # Tell dall-e prompter to generate images for the given subject
    print("\n \U0001F9B8 Bernard, can you generate some images for this subject?")
    generated_prompt, generated_image_names = generate_image(
        base_name=random_subject,
        prompt=f"{random_subject} photographed",
        nb_image=1)
    print("\n\t\t\t\t \N{camera with flash}", f"Okay so I have generated imaged with the following prompt: \n\n {generated_prompt}")

    # Tell the web developer to generate website on the random subject with generated images path
    print("\n \U0001F9B8  Gerald, I need the website to be ready for a demo in 5 minutes, if not done, you are fired...")
    with open(os.path.join(PROMPTS_PATH, "web_developer.txt")) as file:
        website_html = generate_text(
            system_prompt=file.read(),
            user_prompt=f"SUBJECT {random_subject}. IMAGES {generated_image_names}",
            temperature=temperature)

    # Write the code into a file
    with open(os.path.join(OUTPUT_PATH, f"test_article_{random_subject}.html"), "w") as file:
        file.write(website_html)

    print("\n\t\t\t\t \N{desktop computer}", "Done ! See you on the dancefloor Patrick !\n")

if __name__ == "__main__":
    main()