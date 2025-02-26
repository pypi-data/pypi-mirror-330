import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

# Check for MPS availability
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using MPS device (Apple Silicon GPU)")
else:
    device = torch.device("cpu")
    print("MPS not available, using CPU instead")

# Path to your fine-tuned model
model_path = "./fine_tuned_model"
print(f"Loading model from {model_path}...")

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token  # Ensure padding token is set

# Optional: Perform a warmup step to initialize MPS cache
if device.type == "mps":
    print("Performing MPS warmup...")
    dummy_input = torch.zeros(1, 1, device=device)
    dummy_output = dummy_input * 2
    del dummy_input, dummy_output
    torch.mps.synchronize()  # Ensure MPS operations are complete

# Load the model with appropriate device mapping
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto" if device.type != "mps" else None,  # Don't use device_map with MPS
    torch_dtype=torch.float32,  
)

# Move model to device if using MPS
if device.type == "mps":
    model = model.to(device)
    
print(f"Model loaded successfully on {device}")

# Define the input question
question = "What are the different classification types associated with the investigational drug AR-12?"

# Function to generate responses
def generate_response(prompt, max_tokens=200):
    print(f"\nGenerating response for: {prompt}")
    
    # Tokenize the input prompt
    inputs = tokenizer(
        prompt,
        return_tensors="pt",  
        padding=True,
        truncation=True,
        max_length=512,  # Increased for M3 Max
    )

    # Move inputs to the appropriate device
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Generate the response and measure time
    start_time = time.time()
    try:
        with torch.no_grad():  # Disable gradient computation for inference
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.1,
            )

        # Calculate generation time
        gen_time = time.time() - start_time
        tokens_generated = outputs.shape[1] - inputs["input_ids"].shape[1]
        tokens_per_second = tokens_generated / gen_time
        
        # Decode the generated tokens to text
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Print performance stats
        print(f"Generated {tokens_generated} tokens in {gen_time:.2f}s ({tokens_per_second:.2f} tokens/sec)")
        return response
        
    except Exception as e:
        print(f"Error during model inference: {e}")
        print("If you're seeing MPS-related errors, try running with CPU by modifying the script to use device='cpu'")
        return None

# Test with the original question
response = generate_response(question)
if response:
    print("\n----- RESULT -----")
    print("Question:", question)
    print("Response:", response)
    print("------------------\n")

# Optional: Test with additional questions
additional_questions = [
    "What is the mechanism of action for AR-12?",
    "Describe the key clinical trials for AR-12."
]

for q in additional_questions:
    response = generate_response(q)
    if response:
        print("\n----- RESULT -----")
        print("Question:", q)
        print("Response:", response)
        print("------------------\n")
