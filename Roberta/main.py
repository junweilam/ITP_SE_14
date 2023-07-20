import torch
from datasets import load_dataset
from transformers import pipeline
from transformers import RobertaTokenizer, RobertaForMaskedLM, LineByLineTextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

if __name__ == '__main__':
    # This is the try out of using Huggingface official dataset of offensive words to train the model
    # Have not yet experiment on it further, only tried loading the dataset for printing
    dataset = load_dataset(
        'hate_speech_offensive')
    print(dataset['train'][0])

    # This is the start of training by retraining the roberta model, following the article I had given in WA
    # This part is the initialization of roberta model
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    model = RobertaForMaskedLM.from_pretrained('roberta-base')
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=True, mlm_probability=0.15
    )
    # This part is to load the dataset into the tokenizer,
    # tokenizer are to translate text into data that can be processed by the model.
    # Models can only process numbers, so tokenizers need to convert our text inputs to numerical data.
    dataset = LineByLineTextDataset(
        tokenizer=tokenizer,
        file_path="train_text.txt",
        block_size=512,
    )
    # This part is to set the training parameters, not really sure on each parameter meaning,
    # which the article never really explain it.
    training_args = TrainingArguments(
        output_dir="./roberta-retrained",
        overwrite_output_dir=True,
        num_train_epochs=25,
        per_device_train_batch_size=2,
        save_steps=500,
        save_total_limit=2,
        seed=1
    )
    # This part is the initialization of trainer after setting up relative params
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset
    )
    # This part is to start train function and save the model
    torch.cuda.empty_cache()
    trainer.train()

    trainer.save_model("./roberta-retrained")

    # This part is to sample the model, can try change model = "roberta-base" to see difference of pre-trained
    # roberta and the retrained roberta
    fill_mask = pipeline(
        "fill-mask",
        model="./roberta-retrained",
        tokenizer="roberta-base"
    )
    print(fill_mask("YOU ARE SUCH A <mask> "))

