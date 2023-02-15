import random
import math
import numpy as np
from matplotlib import pyplot

def open_and_read_file():
    with open("PDG1.txt", "r") as file:
        # lendo o conteúdo do arquivo
        contents = file.read()

        #numero de funcionarios
        n_funcionarios = contents[0]

        #numero de tarefas
        if(contents[2 + 1] != '\n'):
            conteudo = contents[2] + contents[2 + 1]
            n_tarefas = conteudo
        elif(contents[2 + 1] == '\n'):
            n_tarefas = contents[2]

        print("tarefas: "+n_tarefas)
        #matriz de horas
        matriz_hora = []
        z = 4 # 3 é \n
        
        for i in range(int(n_funcionarios)):
            linha = []             
            j = 0
            while(j < int(n_tarefas)):
                #caso seja numero
                if(contents[z] != '\n' and contents[z] != '\t'):
                    #caso seja numero >= 10
                    if(contents[z + 1] != '\t'):
                        conteudo = contents[z] + contents[z + 1]
                        conteudo2 = int(conteudo)
                        linha.append(conteudo2)     
                        z = z + 1
                        j = j + 1
                    elif(contents[z + 1] == '\t'):
                        conteudo = int(contents[z])
                        linha.append(conteudo)       
                        j = j +1
                    z = z + 1            
                else: #caso seja \n ou \t
                    z = z + 1  
                # TESTES   
                #print("j = " + str(j))
                #print("z = " + str(z))
                #print("adiciounou = ")
                #print(linha)

            matriz_hora.append(linha)
        
        #print(matriz_hora)

        #matriz de custos
        matriz_custos = []

        for i in range(int(n_funcionarios)):
            linha = []
             
            j = 0
            while(j < int(n_tarefas)):
                #caso seja numero
                if(contents[z] != '\n' and contents[z] != '\t'):
                    #caso seja numero >= 10
                    if(contents[z + 1] != '\t'):
                        conteudo = contents[z] + contents[z + 1]
                        conteudo2 = int(conteudo)
                        linha.append(conteudo2)     
                        z = z + 1
                        j = j + 1
                    elif(contents[z + 1] == '\t'):
                        conteudo = int(contents[z])
                        linha.append(conteudo)       
                        j = j +1
                    z = z + 1            
                else: # caso seja \n ou \t
                    z = z + 1     
                
                # TESTES
                #print("j = " + str(j))
                #print("z = " + str(z))
                #print("adiciounou = ")
                #print(linha)

            matriz_custos.append(linha)
        
        #print(matriz_custos)

        # quantidade de horas para cada funcionarios
        horas_funcionarios = []
        j = 0
        while(j < int(n_funcionarios)):
                #caso seja numero
                if(contents[z] != '\n' and contents[z] != '\t'):
                    #caso seja numero >= 10
                    if(contents[z + 1] != '\t'):
                        conteudo = contents[z] + contents[z + 1]
                        conteudo2 = int(conteudo)
                        horas_funcionarios.append(conteudo2)     
                        z = z + 1
                        j = j + 1
                    elif(contents[z + 1] == '\t'):
                        conteudo = int(contents[z])
                        horas_funcionarios.append(conteudo)       
                        j = j +1
                    z = z + 1            
                else: # caso seja \n ou \t 
                    z = z + 1 
        
        #print(horas_funcionarios)
        return n_funcionarios, n_tarefas, matriz_hora, matriz_custos, horas_funcionarios 


def arrependimento(matriz_horas, nfunc, tarefas):
    arrependimento = []
    aux = []
    for j in range(int(tarefas)):
        coluna = []
        aux = []
        for k in range(int(nfunc)):
            a = matriz_horas[k][j]
            coluna.append(a)
        segundo_menor = sorted(coluna)[1]
        menor = sorted(coluna)[0]
        ar = segundo_menor - menor
        aux.append(ar)
        aux.append(j)
        arrependimento.append(aux)
        
    return (arrependimento)
    

def popinicial(matriz_horas, arrependimento, nfunc, horas, tarefas):
    a = []
    S0 = []
    custo = 0
    # vai gerar dicionario para quantidade de funcionarios
    
    for i in range(int(nfunc)):
        tarefaFunc = {'Tarefas': [], 'Programador': 0}
        tarefaFunc["Programador"] = i
        S0.append(tarefaFunc)

    for i in range (int(tarefas)):
        a.append(arrependimento[i])  
    a.sort(reverse=True)

    for j in range(int(tarefas)):
        coluna = a[j][1]
        colunaInteira = []
        aux = []
        #separa a coluna da matriz
        for i in range(int(nfunc)):
            aux = matriz_horas[i][j]
            colunaInteira.append(aux)
        menor = sorted(colunaInteira)[0]

        penalidade = 0
        for i in range(int(nfunc)):
            if(colunaInteira[i] == menor):
                linhamenor = i
        

        if((horas[linhamenor] - matriz_horas[linhamenor][coluna] >= 0)):
            S0[linhamenor]['Tarefas'].append(coluna)
            horas[linhamenor] -= matriz_horas[linhamenor][coluna]
        else :
            S0[linhamenor]['Tarefas'].append(coluna)
            penalidade = abs(horas[linhamenor] - matriz_horas[linhamenor][coluna]) * 2
            horas[linhamenor] -= matriz_horas[linhamenor][coluna]
            custo += penalidade

        custo += matriz_custos[linhamenor][coluna]
    
    return custo, S0

