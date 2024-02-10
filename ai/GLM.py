from zhipuai import ZhipuAI

import system_prompt
from ai.AI import AbsAI
from ai.AIRegister import register_ai


@register_ai('GLM')
class GLM(AbsAI):

    def __init__(self):
        super().__init__()
        self.client = ZhipuAI(api_key="")

    def ai_summary(self, user_input):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "system", "content": system_prompt.summary_prompt},
                {"role": "user", "content": user_input},
            ]
        )
        print(response.choices[0].message)

    def find_text(self, user_input):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "system", "content": system_prompt.find_text_prompt},
                {"role": "user", "content": user_input},
            ]
        )
        print(response.choices[0].message)



