import os
import json
from datasets import Dataset, DatasetDict
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel, Seq2SeqTrainer, Seq2SeqTrainingArguments
import torch

# ================================
# 1. Caricare dataset in HuggingFace
# ================================

def load_dataset_from_folder(folder):
    data = []
    for file in os.listdir(folder):
        if file.endswith(".json"):
            json_path = os.path.join(folder, file)
            img_path = json_path.replace(".json", ".png")
            if not os.path.exists(img_path):
                continue

            with open(json_path, "r", encoding="utf-8") as f:
                label = json.load(f)

            data.append({
                "image": img_path,
                "text": json.dumps(label, ensure_ascii=False)  # target come stringa JSON
            })
    return data

dataset = load_dataset_from_folder("dataset")
hf_dataset = Dataset.from_list(dataset)

# Split train/test
hf_dataset = hf_dataset.train_test_split(test_size=0.1)
dataset = DatasetDict({
    "train": hf_dataset["train"],
    "test": hf_dataset["test"]
})

print(dataset)

# ================================
# 2. Preprocessore e modello Donut
# ================================

model_name = "naver-clova-ix/donut-base"  # puoi usare anche "donut-small" per test veloce
processor = DonutProcessor.from_pretrained(model_name)
model = VisionEncoderDecoderModel.from_pretrained(model_name)

# Forzare output decoder a massimo 512 token
model.config.decoder.max_length = 512
model.config.pad_token_id = processor.tokenizer.pad_token_id
model.config.decoder_start_token_id = processor.tokenizer.convert_tokens_to_ids(["<s>"])[0]

# ================================
# 3. Funzione di preprocessing
# ================================

def preprocess_examples(example):
    # Caricare immagine
    image = Image.open(example["image"]).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values.squeeze()

    # Tokenizzare il target (JSON come stringa)
    text = example["text"]
    tokenized = processor.tokenizer(
        text,
        max_length=512,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    labels = tokenized.input_ids.squeeze()
    labels[labels == processor.tokenizer.pad_token_id] = -100  # ignora pad nella loss

    return {
        "pixel_values": pixel_values,
        "labels": labels
    }

processed_dataset = dataset.map(preprocess_examples, remove_columns=dataset["train"].column_names)

# ================================
# 4. Addestramento
# ================================

training_args = Seq2SeqTrainingArguments(
    output_dir="./donut-finetuned",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    evaluation_strategy="steps",
    num_train_epochs=5,
    save_steps=500,
    save_total_limit=2,
    logging_steps=50,
    predict_with_generate=True,
    fp16=torch.cuda.is_available(),
    learning_rate=5e-5,
    report_to="none"
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=processed_dataset["train"],
    eval_dataset=processed_dataset["test"],
    tokenizer=processor.tokenizer
)

trainer.train()

# ================================
# 5. Salvataggio modello + processor
# ================================

trainer.save_model("./donut-finetuned")
processor.save_pretrained("./donut-finetuned")
