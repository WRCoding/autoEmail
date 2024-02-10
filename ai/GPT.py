import json
from openai import OpenAI
import system_prompt
from ai.AI import AbsAI
from ai.AIRegister import register_ai

@register_ai('GPT')
class GPT(AbsAI):

    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key='')

    @register_ai('GPT')
    def ai_summary(self, user_input):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt.summary_prompt},
                {"role": "user", "content": user_input},
            ]
        )
        return json.loads(response.choices[0].message.content)['type']

    def find_text(self, user_input):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt.find_text_prompt},
                {"role": "user", "content": user_input},
            ]
        )
        result = json.loads(response.choices[0].message.content)
        print(result['text'])
        return result['text']
