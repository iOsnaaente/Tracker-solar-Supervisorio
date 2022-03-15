'''
Calcula a inversa de uma matriz NxN::
    >>> Matriz_A : list -> Uma matriz NxN para ser calculado a inversa
    >>> return : list -> Matriz NxN inversa calculada 
'''
def inv( Matriz_A : list ) -> list:
    N = len(Matriz_A) if len(Matriz_A) == len(Matriz_A[0]) else 0
    identidade = [ [ 0 for _ in range(N)] for _ in range(N) ]
    for linha in range( N ):
        for coluna in range(N):
            if(linha == coluna): 
                identidade[linha][coluna] = 1
            else:
                identidade[linha][coluna] = 0     
    for coluna in range(N):
        pivo = Matriz_A[coluna][coluna]
        for k in range(N):
            Matriz_A[coluna][k] = (Matriz_A[coluna][k])/(pivo)
            identidade[coluna][k] = (identidade[coluna][k])/(pivo)
        for linha in range(N):
            if(linha != coluna):
                m = Matriz_A[linha][coluna]
                for k in range(N):
                    Matriz_A[linha][k] = (Matriz_A[linha][k]) - (m*Matriz_A[coluna][k])
                    identidade[linha][k] = (identidade[linha][k]) - (m*identidade[coluna][k])
    return identidade 


'''
Faz a operação de multiplicação matricial entre uma matriz A(mxn) e um vetor B(nx1) e retorna um vetor coluna R(mx1) ::
    >>> mat_a : list -> matriz da operação
    >>> vector : list -> vetor da operação
    >>> return : list -> vetor coluna resultado
'''
def dot_mat_vec( mat_a : list, vector : list ) -> list: 
    if len(mat_a[0]) != len(vector):
        return 'Dismatch matricial'
    else:
        M = len(mat_a   )
        N = len(mat_a[0])
        P = 1
        doted = [ [ 0 ] for _ in range( M ) ]
    for i in range(M):
        for j in range(P):
            for k in range(N):
                doted[i][j] += mat_a[i][k] * vector[k]
    return doted 


'''
Faz a operação de multiplicação matricial entre uma matriz A(mxn) e um vetor B(nxr) e retorna uma matriz R(mxr) ::
    >>> mat_a : list -> matriz da operação
    >>> mat_b : list -> matriz da operação
    >>> return : list -> matriz resultado
'''
def dot( mat_a : list , mat_b : list) -> list: 
    if len(mat_a[0]) != len(mat_b):
        return 'Dismatch matricial'
    else: 
        M = len(mat_a   )
        N = len(mat_a[0])
        P = len(mat_b[0])
        doted = [ [ 0 for _ in range(P) ] for _ in range( M ) ]
    for i in range(M):
        for j in range(P):
            for k in range(N):
                doted[i][j] += mat_a[i][k] * mat_b[k][j]
    return doted 


'''
Faz a operação de potenciação matricial entre uma matriz base A(nxn) e um expoente inteiro I. Retorna uma matriz R(nxn)::
    >>> mat_a : list -> matriz NxN  da operação
    >>> exp : int -> expoente inteirto I da potência 
    >>> return : list -> matriz NxN resultado 
'''
def pow_dot( mat_a : list, exp : int ) -> list : 
    if exp == 1 :
        return mat_a 
    elif exp == 0 :
        return 1
    else : 
        return dot(mat_a, pow_dot( mat_a, exp -1 ))
    
    
'''
Faz a potenciação termo a termo de um vetor V de N termos por um expoente inteiro I::
    >>> Min : list -> Vetor de N termos
    >>> exp : int -> Expoente inteiro I
    >>> return : list -> Vetor de N termos calculado 
'''
def pow_vector( Min : list, exp : int ) -> list:
    return [ Min[i]**exp for i in range(len(Min)) ]


'''
Calcula a transposta de uma matriz A(nxm)::
    >>> mat : list -> Matriz A(nxm)
    >>> return : list -> Matriz A'(mxn) : transposta 
'''
def transp( mat : list) -> list:
    return list(map(lambda *i: [j for j in i], *mat))


'''
Gera um intervalo de termos iniciando em um ponto inicial A até um final B com N termos::
    >>> pI : float -> Ponto inicial
    >>> pF : float -> Ponto final 
    >>> qtd : int -> Quantidade de termos no intervalo
    >>> return : list -> Vetor intervalo I de N termos com menor termo iniciando em A e o maior em B
'''
def linspace( pI : float, pF : float, qtd : int ) -> list:
    dI = (pF - pI)/(qtd-1)
    return [ dI*i + pI for i in range(qtd)]


