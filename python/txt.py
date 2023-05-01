import os
import numpy as np

class TXT:
    def __init__(self, data, text):
        self.data = data
        self.text = text


    def TXT_Write(self):
        # The path to folder where the data is to be saved
        dir_path = os.path.join(os.getcwd(), "..", "data", "Txt_file")


        # Find the largest index of the folder Data_x created
        max_index = 0
        for filename in os.listdir(dir_path):
            if filename.startswith("Txt_folder_") and os.path.isdir(os.path.join(dir_path, filename)):
                index = int(filename.split("_")[2])
                if index > max_index:
                    max_index = index


        # Create a new directory with index max_index + 1
        new_dir_path = os.path.join(dir_path, "Txt_folder_" + str(max_index + 1))
        os.mkdir(new_dir_path)


        # The path to '.txt' file
        txt_file = "Data.txt"
        data_path = os.path.join(new_dir_path, txt_file)


        # Save data in '.txt' file
        with open(data_path, "a") as f:
            f.write("Text Original:\n")
            np.savetxt(f, self.data, fmt="%s", delimiter=", ")

            f.write("\nPlainText:\n")
            np.savetxt(f, self.text, fmt="%s", delimiter=", ")

        print(f"\t- Save matrix in: {data_path}")