import json

from openai import OpenAI

import system_prompt

client = OpenAI(api_key='')


def ai_summary(user_input):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
             "content": "你是一名AI助手，根据用户输入的项目名称进行总结，只能从餐饮，交通，其他三个词中，选出一个词来总结该项目名称属于哪种类型。只需要返回类型即可，不需要其他内容。结果输出为JSON:{'type':'xxx'}"},
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
    print(result['text'])
    return result['text']
