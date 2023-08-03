class Multi:
    def mul_matrix( matrix1,  matrix2):
        if len( matrix1[0]) == len( matrix2):
            m = [[0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0]]

            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        m[i][j] += ( matrix1[i][k] *  matrix2[k][j])

            return m
        
    def var_Mul_Matrix(matrixes):
        res = [[1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]]
        
        for matrix in matrixes:
            res = Multi.mul_matrix(res,matrix)
        return res

    def mul_vector( matrix1, vector):
        v = [0.0, 0.0, 0.0, 0.0]
        for i in range(4):
            for j in range(4):
                v[i] += ( matrix1[i][j] * vector[j])

        return v
    
    
    def barycentricCoords(A,B,C,P):
        areaPCB = ((B[1]-C[1]) * (P[0]-C[0]) + (C[0]-B[0]) * (P[1]-C[1])) 
        areaACP = ((C[1]-A[1]) * (P[0]-C[0]) + (A[0]-C[0]) * (P[1]-C[1])) 
        areaABC = ((B[1]-C[1]) * (A[0]-C[0]) + (C[0]-B[0]) * (A[1]-C[1])) 
        
        try:
            u= areaPCB/areaABC
            v= areaACP/areaABC
            w= 1-u-v
            return u,v,w
        except:
            return -1,-1,-1
