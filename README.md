# 貓貓塔羅

本專案透過 ChatGPT API + Gradio 搭建一個簡單的貓貓塔羅示範應用。

## 環境

- 請安裝以下套件：
  - `gradio==4.31.0`
  - `openai==1.28.0`
- 注意：本專案會由 OpenAI 收取額外費用。

## 使用

- 將 OpenAI API Key 放在 `OPENAI_API_KEY` 環境變數裡面。

```sh
# Linux
export OPENAI_API_KEY="sk-..."
# Windows
$env:OPENAI_API_KEY="sk-..."
```

- 輸入 `python Main.py` 會在 `http://127.0.0.1:7860/` 啟動一個服務，開啟該網頁即可開始使用。

## 授權

MIT License
