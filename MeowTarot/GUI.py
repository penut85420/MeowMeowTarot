from threading import Event

import gradio as gr

from MeowTarot.Chat import TarotChat
from MeowTarot.Tarot import TarotDeck


class MeowTarotApp:
    def __init__(self):
        css = read_text("Data/Style.css")
        font = [gr.themes.GoogleFont("Noto Sans Mono")]
        theme = gr.themes.Soft(font=font)

        with gr.Blocks(css=css, theme=theme, title="薯條塔羅") as self.app:
            self.stop_event = gr.State(None)
            self.resp = gr.State(None)
            self.deck = gr.State(TarotDeck())
            self.chat_tarot = gr.State(TarotChat())
            gr.Markdown("# 🐱 薯條貓貓塔羅")
            with gr.Row():
                with gr.Column():
                    self.init_left_column()

                with gr.Column():
                    self.init_right_column()

            self.init_events()

    def launch(self):
        self.app.queue().launch(favicon_path="Data/RoundCat.png")

    def init_left_column(self):
        self.welcome = [[None, "有什麼事情要問本喵呢？"]]
        self.chat = gr.Chatbot(label="薯條貓貓占卜大師", value=self.welcome, height=500)
        self.msg = gr.Textbox(label="問題", placeholder="喵喵喵，讓本喵來幫你解答心中的疑惑！")
        with gr.Row():
            self.send = gr.Button("🌙 抽牌")
            self.clear = gr.Button("🗑️ 清除")
            self.stop = gr.Button("🛑 停止")

    def init_right_column(self):
        self.image = gr.Image(label="塔羅牌", interactive=False, height=400, elem_id="img-div")
        self.tarot_name = gr.Textbox(label="塔羅牌名稱")
        self.info = gr.TextArea(label="塔羅牌資訊", lines=1)
        with gr.Accordion("完整提示", open=False) as self.fold:
            self.debug_msg = gr.TextArea(show_label=False, lines=14)

    def init_events(self):
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
        arg_send = dict(fn=self.send_message, inputs=inn_send, outputs=out_send)

        inn_show = [self.chat, self.resp, self.chat_tarot, self.stop_event]
        out_show = [self.chat]
        arg_show = dict(fn=self.show_response, inputs=inn_show, outputs=out_show)

        self.msg.submit(self.send_message, inn_send, out_send, show_progress="minimal").then(
            **arg_show, show_progress="minimal"
        )
        self.send.click(**arg_send).then(**arg_show)

        out_clear = [self.chat, self.tarot_name, self.image, self.info]
        self.clear.click(self.clear_message, None, out_clear)
        self.stop.click(self.trigger_stop, self.stop_event, queue=False)

    def send_message(self, msg, chat: list, deck: TarotDeck, tarot: TarotChat):
        tarot_path, tarot_data, tarot_name = deck.pick()
        tarot_info = tarot_data["related"]
        chat.append([msg, None])
        sys_prompt, user_prompt = tarot.build_prompt(msg, tarot_name, tarot_info)
        resp = tarot.chat(user_prompt)

        prompt = f"System: {sys_prompt}\n\nUser: {user_prompt}"
        return None, chat, tarot_path, tarot_info, tarot_name, resp, prompt, Event()

    def show_response(self, history: list, resp, tarot: TarotChat, stop_event: Event):
        history[-1][1] = str()
        for msg in resp:
            history[-1][1] = msg
            yield history

            if stop_event.is_set():
                tarot.stop()
                break

    def clear_message(self):
        return self.welcome, None, None, None

    def trigger_stop(self, stop_event):
        if isinstance(stop_event, Event):
            stop_event.set()


def read_text(file_path: str) -> str:
    with open(file_path, "rt", encoding="UTF-8") as fp:
        return fp.read()
