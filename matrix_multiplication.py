def multiply_matrices(mod, mat1, mat2):
    res = [[0 for _ in range(len(mat2[0]))] for _ in range(len(mat1))]
    for i in range(len(mat1)):
        for j in range(len(mat2[0])):
            for k in range(len(mat2)):
                res[i][j] += (mat1[i][k] * mat2[k][j]) % mod
                res[i][j] %= mod
    return res

# Example usage:
mod = 1000000007
mat1 = [[1, 2, 3], [4, 5, 6]]
mat2 = [[7, 8], [9, 10], [11, 12]]
result = multiply_matrices(mod, mat1, mat2)
print(result)