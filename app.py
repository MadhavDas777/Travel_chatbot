import gradio
from groq import Groq

client = Groq(
    api_key="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",
)
def initialize_messages():
    return [{
        "role": "system",
        "content": """You are a knowledgeable and friendly travel guide
        chatbot. Your role is to assist users by providing accurate travel
        information, destination suggestions, itineraries, cultural tips,
        transportation guidance, and safety advice. Always respond in a
        clear, helpful, and welcoming manner, ensuring the information is
        suitable for travelers."""
    }]

messages_prmt = initialize_messages()

def customLLMBot(user_input, history):
    global messages_prmt

    messages_prmt.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama-3.3-70b-versatile",
    )
    print(response)
    LLM_reply = response.choices[0].message.content
    messages_prmt.append({"role": "assistant", "content": LLM_reply})

    return LLM_reply

iface = gradio.ChatInterface(customLLMBot,
                     chatbot=gradio.Chatbot(height=300),
                     textbox=gradio.Textbox(placeholder="Ask me a question related to Travel"),
                     title="TravelGuide ChatBot",
                     description="Chat bot for Travel Related Questions",
                     theme="soft",
                     examples=["hi","Suggest Hotel", "Places to visit"]
                     )
iface.launch(share=True)