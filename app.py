import gradio
from groq import Groq
import os
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
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

css = """
.app, body {
    background-color: #087f23 !important;  
    color: white !important;              
}

.gr-chatbot {
    background-color: white !important;    
    border-radius: 12px !important;
}

.gr-textbox textarea {
    background-color: white !important;    
    border-radius: 12px !important;
    
    color: black !important;               
}

.gr-button {
    color: black !important;               
}
"""

iface = gradio.ChatInterface(
    fn=customLLMBot,

    chatbot=gradio.Chatbot(
        type="messages",
        height=450,
        show_copy_button=True,
        avatar_images=(
            "https://img.icons8.com/color/96/airplane-take-off.png",
            "https://img.icons8.com/color/96/robot.png"
        ),
    ),

    textbox=gradio.Textbox(
        placeholder=" Ask me a question related to Travel...",
        show_label=False,
        lines=1,
    ),

    title=" Travel Guide ChatBot",
    #description="Your AI-powered travel companion.",

    examples=[
        "Suggest a budget-friendly hotel",
        "Best places to visit in Kerala",
        "Plan a 3-day trip to Ooty",
        "Best time to visit Manali"
    ],

    theme=gradio.themes.Soft(
        primary_hue="green",
        secondary_hue="lime",
        font=[gradio.themes.GoogleFont("Poppins"), "system-ui"],
    ),

    css=css
)
iface.launch(share=True)
