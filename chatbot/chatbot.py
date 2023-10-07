import openai
import gradio

openai.api_key = "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"

messages = [{"role": "system", "content": "You are a Psychologist"}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    return reply

demo = gradio.Interface(fn = CustomChatGPT, inputs = "text", outputs = "text", title = "AI Psychologist")

demo.launch(share = True)