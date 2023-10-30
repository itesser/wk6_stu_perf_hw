import pandas as pd
from pathlib import Path

sources = {"mat": "student-mat.csv", "por": "student-por.csv"}


class Base:
    def __init__(self, files: dict = sources):
        self.sources = files
        self.get_data()
        self.clean_data()

    def get_data(self):
        self.data = pd.DataFrame()
        folder_dir = f"{Path(__file__).parents[0]}\\data"
        for k, v in self.sources.items():
            df = pd.read_csv(f"{folder_dir}\\{v}", delimiter=";")
            df["subj"] = k
            new_cols = []
            for col in df.columns:
                if col == col.lower():
                    new_cols.append(col)
                else:
                    if col[0] == col[0].upper():
                        new_cols.append(col[0].lower() + "_" + col[1:])
            df.columns = new_cols
            self.data = pd.concat([self.data, df], ignore_index=True)
        self.data.reindex()

    def clean_data(self):
        sample = self.data.loc[0]
        bool_cols = []
        for i in range(len(sample)):
            try:
                if sample.iloc[i].lower() == "yes" or sample.iloc[i].lower() == "no":
                    bool_cols.append(self.data.columns[i])
            except:
                pass
        for col in bool_cols:
            self.data[col] = (
                self.data[col].str.replace("no", "False").str.replace("yes", "True")
            )
        # self.data.drop(columns="index", inplace=True)


if __name__ == "__main__":
    d = Base()
    print(d.data.head())
    print(d.data.shape)
