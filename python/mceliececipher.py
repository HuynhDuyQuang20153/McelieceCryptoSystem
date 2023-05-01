from mathutils import *


class McElieceCipher:
    def __init__(self, t, k, n):
        self.t = t
        self.k = k
        self.n = n
        self.G = None
        self.S = None
        self.P = None
        self.P_inv = None
        self.S_inv = None
        self.Gp = None
        self.Gp_row = None
        self.Gp_col = None
        self.e = None
        self.y = None
        self.x = None
        self.xS = None
        self.y_ = None
        self.yy_= None
        self.Cp = None


    def generate_create_keys(self):
        # Create generation matrix G
        self.G = create_generation_G(self.n, self.k*3)

        # Create the invertible matrix S and the inverse matrix S^-1
        self.S, self.S_inv = create_invertible_S_inverse_S_inv(self.G.shape[0])

        # Create permutation matrix P
        self.P = create_permutation_P(self.G.shape[1])

        # Create matrix Gp
        self.Gp = create_matrix_Gp(self.G, self.S, self.P)
        self.Gp_row = self.Gp.shape[0]
        self.Gp_col = self.Gp.shape[1]

        # Create the inverse matrix P^-1
        self.P_inv = create_inverse_P(self.P)


    def encrypt(self, x, Gp, Gp_col, t):
        if Gp is not None and x is not None:
            # Create ciphertext vector Cp = x * G'
            self.Cp = multi_matrix(x, Gp)
            print(f"\t- Successfully create generated ciphertext vector Cp = x * Gp")

            # Random error matrix e
            self.e = random_matrix(t, Gp_col)

            # Create ciphertext y = Cp + e
            self.y = cipherText(self.Cp, self.e)


    def decrypt(self, matrix, y, P_inv, S_inv, S):
        if P_inv is not None and S_inv is not None:
            # Create plaintext vector y' = y*P^-1 = (x*G'+e)*P^-1 = G*S*x + P^-1*e = G*(Sx) + e'
            self.y_ = multi_matrix(y, P_inv)
            print(f"\t- Successfully create generated ciphertext vector y' = y * P^-1")

            # Create matrix xS 
            self.xS = multi_matrix(matrix, S)
            print(f"\t- Successfully create value xS")

            # Create plaintext x = xS * S^-1
            self.x = multi_matrix(self.xS, S_inv)
            print(f"\t- Successfully restore the original matrix x = xS * S^-1")
