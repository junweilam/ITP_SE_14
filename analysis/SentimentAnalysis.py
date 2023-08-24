import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import os

# Initialization of models
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
# Fine-tuned model, Uncomment to run input against respective models
model = AutoModelForSequenceClassification.from_pretrained("retrained_model/checkpoint-500")
# Pre-Trained model, Uncomment to run input against respective models
# model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

# Get Countries folder pathing
root = './data'
countrylist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
print(countrylist)

header = ['Comment', 'Negative', 'Neutral', 'Positive']
for country in countrylist:
    counter = 0
    # Read Cleaned up files
    with open(f'{country}_reviews_pros_cons.csv', newline='', encoding="utf-8") as f:
        # Writing to another file of results of scoring on Negative, Neutral, Positive
        with open(f'{country}_analyse_result_retrained.csv', 'a', encoding="utf-8") as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            writer.writerow(header)
            reader = csv.reader(f)
            alls = []
            for row in reader:
                if row:
                    # Running model against input
                    encoded_tweet = tokenizer(row, return_tensors='pt',truncation=True,max_length=512)
                    output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
                    # Formatting output to probability scores of sentiment
                    scores = output[0][0].detach().numpy()
                    scores = softmax(scores)
                    for score in scores:
                        row.append(score)
                    writer.writerow(row)
                    alls.append(row)
                    print(counter)
                    print(row)

                else:
                    print('emptyfile')
                counter += 1

            print(alls)