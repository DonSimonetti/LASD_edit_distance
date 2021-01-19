import math

cost = {
    "DEL": 1,
    "INS": 1,
    "COPY": 0,
    "REP": 2,
    "TWI": 1
}


def editDistance(stringX, stringY):
    matrixC = [[0 for i in range(stringY.__len__()+1)] for j in range(stringX.__len__()+1)]
    matrixOp = [[ [""] for i in range(stringY.__len__()+1) ] for j in range(stringX.__len__()+1)]

    for i in range(stringX.__len__()+1):
        matrixC[i][0] = i * cost["DEL"]
        matrixOp[i][0] = "DEL"

    for i in range(stringY.__len__()+1):
        matrixC[0][i] = i * cost["INS"]
        matrixOp[0][i] = "INS"

    for i in range(1, stringX.__len__()+1):
        for j in range(1, stringY.__len__()+1):
            matrixC[i][j] = math.inf
            if stringX[i-1] == stringY[j-1]:
                matrixC[i][j] = matrixC[i - 1][j - 1] + cost["COPY"]
                matrixOp[i][j] = "COP"

            if stringX[i-1] != stringY[j-1] and matrixC[i - 1][j - 1] + cost["REP"] < matrixC[i][j]:
                matrixC[i][j] = matrixC[i - 1][j - 1] + cost["REP"]
                matrixOp[i][j] = "REP"

            if i >= 2 and j >= 2 and stringX[i - 1] == stringY[j - 2] and stringX[i - 2] == stringY[j - 1] and matrixC[i - 2][j - 2] + cost["TWI"] < matrixC[i][j]:
                matrixC[i][j] = matrixC[i - 2][j - 2] + cost["TWI"]
                matrixOp[i][j] = "TWI"

            if matrixC[i - 1][j] + cost["DEL"] < matrixC[i][j]:
                matrixC[i][j] = matrixC[i - 1][j] + cost["DEL"]
                matrixOp[i][j] = "DEL"

            if matrixC[i][j - 1] + cost["DEL"] < matrixC[i][j]:
                matrixC[i][j] = matrixC[i][j - 1] + cost["INS"]
                matrixOp[i][j] = "INS"
    #return matrixC, matrixOp
    return matrixC[-1][-1] #distanza
