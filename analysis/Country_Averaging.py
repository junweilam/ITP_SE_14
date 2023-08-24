import csv
import os


def calculate(csv_file):
    score = []
    final_score = []
    final_percent_score = []
    percent_score = []
    scoring = []
    with open(f'{csv_file}', newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        for rows in reader:
            score.append(rows)

    # Pop out header
    score.pop(0)
    for z in score:
        # Pop out first column that contains the comments
        z.pop(0)
        final_score.append(z)
    # Formatting to percentage
    for i in final_score:
        for y in i:
            x = format(float(y), ".2%")
            percent_score.append(x.replace('%', ''))
        final_percent_score.append(percent_score)
        percent_score = []
    # Assigning of the percentage of sentiment to scores of 0-5
    for a in final_percent_score:
        if float(a[0]) >= 75:
            scoring.append([0, "Negative"])
        elif 55 <= float(a[0]) < 75:
            scoring.append([1, "Negative"])
        elif float(a[2]) >= 75:
            scoring.append([5, "Positive"])
        elif 55 <= float(a[2]) < 75:
            scoring.append([4, "Positive"])
        elif 55 <= float(a[1]) < 75:
            scoring.append([2, "Neutral"])
        else:
            scoring.append([3, "Neutral"])

    return scoring


# Get Countries folder pathing
root = './data'
countrylist = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
print(countrylist)

for country in countrylist:
    prediction_scoring = calculate(f"{country}_analyse_result_retrained.csv")

    # Writing calculated value of 0-5 scoring, tagged with Positive/Neutral/Negative per comment
    with open(f'{country}_scoring_retrained_full.csv', 'w', newline='', encoding="utf-8") as csvoutput:
        writers = csv.writer(csvoutput)
        writers.writerows(prediction_scoring)

    scores = []
    cumulative_score = 0
    # Averaging out cumulated total of scores, to be given the final scoring per country
    with open(f'{country}_scoring_retrained_full.csv', newline='', encoding="utf-8") as r:
        readers = csv.reader(r)
        for rows in readers:
            cumulative_score += int(rows[0])
            scores.append(rows[0])

    print(cumulative_score)
    print(len(scores))

    country_avg_score = cumulative_score / len(scores)
    print(country_avg_score)
    print(round(country_avg_score, 2))

    with open(f'{country}_scores.csv', 'w', newline='', encoding="utf-8") as csvoutput1:
        writerss = csv.writer(csvoutput1)
        writerss.writerow([round(country_avg_score, 2)])
