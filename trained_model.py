from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the trained model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('/path/to/save/trained_model')
model = GPT2LMHeadModel.from_pretrained('/path/to/save/trained_model')

# Function to generate text
def generate_text(prompt):
    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = model.generate(inputs.input_ids, max_length=500, num_return_sequences=1)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Example usage
prompt = "Your custom prompt here"
print(generate_text(prompt))