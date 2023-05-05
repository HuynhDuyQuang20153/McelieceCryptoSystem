import openpyxl
import os
import pandas as pd


class df_Excel:
    def __init__(self, data_line):
        self.data_line = data_line


    def df_Write(self):
        file_name = "output.xlsx"
        dir_path = os.path.join(os.getcwd(), "..", "data", "Save_Excel")
        max_index = 0
        for filename in os.listdir(dir_path):
            if filename.startswith("Save_Excel_") and os.path.isdir(os.path.join(dir_path, filename)):
                index = int(filename.split("_")[2])
                if index > max_index:
                    max_index = index

        new_dir_path = os.path.join(dir_path, "Save_Excel_" + str(max_index + 1))
        os.mkdir(new_dir_path)

        df_back = pd.DataFrame(self.data_line, columns=None)
        df_back.columns = range(df_back.shape[1])

        data_path = os.path.join(new_dir_path, file_name)
        df_back.to_excel(data_path, startrow=0, index=False, columns=None, header=False)

        print(f"\t- Save data in: '{data_path}'")