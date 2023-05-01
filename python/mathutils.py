import numpy as np


def create_generation_G(k, n):
    try:
        G = np.random.randint(0, 2, size=(k, n))
        print(f"\t- Successfully create Generation matrix G[{k},{n}]")
        return G
    
    except ValueError as e:
        print(f"Error from 'create_G[{k},{n}]': {e}")

    return None


def create_invertible_S_inverse_S_inv(k):
    try:
        I = np.eye(k) 
        while True:
            S = np.random.randint(2, size=(k, k))
               
            test = np.linalg.det(S)
            if test != 0:
                S_inv = np.linalg.inv(S).astype(int)
                SS_inv = np.dot(S, S_inv)
                if np.allclose(SS_inv, I):
                    print(f"\t- Successfully create Invertible matrix S[{k},{k}]") 
                    print(f"\t- Successfully create Inverse matrix S^-1")
                    return S, S_inv
 
    except ValueError as e:
        print(f"Error from 'create_S_S^-1[{k},{k}]': {e}")

    return None


def create_permutation_P(n):
    try:
        arr = np.arange(n)

        # Apply the Fisher-Yates shuffle method to shuffle the elements
        for i in range(n-1):
            j = np.random.randint(i, n)
            arr[i], arr[j] = arr[j], arr[i]

        # Create a permutation matrix P from the elements in the array arr
        P = np.zeros((n, n))
        for i in range(n):
            P[i, arr[i]] = 1

        P = P.astype(int)
        if np.linalg.det(P) != 0:
            print(f"\t- Successfully create Permutation matrix P[{n},{n}]")
            return P 

    except ValueError as e:
        print(f"Error from 'create_P[{n},{n}]': {e}")

    return None


def create_matrix_Gp(G, S, P):
    try:
        Gp = np.dot(np.dot(S, G), P)
        print(f"\t- Successfully create create matrix Gp[{G.shape[0]},{G.shape[1]}]")
        return Gp
    
    except ValueError as e:
        print(f"Error from 'create_Gp = S*G*P': {e}")

    return None


def create_inverse_P(matrix):
    try:
        matrix_inv = np.linalg.inv(matrix).astype(int)
        print(f"\t- Successfully create inverse matrix P^-1")
        return matrix_inv
    
    except ValueError as e:
        print(f"Error from 'create_P^-1': {e}")

    return None


def random_matrix(k, n):
    try:
        matrix = np.random.randint(2, size=(k, n))
        print(f"\t- Successfully create generate random error matrix e[{k},{n}]")
        return matrix
    
    except ValueError as e:
        print(f"Error from 'Create_error_e[{k},{n}]': {e}")

    return None


def cipherText(Cp, e):
    try:
        if Cp.ndim == 1:
            y = np.add(Cp, e)
            print(f"\t- Successfully create generated ciphertext y = Cp + e")
            return y
        
        elif Cp.ndim > 1 or len(Cp.shape) > 1:
            m, n = Cp.shape
            p, q = e.shape
            if n != q:
                return None
            y = np.zeros((p, n))
            for i in range(m):
                for j in range(n):
                    y[i][j] = Cp[i][j] + e[i][j]

            for i in range(m, p):
                for j in range(n):
                    y[i][j] = e[i][j]
            print(f"\t- Successfully create generated ciphertext y = Cp + e")
            return y
    
    except ValueError as e:
        print(f"Error from 'Create_y = Cp + e': {e}")

    return None


def multi_matrix(a, b):
    try:
        res = np.dot(a, b)
        return res
    
    except ValueError as e:
        print(f"Error from 'matrix_A * matrix_B': {e}")

    return None