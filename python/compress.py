import numpy as np
import os

class Compress:
    def __init__(self, private_key, public_key, orther, direc_cipherText, direc_plaintText, matrix):
        self.S = private_key['S']
        self.P = private_key['P']
        self.G = private_key['G']
        self.Gp = public_key['Gp']
        self.vector_cipher = direc_cipherText['vector']
        self.ciphertext = direc_cipherText['ciphertext']
        self.vector_plain = direc_plaintText['vector']
        self.plainText = direc_plaintText['plainText']
        self.matrix = matrix


    def Compress_Write(self):
        # The path to folder where the data is to be saved
        dir_path = os.path.join(os.getcwd(), "..", "data", "Compress_npz")


        # Find the largest index of the folder compress_x created
        max_index = 0
        for filename in os.listdir(dir_path):
            if filename.startswith("Compress_folder_") and os.path.isdir(os.path.join(dir_path, filename)):
                index = int(filename.split("_")[2])
                if index > max_index:
                    max_index = index


        # Create a new directory with index max_index + 1
        new_dir_path = os.path.join(dir_path, "Compress_folder_" + str(max_index + 1))
        os.mkdir(new_dir_path)


        # File name 
        compress_file = "Compress.npz"


        # Create compress file with G, S, P, Gp, Cp, y, yy_, x
        compress_path = os.path.join(new_dir_path, compress_file)
        np.savez_compressed(compress_path, G=self.G, S=self.S, P=self.P, Gp=self.Gp, 
                                Cp=self.vector_cipher, y=self.ciphertext, yy_=self.vector_plain, 
                                x=self.plainText, matrix=self.matrix)
        print(f"\t- Save data in: '{compress_path}'")


        # Show data in '.npz' file
        # data = np.load(compress_path)
        # G = data['G']
        # S = data['S']
        # P = data['P']
        # Gp = data['Gp']
        # Cp = data['Cp']
        # y = data['y']
        # yy_ = data['yy_']
        # x = data['x']
        # matrix = data['matrix']
        # print(f"\n- File '{compress_file}' vua duoc nen: ")
        # print(f"G: \n", G)
        # print(f"S: \n", S)
        # print(f"P: \n", P)
        # print(f"Gp: \n", Gp)
        # print(f"Cp: \n", Cp)
        # print(f"y: \n", y)
        # print(f"yy_: \n", yy_)
        # print(f"x: \n", x)
        # print(f"matrix: \n", matrix)