"""Statistical analysis script"""

import pandas as pd
import matplotlib.pyplot as plt

og_data = pd.read_csv('predictions.csv')

speaker_gender = []
partner_gender = []
about_gender = []

num_male_speakers, num_female_speakers, num_unknown_speakers = 0, 0, 0
num_neutral_partners, num_male_partners, num_female_partners, num_unknown_partners = 0, 0, 0, 0
num_neutral_about, num_male_about, num_female_about, num_nonbinary_about = 0, 0, 0, 0

def compare(dataframe, row, comparor, start, stop):
    """Returns whether the datum in the row-th row and comparor-th column of dataframe is
    greater than the data in the row-th row and n-th column of dataframe for all n in
    range(start, stop)"""
    result = True
    for comparand in range(start, stop):
        if comparor is not comparand:
            result = result and dataframe.iloc[row, comparor] > dataframe.iloc[row, comparand]
    return result

for tweet in range(len(og_data)):
    if og_data.iloc[tweet, 36] >= 0.52:
        SPEAKER = "Male" # conclusion is speaker is male
        num_male_speakers += 1
    elif og_data.iloc[tweet, 37] >= 0.52:
        SPEAKER = "Female" # conclusion is speaker is female
        num_female_speakers += 1
    else:
        SPEAKER = "Unknown" # conclusion is speaker is unknown
        num_unknown_speakers += 1

    speaker_gender.append(SPEAKER)

    if compare(og_data, tweet, 38, 38, 41):
        PARTNER = "Gender Neutral" # conclusion is partner is gender neutral
        num_neutral_partners += 1
    elif og_data.iloc[tweet, 39] >= 0.52:
        PARTNER = "Male" # conclusion is partner is male
        num_male_partners += 1
    elif og_data.iloc[tweet, 40] >= 0.52:
        PARTNER = "Female" # conclusion is partner is female
        num_female_partners += 1
    else:
        PARTNER = "Unknown" # conclusion is partner is unknown
        num_unknown_partners += 1

    partner_gender.append(PARTNER)

    if compare(og_data, tweet, 41, 41, 45):
        ABOUT = "Gender Neutral" # conclusion is about is gender neutral
        num_neutral_about += 1
    elif compare(og_data, tweet, 42, 41, 45):
        ABOUT = "Female" # conclusion is about is female
        num_female_about += 1
    elif compare(og_data, tweet, 43, 41, 45):
        ABOUT = "Male" # conclusion is about is male
        num_male_about += 1
    else:
        ABOUT = "Non-binary" # conclusion is about is non-binary
        num_nonbinary_about += 1

    about_gender.append(ABOUT)

print("Number of tweets with male speakers: " + str(num_male_speakers))
print("Number of tweets with female speakers: " + str(num_female_speakers))
print("Number of tweets with unknown speakers: " + str(num_unknown_speakers) + "\n")

print("Number of tweets with male partners: " + str(num_male_partners))
print("Number of tweets with female partners: " + str(num_female_partners))
print("Number of tweets with unknown partners: " + str(num_unknown_partners))
print("Number of tweets with neutral partners: " + str(num_neutral_partners) + "\n")

print("Number of tweets about males: " + str(num_male_about))
print("Number of tweets about females: " + str(num_female_about))
print("Number of tweets about neutral gender: " + str(num_neutral_about))
print("Number of tweets about non-binary: " + str(num_nonbinary_about))

og_data['Speaker Gender'] = speaker_gender
og_data['Partner Gender'] = partner_gender
og_data['About Gender'] = about_gender

og_data.to_csv('labeleddata.csv')

pie_speakers = [num_male_speakers, num_female_speakers, num_unknown_speakers]
speaker_labels = ["Male", "Female", "Unknown"]

pie_partners = [num_neutral_partners, num_male_partners, num_female_partners, num_unknown_partners]
partner_labels = ["Neutral", "Male", "Female", "Unknown"]

pie_about = [num_neutral_about, num_male_about, num_female_about, num_nonbinary_about]
about_labels = ["Neutral", "Male", "Female", "Non-binary"]

graph = plt.pie(pie_speakers, labels = speaker_labels)
plt.title("Gender of speaker in tweet")
plt.show()

plt.clf()
graph = plt.pie(pie_partners, labels = partner_labels)
plt.title("Gender of person being spoken to in tweet")
plt.show()

plt.clf()
graph = plt.pie(pie_about, labels = about_labels)
plt.title("Gender of person spoken about in tweet")
plt.show()
