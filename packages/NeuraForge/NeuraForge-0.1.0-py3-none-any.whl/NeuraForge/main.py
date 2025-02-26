import google.generativeai as genai

def Api(API_key):
    genai.configure(api_key=API_key)
    return API_key

def Model(model = "gemini-1.5-pro", temperature = 1, top_p = 0.95, top_k = 40, max_output_tokens = 8192):
    generation_config = {
    "temperature": temperature,
    "top_p": top_p,
    "top_k": top_k,
    "max_output_tokens": max_output_tokens,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config,
    )
    return model


def Chat(model):
    chat_session = model.start_chat(
        history=[
        ]
    )
    return chat_session
def Send(chat_name, message):
    response = chat_name.send_message(message)
    return response.text



