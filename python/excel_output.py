import openpyxl
import os
import joblib
import shutil
import numpy as np
import pandas as pd


class Excel_output:
    def __init__(self, choose_type_file, already_assigned, encoder, texts, path_location_save, data_line):
        self.choose_type_file = choose_type_file
        self.encoder = encoder
        self.already_assigned = already_assigned
        self.texts = texts
        self.data_line = data_line
        self.path_location_save = path_location_save

    def Excel_Write_output(self):
        dir_path = os.path.join(os.getcwd(), "..", "data", "Save_file")
        max_index = 0
        for filename in os.listdir(dir_path):
            if filename.startswith("Save_turn_") and os.path.isdir(os.path.join(dir_path, filename)):
                index = int(filename.split("_")[2])
                if index > max_index:
                    max_index = index

        new_dir_path = os.path.join(dir_path, "Save_turn_" + str(max_index))

        path_plain = os.path.join(new_dir_path, "PlainText")
        if not os.path.exists(path_plain):
            os.mkdir(path_plain)

        if self.choose_type_file == '1':
            input_file = os.path.join(self.path_location_save)
            output_file = os.path.join(path_plain, "Cipher.xlsx")
            shutil.copyfile(input_file, output_file)

            df_back = pd.DataFrame(self.data_line, columns=None)
            df_back.columns = range(df_back.shape[1])

            save_path = os.path.join(path_plain, "Plain.xlsx")
            df = df_back.applymap(lambda x: pd.to_numeric(x, errors='ignore') if isinstance(x, str) else x)
            df.to_excel(save_path, startrow=0, index=False, columns=None, header=False)

            print(f"\t- Save PlainText in: {save_path}")

        elif self.choose_type_file == '2':
            input_file = os.path.join(self.path_location_save)
            output_file = os.path.join(path_plain, 'Cipher.txt')
            shutil.copyfile(input_file, output_file)

            txt_file = "Plain.txt"
            txt_path = os.path.join(path_plain, txt_file)
            with open(txt_path, "a", encoding='utf-8') as f:
                np.savetxt(f, self.texts, fmt="%s", delimiter=", ")

            print(f"\t- Save PlainText in: {txt_path}")


            