def vizinhos(solucao, custo, matriz_custos, matriz_horas, n_func):
    vizinhos = []
    penalidadeanterior = 0
    
    trocaprogramador =  random.randint(0, int(n_func)-1)
    while(len(solucao[trocaprogramador]["Tarefas"]) <= 0):
        trocaprogramador =  random.randint(0, int(n_func)-1)
    
    trocatarefa = random.randint(0, len(solucao[trocaprogramador]["Tarefas"])-1)
    botatarefa= solucao[trocaprogramador]["Tarefas"][trocatarefa]    

    solucao[trocaprogramador]["Tarefas"].pop(trocatarefa)
    colocaprogramador = random.randint(0, int(n_func)-1)
    

    while(colocaprogramador == trocaprogramador):
        colocaprogramador = random.randint(0, int(n_func)-1)

    solucao[colocaprogramador]["Tarefas"].append(botatarefa)
    custo -= matriz_custos[trocaprogramador][trocatarefa]
    custo += matriz_custos[colocaprogramador][trocatarefa]

    horas_funcionarios[trocaprogramador] += matriz_horas[trocaprogramador][trocatarefa]

    if((horas_funcionarios[colocaprogramador] - matriz_horas[colocaprogramador][botatarefa] >= 0)):
        horas_funcionarios[colocaprogramador] -= matriz_horas[colocaprogramador][botatarefa]
    else :
        penalidade = abs(horas_funcionarios[colocaprogramador] - matriz_horas[colocaprogramador][botatarefa]) * 2
        horas_funcionarios[colocaprogramador] -= matriz_horas[colocaprogramador][botatarefa]
        custo += penalidade
    
    return solucao, custo
  
def SA(custo, T0, solucao, n_funcionarios, tarefas, matriz_horas, matriz_custos, horas_funcionarios ): 
    s = solucao
    melhor_s = s
    grafico_temperatura = []
    grafico_custo = []
    #parametros "s_novo e f_novo"= gera_nova_vizinhança(s)
    f_inicial = custo # f é o custo 
    f_novo = 0 
    EPSILON = 1e-10 #o importante eh nao chegar a 0
    temperatura = 1

    melhor_f = f_inicial
    #SAmax = 3      # SAmax é o numero de soluções por temperatura
    alfa = 0.99   # alfa é o fator de atenuação de temperatura

    while temperatura:  
        s_novo, f_novo = vizinhos(s, custo, matriz_custos, matriz_horas, n_funcionarios) #(prum f_novo e um s_novo)
      
        delta = f_novo - f_inicial #verificação do função objetivo
        if delta < 0:
            s = s_novo
            if(f_novo < melhor_f):
                melhor_s = s_novo
                melhor_f = f_novo
        elif np.exp(-delta / T0) < np.random.random():
            s = s_novo
        T0 *= alfa
        if(T0 < EPSILON):
            temperatura = 0

        grafico_temperatura.append(T0)
        grafico_custo.append(melhor_f)

    print(melhor_f)
    print(melhor_s)
    pyplot.xlim([0,600])
    pyplot.ylim([0,200])
    pyplot.plot(grafico_temperatura)
    pyplot.plot(grafico_custo)
   # pyplot.label
    pyplot.title(f'TABELA DA TEMPERATURA E CUSTO AO LONGO DO TEMPO DE EXECUÇÃO')
    pyplot.show()
    return melhor_s, melhor_f


n_funcionarios, tarefas, matriz_horas, matriz_custos, horas_funcionarios  = open_and_read_file() # chamando a function para funcionar

ar = arrependimento(matriz_horas, n_funcionarios, tarefas)

custoinicial, S0 = popinicial(matriz_horas,ar, n_funcionarios, horas_funcionarios ,tarefas)
aux = 0
t0 = 0
for i in range(3):
    Sk, aux = vizinhos(S0, custoinicial, matriz_custos, matriz_horas, n_funcionarios)
    t0 += aux
    aux = 0
t0 /= 3 

SA(custoinicial, t0, S0, n_funcionarios, tarefas, matriz_horas, matriz_custos, horas_funcionarios )

