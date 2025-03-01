import google.generativeai as genai
import PIL.Image
import mimetypes

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
def Send(chat_name, message, path=None):
    if path:
        mime_type, _= mimetypes.guess_type(path)
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        response = chat_name.send_message([message, file]) #if image is None, send without image.
    else:
        response = chat_name.send_message(message)
    return response.text



