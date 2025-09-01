import os
import json
import torch
from torch.utils.data import Dataset
from transformers import DonutProcessor, VisionEncoderDecoderModel, Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import load_dataset

# ==============================
# 1. CONFIGURAZIONE
# ==============================
MODEL_NAME = "naver-clova-ix/donut-base"  # modello pre-addestrato
OUTPUT_DIR = "./donut-id-trained"
MAX_LENGTH = 512
BATCH_SIZE = 2
EPOCHS = 20
LR = 5e-5

# ==============================
# 2. PREPARAZIONE DATASET
# ==============================
class IDDataset(Dataset):
    def __init__(self, root_dir, processor, max_length=MAX_LENGTH):
        self.root_dir = root_dir
        self.processor = processor
        self.max_length = max_length
        self.samples = []

        for split in ["train", "val"]:
            folder = os.path.join(root_dir, split)
            ann_file = os.path.join(folder, "labels.json")
            with open(ann_file, "r", encoding="utf-8") as f:
                ann_data = json.load(f)
            for item in ann_data:
                self.samples.append({
                    "image_path": os.path.join(folder, item["file_name"]),
                    "label": item["ground_truth"]
                })

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        image = self.processor.image_processor(Image.open(sample["image_path"]).convert("RGB"), return_tensors="pt")
        pixel_values = image["pixel_values"][0]

        # Encode testo target come JSON
        input_ids = self.processor.tokenizer(
            sample["label"],
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        ).input_ids[0]

        return {
            "pixel_values": pixel_values,
            "labels": input_ids,
        }

# ==============================
# 3. CARICAMENTO PROCESSOR E MODELLO
# ==============================
processor = DonutProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

# Imposta token EOS
model.config.decoder_start_token_id = processor.tokenizer.convert_tokens_to_ids(["<s>"])[0]
model.config.pad_token_id = processor.tokenizer.pad_token_id
model.config.eos_token_id = processor.tokenizer.eos_token_id

# ==============================
# 4. CARICAMENTO DATI
# ==============================
train_dataset = IDDataset("./dataset", processor)

# Split semplice (70/30)
train_size = int(0.7 * len(train_dataset))
val_size = len(train_dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(train_dataset, [train_size, val_size])

# ==============================
# 5. TRAINING
# ==============================
training_args = Seq2SeqTrainingArguments(
    predict_with_generate=True,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=LR,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    weight_decay=0.01,
    save_total_limit=2,
    output_dir=OUTPUT_DIR,
    logging_dir=f"{OUTPUT_DIR}/logs",
    logging_strategy="steps",
    logging_steps=50,
    push_to_hub=False,
)

def collate_fn(batch):
    pixel_values = torch.stack([item["pixel_values"] for item in batch])
    labels = torch.stack([item["labels"] for item in batch])
    return {"pixel_values": pixel_values, "labels": labels}

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=processor.tokenizer,
    data_collator=collate_fn,
)

trainer.train()

# ==============================
# 6. SALVATAGGIO MODELLO
# ==============================
model.save_pretrained(OUTPUT_DIR)
processor.save_pretrained(OUTPUT_DIR)

print("✅ Addestramento completato. Modello salvato in:", OUTPUT_DIR)
