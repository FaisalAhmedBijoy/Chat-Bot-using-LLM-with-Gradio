from transformers import AutoModelForCausalLM, AutoTokenizer

# Specify the model name
model_name = "Qwen/Qwen2-7B-Instruct"

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the model and tokenizer locally
model.save_pretrained("models/Qwen2-7B-Instruct")
tokenizer.save_pretrained("models/Qwen2-7B-Instruct")

print("Model and tokenizer downloaded and saved locally.")