'''
Calcula os termos de um polinomio P em uma lista X que represeta os pontos de um intervalo qualquer
Os temos em P são os coeficientes de um polinomio do tipo::
    F(x) = A.x^4 + B.x^3 + C.x^2 + D.x + E
    onde::
    P = [ A, B, C, D, E ]
    Para um intervalo X sendo:
    X = [ p0, p1, p2, p3 ]
    Teriamos como saida
    f(x) = [ A.p0^4 + B.p0^3 + C.p0^2 + D.p0 + E,
             A.p1^4 + B.p1^3 + C.p1^2 + D.p1 + E,
             A.p2^4 + B.p2^3 + C.p2^2 + D.p2 + E,
             A.p3^4 + B.p3^3 + C.p3^2 + D.p3 + E,
           ] 
    -----------
    Argumentos::
        >>> P : list -> Lista de coeficientes P de um polinomio : len(P) == grau do polinomio
        >>> X : list -> Intervalo X do domínio da função polinomial dada por P : Domínio de uma função polinomial = DeR -> ( -inf, +inf )
        >>> return : list -> Lista de pontos f(x) calculado para cada ponto de X dados P : len(return) == len(X) 
'''
def polyvals( P : list, X : list ) -> list: 
    r_poly = [ 0 for i in range(len(X))] 
    N = len(P)
    T = len(X)
    for x in range( T ):
        for i in range(1,N+1):
            r_poly[x] += P[i-1]*X[x]**(N-i)
    return r_poly


'''
Calcula os termos de um polinomio P em um  valor X que represeta um ponto qualquer no dominio de f(x) 
Os temos em P são os coeficientes de um polinomio f(x) do tipo::
    F(x) = A.x^4 + B.x^3 + C.x^2 + D.x + E
    onde::
    P = [ A, B, C, D, E ]
    Para um valor X qualquer:
    X = p 
    Teriamos como saida
    f(x) = A.p^4 + B.p^3 + C.p^2 + D.p + E, 
    
    -----------
    Argumentos::
        >>> P : list -> Lista de coeficientes P de um polinomio : len(P) == grau do polinomio
        >>> X : list -> Valor X do domínio da função polinomial dada por P : Domínio de uma função polinomial = DeR -> ( -inf, +inf )
        >>> return : float -> Retorna o valor de X correspondente a função f(X) dados os coeficientes P do polinomio. 
'''
def polyval( P : list, X : list ) -> float:
    r_poly = 0.0
    N = len( P ) 
    for i in range( N ):
        r_poly += P[i-1]*X**(N-i)
    return r_poly 

'''
Calcula a aproximação polinomial de uma distribuição de pontos (``Xin``, ``Yin``)
A ordem do polomio é dada pelo expoente ``exp``.
Pode ser calculado um intervalo de pontos sobre a função polomial calculada
atributos::
    >>> Xin : list -> Pontos X da distribuição de entrada : len(Xin) == len(Yin)  
    >>> Yin : list -> Pontos Y da distribuição de entrada : len(Xin) == len(Yin)
    >>> exp : int = 1 -> Expoente máximo da função polinomial a ser calculada : grau polinomial ( valor padrão == 1 )
    >>> num : int = -1 ->  Número de pontos a ser calculado no intervalo de saida do polinomio.
    >>> return : list ( num == -1 ) -> Se o valor do atributo num esteja padrão (-1), somente os coeficientes A serão retornados
    >>> return : list ( num != -1 ) -> Caso seja setado, retorna um intervalo de pontos (x,y) de tamanho num 
'''
def get_aprox( Xin : list, Yin : list, num : int = -1 ):
    V = transp( [ pow_vector(Xin, 4), pow_vector(Xin, 3), pow_vector(Xin, 2), pow_vector(Xin, 1), pow_vector(Xin, 0) ] ) 
    a = transp( dot_mat_vec( dot( inv( dot( transp( V ), V) ), transp(V)), Yin ) )[0]
    if num:
        return a 
    else:
        Xout = linspace( Xin[0], Xin[-1], len(Xin) if num == -1 else num )
        Yout = polyvals( a, Xout )
        return [ Xout, Yout ]
    