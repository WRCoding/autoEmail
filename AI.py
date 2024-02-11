import json

from openai import OpenAI

import system_prompt

client = OpenAI(api_key='')


def ai_summary(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt.summary_prompt},
            {"role": "user", "content": user_input},
        ]
    )
    return json.loads(response.choices[0].message.content)['type']


def find_text(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
             "content": system_prompt.prompt},
            {"role": "user", "content": user_input},
        ]
    )
    result = json.loads(response.choices[0].message.content)
    return result['text']
