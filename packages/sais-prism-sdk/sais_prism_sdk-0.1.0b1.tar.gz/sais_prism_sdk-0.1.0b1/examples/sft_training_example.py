from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset
import torch
from sais_prism.core.service_locator import ServiceLocator
from sais_prism.core.decorators import sais_foundation
from sais_prism.core.config import config


@sais_foundation
class SFTTraining:
    def __init__(self) -> None:
        self.ml = ServiceLocator.get_ml_manager()
        self.ml_config = config.ml
        # Check if MPS is available
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        print(f"Using device: {self.device}")

    def run(self):
        # 1. Load model and tokenizer (enforce FP32 mode)
        tokenizer = AutoTokenizer.from_pretrained(
            self.ml_config.parameters.base_model)
        tokenizer.pad_token = tokenizer.eos_token

        print(f"Loading model from {self.ml_config.parameters.base_model}...")
        
        # Optional: Perform a warmup step to initialize MPS cache
        if self.device.type == "mps":
            print("Performing MPS warmup...")
            dummy_input = torch.zeros(1, 1, device=self.device)
            dummy_output = dummy_input * 2
            del dummy_input, dummy_output
            torch.mps.synchronize()  # Ensure MPS operations are complete

        model = AutoModelForCausalLM.from_pretrained(
            self.ml_config.parameters.base_model,
            device_map="auto" if self.device.type != "mps" else None,  # Don't use device_map with MPS
            low_cpu_mem_usage=True,
            torch_dtype=torch.float32,  # FP32 mode
        )
        
        # Move model to MPS device if using MPS
        if self.device.type == "mps":
            model = model.to(self.device)
            
        print(f"Model loaded successfully, using {torch.cuda.device_count() if torch.cuda.is_available() else 1} devices")

        # 2. Load dataset and preprocess
        print("Loading and preprocessing dataset...")
        dataset = load_dataset(
            "json",
            data_files=config.unified_data_access.data_access.dataset_names[0],
            split="train"
        )

        def preprocess_function(examples):
            inputs = [
                f"{instruction}\n{input}\nAssistant: " if input else f"{instruction}\nAssistant: "
                for instruction, input in zip(examples["instruction"], examples["input"])
            ]
            full_texts = [
                inp + out + tokenizer.eos_token
                for inp, out in zip(inputs, examples["output"])
            ]
            tokenized = tokenizer(
                full_texts,
                truncation=True,
                padding="max_length",
                max_length=512,  # Increased for M3 Max with 36GB memory
                return_tensors="pt",
            )
            tokenized["labels"] = tokenized["input_ids"].clone()
            return tokenized

        tokenized_datasets = dataset.map(
            preprocess_function,
            batched=True,
            num_proc=8,  # Increased for M3 Max (more CPU cores)
            remove_columns=dataset.column_names,
        )
        print(f"Dataset processed: {len(tokenized_datasets)} examples")

        # 3. Configure training parameters (optimized for M3 Max with 36GB)
        batch_size = 8  # Increased for high-memory system
        print(f"Configuring training with batch size: {batch_size}")
        
        training_args = TrainingArguments(
            output_dir=self.ml_config.parameters.output_dir,
            num_train_epochs=self.ml_config.parameters.num_train_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=self.ml_config.parameters.gradient_accumulation_steps,
            learning_rate=1e-5,  # Conservative learning rate
            weight_decay=self.ml_config.parameters.weight_decay,
            warmup_steps=self.ml_config.parameters.warmup_steps,
            save_total_limit=self.ml_config.parameters.save_total_limit,
            logging_dir=self.ml_config.parameters.logging_dir,
            logging_steps=self.ml_config.parameters.logging_steps,
            save_strategy=self.ml_config.parameters.save_strategy,
            evaluation_strategy=self.ml_config.parameters.evaluation_strategy,
            report_to=self.ml_config.parameters.report_to,
            optim=self.ml_config.parameters.optim,
            gradient_checkpointing=self.ml_config.parameters.gradient_checkpointing,
            max_grad_norm=1.0,  # Gradient clipping
            fp16=False,  # Disable FP16
            no_cuda=True if self.device.type == "mps" else False,  # Disable CUDA when using MPS
        )

        # 4. Re-initialize Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_datasets,
            data_collator=DataCollatorForLanguageModeling(
                tokenizer, mlm=False),
            callbacks=[self.ml],
        )

        # 5. Train and save
        print("Starting training...")
        trainer.train()
        print("Training complete")
        
        output_dir = "./fine_tuned_model"
        print(f"Saving model to {output_dir}")
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        
        # Save model metadata according to project requirements
        with open(f"{output_dir}/metadata.txt", "w") as f:
            f.write(f"model_framework: transformers\n")
            f.write(f"task_type: causal_lm\n")
            f.write(f"base_model: {self.ml_config.parameters.base_model}\n")
            f.write(f"training_device: {self.device.type}\n")
            
        print(f"Model saved successfully to {output_dir}")
        print("Done")


if __name__ == "__main__":
    sft = SFTTraining()
    sft.run()
