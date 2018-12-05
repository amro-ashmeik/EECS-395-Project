import movie_classifier as tc
import pandas as pd

df = pd.read_csv('finaldata.csv')
df = tc.tweet_classifier(df)
df.generate_report()