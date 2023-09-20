from threading import Event

import gradio as gr

from MeowTarot.Chat import ChatTarot
from MeowTarot.Tarot import TarotDeck


class MeowTarotApp:
    def __init__(self):
        css = ReadText("Data/Style.css")
        font = [gr.themes.GoogleFont("Noto Sans Mono")]
        theme = gr.themes.Soft(font=font)

        with gr.Blocks(css=css, theme=theme, title="薯條塔羅") as self.app:
            self.stop_event = gr.State(None)
            self.resp = gr.State("")
            self.deck = gr.State(TarotDeck())
            self.chat_tarot = gr.State(ChatTarot())
            gr.Markdown("# 🐱 薯條貓貓塔羅", elem_id="title")
            with gr.Row():
                with gr.Column():
                    self.InitLeftColumn()

                with gr.Column():
                    self.InitRightColumn()

            self.RegisterEvents()

    def Launch(self):
        self.app.queue().launch(favicon_path="Data/RoundCat.png")

    def InitLeftColumn(self):
        with gr.Box():
            self.welcome = [[None, "有什麼事情要問本喵呢？"]]
            self.chat = gr.Chatbot(label="薯條貓貓占卜大師", value=self.welcome, height=600)
            self.msg = gr.Textbox(label="問題", placeholder="喵喵喵，讓本喵來幫你解答心中的疑惑！")
            with gr.Row():
                self.send = gr.Button("🌙  抽牌")
                self.clear = gr.Button("🗑️  清除")
                self.stop = gr.Button("🛑 停止")
            with gr.Accordion("完整提示", open=False) as self.fold:
                self.debug_msg = gr.TextArea(show_label=False, lines=14)

    def InitRightColumn(self):
        with gr.Box():
            self.tarot_name = gr.Textbox(label="塔羅牌名稱")
            self.image = gr.Image(label="塔羅牌", interactive=False, height=400)
            self.info = gr.TextArea(label="塔羅牌資訊", lines=1)

    def RegisterEvents(self):
        inn_send = [self.msg, self.chat, self.deck, self.chat_tarot]
        out_send = [
            self.msg,
            self.chat,
            self.image,
            self.info,
            self.tarot_name,
            self.resp,
            self.debug_msg,
            self.stop_event,
        ]
        arg_send = {
            "fn": self.SendMessage,
            "inputs": inn_send,
            "outputs": out_send,
        }

        inn_show = [self.chat, self.resp, self.chat_tarot, self.stop_event]
        out_show = [self.chat]
        arg_show = {
            "fn": self.ShowResponse,
            "inputs": inn_show,
            "outputs": out_show,
        }

        self.msg.submit(self.SendMessage, inn_send, out_send).then(**arg_show)
        self.send.click(**arg_send).then(**arg_show)

        out_clear = [self.chat, self.tarot_name, self.image, self.info]
        self.clear.click(self.Clear, None, out_clear)
        self.stop.click(self.TriggerStop, self.stop_event, queue=False)

    def SendMessage(self, msg, chat: list, deck: TarotDeck, tarot: ChatTarot):
        tarot_path, tarot_data, tarot_name = deck.Pick()
        tarot_info = tarot_data["related"]
        chat.append([msg, None])
        sys_prompt, user_prompt = tarot.BuildPrompt(msg, tarot_name, tarot_info)
        resp = tarot.Chat(user_prompt)

        prompt = f"System: {sys_prompt}\n\nUser: {user_prompt}"
        return None, chat, tarot_path, tarot_info, tarot_name, resp, prompt, Event()

    def ShowResponse(self, history: list, resp, tarot: ChatTarot, stop_event: Event):
        history[-1][1] = ""
        for r in resp:
            history[-1][1] = r
            yield history

            if stop_event.is_set():
                tarot.Stop()
                break

    def Clear(self):
        return self.welcome, None, None, None

    def TriggerStop(self, stop_event):
        if isinstance(stop_event, Event):
            stop_event.set()


def ReadText(fp: str) -> str:
    with open(fp, "rt", encoding="UTF-8") as f:
        return f.read()
