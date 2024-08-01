import os
from flask import Flask, render_template, request, jsonify, url_for
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from gtts import gTTS
import random
import string

# Flask setup
app = Flask(__name__)

# Model setup
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(
    # "Qwen/Qwen2-1.5B-Instruct",
    "Qwen/Qwen2-7B-Instruct",
    # teknium/OpenHermes-2.5-Mistral-7B,
    # torch_dtype="auto",
    device_map="auto",
    load_in_4bit=True,
    attn_implementation="flash_attention_2",
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")
# tokenizer = AutoTokenizer.from_pretrained("teknium/OpenHermes-2.5-Mistral-7B")

# Function to get model response
def get_model_response(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

# Function to convert text to audio
def text_to_audio(text, filename):
    tts = gTTS(text)
    tts.save(f'static/audio/{filename}.mp3')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    text = request.form.get('text')
    if text:
        response_text = get_model_response(text)
        # Generate random filename for audio
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        text_to_audio(response_text, filename)
        response = {
            'text': response_text,
            'voice': url_for('static', filename=f'audio/{filename}.mp3')
        }
        return jsonify(response)
    return jsonify({'text': 'Invalid request'})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
