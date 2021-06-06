# prep.py
# Takes in excel info and pickles it into a pandas df for easy retreival
import pandas as pd
import pickle

def prep(csv_file):
    df = pd.read_csv(csv_file)
    with open('checkout_info.pickle', 'wb') as f:
        pickle.dump(df, f)

def read(pickle_file):
    with open(pickle_file, 'rb') as f:
        df = pickle.load(f)
        return df
