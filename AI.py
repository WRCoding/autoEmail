import json

from openai import OpenAI


def ai_summary(user_input):
    client = OpenAI(api_key='')
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "你是一名AI助手，根据用户输入的项目名称进行总结，只能从餐饮，交通，其他三个词中，选出一个词来总结该项目名称属于哪种类型。只需要返回类型即可，不需要其他内容。结果输出为JSON:{'type':'xxx'}"},
            {"role": "user", "content": user_input},
        ]
    )
    return json.loads(response.choices[0].message.content)['type']
