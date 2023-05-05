import numpy as np


def can_create_matrix(X):
    try:
        num_cols = len(X[0])
        same_num_cols = True
        for row in X:
            if len(row) != num_cols:
                same_num_cols = False
                break

        return same_num_cols
    
    except ValueError as e:
        print(f"Error from 'can_create_matrix_?': {e}")

    return None 


def paddingMatrix(X):
    try:
        max_length = max([len(row) for row in X])
        input = np.zeros((len(X), max_length))
        already_assigned = np.zeros_like(input, dtype=bool)

        for i, row in enumerate(X):
            input[i, :len(row)] = row
            already_assigned[i, :len(row)] = True

        return input.astype(int), already_assigned
    
    except ValueError as e:
        print(f"Error from 'padding to matrix': {e}")

    return None 


def create_generation_G(k, n):
    try:
        print(f"\t- Creating Generation matrix G .....")
        G = np.random.randint(0, 2, size=(k, n))
        print(f"\t   --> Successfully create Generation matrix G[{k},{n}]")
        return G
    
    except ValueError as e:
        print(f"Error from 'create_G[{k},{n}]': {e}")

    return None


def create_invertible_S_inverse_S_inv(k):
    try:
        I = np.eye(k) 
        print(f"\t- Creating Invertible matrix S .....")
        count = 0
        while True:
            S = np.random.randint(2, size=(k, k))
            count+=1
            test = np.linalg.det(S)
            if test != 0:
                S_inv = np.linalg.inv(S).astype(int)
                SS_inv = np.dot(S, S_inv)
                if np.allclose(SS_inv, I):
                    print(f"\t   --> Successfully create Invertible matrix S[{k},{k}]") 
                    print(f"\t   --> Number of random time S: ", count)
                    print(f"\t   --> Successfully create Inverse matrix S^-1")
                    return S, S_inv
                
    except ValueError as e:
        print(f"Error from 'create_S_S^-1[{k},{k}]': {e}")

    return None


def create_permutation_P(n):
    try:
        print(f"\t- Creating Permutation matrix P .....")
        arr = np.arange(n)

        for i in range(n-1):
            j = np.random.randint(i, n)
            arr[i], arr[j] = arr[j], arr[i]

        P = np.zeros((n, n))
        for i in range(n):
            P[i, arr[i]] = 1

        P = P.astype(int)
        if np.linalg.det(P) != 0:
            print(f"\t   --> Successfully create Permutation matrix P[{n},{n}]")
            return P 

    except ValueError as e:
        print(f"Error from 'create_P[{n},{n}]': {e}")

    return None


def create_matrix_Gp(G, S, P):
    try:
        print(f"\t- Creating matrix Gp .....")
        Gp = np.dot(np.dot(S, G), P)
        print(f"\t   --> Successfully create matrix Gp[{G.shape[0]},{G.shape[1]}]")
        return Gp
    
    except ValueError as e:
        print(f"Error from 'create_Gp = S*G*P': {e}")

    return None


def create_inverse_P(matrix):
    try:
        print(f"\t- Creating inverse matrix P^-1 .....")
        matrix_inv = np.linalg.inv(matrix).astype(int)
        print(f"\t   --> Successfully create inverse matrix P^-1")
        return matrix_inv
    
    except ValueError as e:
        print(f"Error from 'create_P^-1': {e}")

    return None


def random_matrix(k, n):
    try:
        print(f"\t- Creating generate random error matrix e .....")
        matrix = np.random.randint(2, size=(k, n))
        print(f"\t   --> Successfully create generate random error matrix e[{k},{n}]")
        return matrix
    
    except ValueError as e:
        print(f"Error from 'Create_error_e[{k},{n}]': {e}")

    return None


def cipherText(Cp, e):
    try:
        print(f"\t- Creating generated ciphertext y .....")
        if Cp.ndim == 1:
            y = np.add(Cp, e)
            print(f"\t   --> Successfully create generated ciphertext y = Cp + e")
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
            print(f"\t   --> Successfully create generated ciphertext y = Cp + e")
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


#-------------------------------------- MULTIPROCESSING ----------------------------------------------
def get_input_data(key):
    try:
        text = key[0][0]   
        data_line = key[0][1]   
        matrix_text = key[0][2]   
        already_assigned = key[0][3]  
        t = key[0][4]   
        k = key[0][5]   
        n = key[0][6]   
        encoder = key[0][7]  
        return text, data_line, matrix_text, already_assigned, t, k, n, encoder
    
    except ValueError as e:
        print(f"Error from 'get_input_data': {e}")

    return None


def get_key_data(key_):
    try: 
        private_key = key_[0][0]
        public_key = key_[0][1]
        orther = key_[0][2]
        return private_key, public_key, orther

    except ValueError as e:
        print(f"Error from 'get_key_data': {e}")
        
    return None


def get_encrypt_data(key_):
    try:
        direc_cipherText = key_[0]
        return direc_cipherText

    except ValueError as e:
        print(f"Error from 'get_encrypt_data': {e}")
        
    return None


def get_decrypt_data(key_):
    try:
        direc_plaintText = key_[0]
        return direc_plaintText
    
    except ValueError as e:
        print(f"Error from 'get_decrypt_data': {e}")
        
    return None


def get_backtext(backtext):
    try:
        text_recovery = backtext[0][0]
        texts = backtext[0][1]
        return text_recovery, texts
    
    except ValueError as e:
        print(f"Error from 'get_backtext': {e}")
        
    return None
