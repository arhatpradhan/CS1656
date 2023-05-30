import json
from datetime import datetime, timedelta
import requests
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Task(object):
    def __init__(self):
        self.df = pd.read_csv('bank-data.csv')

    def t1(self):
        income_by_sex = self.df.groupby('sex')['income'].mean()
        return income_by_sex

    def t2(self):
        ct = pd.crosstab(self.df['save_act'], self.df['mortgage'], margins=True)
        return ct

    def t3(self):
        ct = pd.crosstab(self.df['save_act'], self.df['mortgage'], margins=True)
        ct_pct = ct.apply(lambda r: (r/(r.sum())*2), axis = 1)
        return ct_pct[:2].append(ct.iloc[-1:])

if __name__ == "__main__":
    t = Task()
    print("----T1----" + "\n")
    print(str(t.t1()) + "\n")
    print("----T2----" + "\n")
    print(str(t.t2()) + "\n")
    print("----T3----" + "\n")
    print(str(t.t3()) + "\n")
