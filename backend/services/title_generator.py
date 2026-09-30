import re


def generate_title(question: str) -> str:

    question = question.strip()


    replacements = {
        "what are the main steps of": "",
        "what is": "",
        "how to": "",
        "how do i": "",
        "how can i": "",
        "explain": "",
        "describe": "",
    }


    title = question.lower()


    for key, value in replacements.items():
        title = title.replace(key, value)



    title = title.replace(
        "the recruitment process",
        "Recruitment Process"
    )


    title = title.replace(
        "recruitment process",
        "Recruitment Process"
    )


    title = re.sub(
        r"[^a-zA-Z0-9 ]",
        "",
        title
    )


    title = title.strip()


    if len(title) > 50:
        title = title[:50]


    if not title:
        title = "New Conversation"


    return title.title()