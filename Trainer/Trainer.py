import torch
from pathlib import Path
from sklearn.model_selection import train_test_split
from transformers import Trainer, TrainingArguments
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# Read labelled negative, neutral, positive comments and relabel with 0 1 2 for easy encodings.
def read_training_split(split_dir):
    split_dir = Path(split_dir)
    print(split_dir)
    texts = []
    labels = []
    for label_dir in ["neg", "neu", "pos"]:
        for text_file in (split_dir / label_dir).iterdir():
            texts.append(text_file.read_text(encoding="utf8"))
            if label_dir == "neg":
                labels.append(0)
            elif label_dir == "neu":
                labels.append(1)
            else:
                labels.append(2)

    return texts, labels


train_texts, train_labels = read_training_split('Train')
test_texts, test_labels = read_training_split('Test')

# Set self test size of 70%/30%
train_texts, val_texts, train_labels, val_labels = train_test_split(train_texts, train_labels, test_size=.3)

# Pass Text into tokenizer
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
train_encodings = tokenizer(train_texts, truncation=True, padding=True)
val_encodings = tokenizer(val_texts, truncation=True, padding=True)
test_encodings = tokenizer(test_texts, truncation=True, padding=True)


# Creating Dataset Object
class TrainDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


train_dataset = TrainDataset(train_encodings, train_labels)
val_dataset = TrainDataset(val_encodings, val_labels)
test_dataset = TrainDataset(test_encodings, test_labels)

# Initialization of Trainer and parameters
training_args = TrainingArguments(
    output_dir='./retrained_models',  # output directory
    num_train_epochs=3,  # total number of training epochs
    per_device_train_batch_size=4,  # batch size per device during training
    per_device_eval_batch_size=8,  # batch size for evaluation
    warmup_steps=500,  # number of warmup steps for learning rate scheduler
    weight_decay=0.01,  # strength of weight decay
    logging_dir='./logs',  # directory for storing logs
    logging_steps=10,
)
# Model to be fine-tuned
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

trainer = Trainer(
    model=model,  # the instantiated 🤗 Transformers model to be trained
    args=training_args,  # training arguments, defined above
    train_dataset=train_dataset,  # training dataset
    eval_dataset=val_dataset,  # evaluation dataset
    test_dataset=test_dataset  # test dataset
)

trainer.train()
