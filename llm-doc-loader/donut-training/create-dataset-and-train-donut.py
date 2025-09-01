import os
import json
from datasets import load_dataset, Dataset, DatasetDict
from transformers import DonutProcessor, VisionEncoderDecoderModel, Seq2SeqTrainer, Seq2SeqTrainingArguments
import torch
from PIL import Image

# === 1. Preparazione dataset ===
def load_custom_dataset(dataset_dir="dataset"):
    images = []
    labels = []
    for file in os.listdir(dataset_dir):
        if file.endswith(".png"):
            img_path = os.path.join(dataset_dir, file)
            json_path = img_path.replace(".png", ".json")
            if os.path.exists(json_path):
                images.append(img_path)
                with open(json_path, "r", encoding="utf-8") as f:
                    labels.append(json.load(f))
    return Dataset.from_dict({"image_path": images, "label": labels})

dataset = load_custom_dataset("dataset")

# Split train/val
dataset = dataset.train_test_split(test_size=0.1)
dataset = DatasetDict({
    "train": dataset["train"],
    "validation": dataset["test"]
})

# === 2. Caricare Donut pre-addestrato ===
model_id = "naver-clova-ix/donut-base"
processor = DonutProcessor.from_pretrained(model_id)
model = VisionEncoderDecoderModel.from_pretrained(model_id)

# Impostiamo token speciale per "task prompt"
task_prompt = "<s_invoices>"

# === 3. Preprocessing ===
def preprocess(example):
    # Apri immagine
    image = Image.open(example["image_path"]).convert("RGB")

    # Convertila in pixel_values
    pixel_values = processor(image, return_tensors="pt").pixel_values[0]

    # Converti label JSON in stringa
    text = json.dumps(example["label"], ensure_ascii=False)
    text = task_prompt + text + processor.tokenizer.eos_token

    # Tokenizza target
    labels = processor.tokenizer(
        text,
        add_special_tokens=False,
        return_tensors="pt"
    ).input_ids[0]

    return {"pixel_values": pixel_values, "labels": labels}

dataset = dataset.map(preprocess, remove_columns=dataset["train"].column_names)

# === 4. Parametri di addestramento ===
training_args = Seq2SeqTrainingArguments(
    output_dir="./donut_finetuned",
    evaluation_strategy="steps",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    predict_with_generate=True,
    logging_steps=50,
    save_steps=500,
    eval_steps=500,
    warmup_steps=200,
    save_total_limit=2,
    num_train_epochs=5,
    fp16=torch.cuda.is_available(),
    learning_rate=5e-5,
    report_to="none"
)

# Collator
def collate_fn(batch):
    pixel_values = torch.stack([x["pixel_values"] for x in batch])
    labels = [x["labels"] for x in batch]

    labels = torch.nn.utils.rnn.pad_sequence(
        labels,
        batch_first=True,
        padding_value=processor.tokenizer.pad_token_id
    )

    return {"pixel_values": pixel_values, "labels": labels}

# === 5. Trainer ===
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    tokenizer=processor.tokenizer,
    data_collator=collate_fn,
)

# === 6. Avvio training ===
trainer.train()

# === 7. Salva modello ===
trainer.save_model("./donut_finetuned")
processor.save_pretrained("./donut_finetuned")
