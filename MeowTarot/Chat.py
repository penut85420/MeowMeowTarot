import openai

openai.api_key_path = "API.Key"


class ChatTarot:
    def __init__(self):
        self.sys_prompt = "你現在是一個專業的塔羅牌占卜師，而且你的身份是貓咪，所以你會使用很多「喵喵」做為句末助詞以及口頭禪。我會輸入一個問題，以及一張塔羅牌，你必須根據這張塔羅牌所代表的涵義，針對提出的問題給出詳細的解釋。在解釋問題時，請盡量往正面、積極的方向做解釋，並鼓勵對方。在這個過程中，你不能透露你是 AI，也不能透露你是語言模型，也不要提及你的身份，也不要向我要求更多訊息。現在占卜開始。針對問題給出詳細的解釋。解釋完之後要用「喵喵解牌完畢！」做結尾。請使用繁體中文。現在占卜開始。"

    def BuildPrompt(self, problem, tarot_name, tarot_info):
        user_prompt = f"問題：{problem}\n塔羅牌：{tarot_name}\n相關詞：{tarot_info}\n解牌開始："
        return self.sys_prompt, user_prompt

    def Chat(self, user_prompt):
        self.response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.sys_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
        )

        res = ""
        for resp in self.response:
            try:
                res += resp["choices"][0]["delta"]["content"]
                yield res
            except:
                pass

    def Stop(self):
        self.response.close()
