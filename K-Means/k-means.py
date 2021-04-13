import csv
import math
import random
import numpy

import PySimpleGUI as sg

# Método para abrir um arquivo CSV e retornar uma matriz da dados.
def readCsvFile(csvFile):
    data = []
    with open(csvFile, newline='') as csvfile:
        fileCsv = csv.reader(csvfile, delimiter=',')
        for row in fileCsv:
            data.append(row)
        return data

# Método para receber um dado e escrever em um arquivo output.csv
def writeCsvFile(data):
    with open('output.csv', mode='w', newline="") as csvfile:
        fileCsv = csv.writer(csvfile, delimiter=',')
        for row in data:
            fileCsv.writerow(row)

# Método para remover a classe, a mesma deve estar na ultima coluna.
# TODO: Adicionar forma para escolher que coluna remover.
def removeClass(data):
    for row in data:
        row.pop()

def formatarCampo(data):
    newData = []
    for row in data:
        newRow = []
        for col in row:
            newCol = float(col)
            newRow.append(newCol)
        newData.append(newRow)
    return newData

# Método para calcular a distancia euclidiana entre dois pontos.
# Dados dois pontos é encontrado a quantidade de dimencoes e com isso calculado a distancia.
def calcEuclidianDistance(pointOne, pointTwo):
    dim, soma = len(pointOne), 0
    for i in range(dim):
        soma += math.pow(float(pointOne[i]) - float(pointTwo[i]), 2)
    return math.sqrt(soma)

# Método para selecionar os primeiros centroids aleatoriamente
def selectFirstCentroids(data, numberCluster):
    dataLength = len(data)
    return random.choices(data, k=numberCluster)

# Método para realocar os dados em cada cluster.
def recalculateClusters(dataSet, centroids, numberCluster):
    # Inicia os clusters como vazio.
    clusters = {}
    for i in range(numberCluster):
        clusters[i] = []
    
    # Para cada dado no conjunto de dados:
    for data in dataSet:
        # Cria-se um array de distancias euclidianas.
        euclidianDistances = []
        # Para cada centroide:
        for i in range(numberCluster):
            # É realizado o calculo entre o dado e o centroide, e adicionado ao array de distancias.
            euclidianDistances.append(calcEuclidianDistance(data, centroids[i]))
        # Seleciona o index no qual se encontra a menor distancia euclidiana.
        index = euclidianDistances.index(min(euclidianDistances))
        # É adicionado no cluster o dado.
        clusters[index].append(data)
    return clusters

# Método para recalcular os centroides.
def recalculateCentroids(clusters, numberCluster):
    centroids = []
    for i in range(numberCluster):
        centroids.append(numpy.average(clusters[i], axis=0))
    return centroids

# Método para o calculo de K-Means.
def kMeans(data, numberCluster):
    # Variável de controle do loop.
    count = 0

    # É realizado a seleção dos primeiros centroides.
    centroids = selectFirstCentroids(data, numberCluster)

    # Esta variável é utilizada para o controle em que é necessário saber os centroides antigos e os novos
    newCentroids = []
    # Variável de controle.
    flag = True
    # Enquanto o controle for verdadeiro:
    while flag:
        # Realoca os dados nos clusters.
        clusters = recalculateClusters(data, centroids, numberCluster)
        # Seleciona novos centroides.
        newCentroids = recalculateCentroids(clusters, numberCluster)
        # Verifica se o algoritmo ainda deve continuar rodando.
        flag = verifyCondition(count, centroids, newCentroids, numberCluster)
        # Salva os dados dos novos centroids para proximas operações.
        centroids = newCentroids
        # Atualiza o contador.
        count = count + 1
    return clusters

# Método para verificar se o código ainda deve continuar rodando
def verifyCondition(count, oldCentroid, newCentroid, numberCluster):
    hasChange = False
    # Se o contador for maior que 100 ele retorna false.
    if(count >= 100):
        return False
    # Para cada centroide:
    for i in range(numberCluster):
        # É realizado a subtração entre o centroide antigo e o novo calculado.
        result = numpy.diff([newCentroid[i], oldCentroid[i]], axis=0)
        soma = numpy.sum(result[0])
        # Se o resultado for 0, ou seja não houve auteração, a flag de mudança é alterada
        if(soma != 0):
            hasChange = True
    # Se houve mudança de centroide retorna false
    if(hasChange):
        return False
    return True

if __name__ == "__main__":
    title = 'K-Means'
    # Pop-up da tela de selecionar o arquivo.
    csvFileName = sg.popup_get_file('Informe o diretório do arquivo: ')
    dataWithClass = readCsvFile(csvFileName)

    # Layout da tela de perguntar se possui classe.
    layoutPossuiClasse = [
        [sg.Text('O arquivo possui classe?')],
        [sg.Button('Sim'), sg.Button('Nao')]
    ]

    # Layout da tela de quantos grupos devem existir.
    layoutNumeroCetroides = [
        [sg.Text('Quantos centróides você deseja?')],
        [sg.Input()],
        [sg.Button('Continuar')]
    ]

    # Inicio da tela
    window = sg.Window(title, layoutPossuiClasse, element_justification='center')
    # Captura de evento e valores.
    event, values = window.read()
    # Tela para informar se os dados possuem classe.
    hasClass = event
    

    if hasClass == 'Sim':
        # For para no output aparecer com as respectivas classes, se houver.
        data = []
        for dado in dataWithClass:
            data.append(dado.copy())
        removeClass(data)
    removeClass(data)
    data = formatarCampo(data)

    # Tela para receber quantos grupos devem existir.
    window = sg.Window(title, layoutNumeroCetroides, element_justification='center')
    event, values = window.read()
    qtdeGrupos = int(values[0])
    
    clusters = kMeans(data, qtdeGrupos)
    # For para adicionar os respectivos cluster em cada dado.
    for i in range(len(dataWithClass)):
        for j in range(len(clusters)):
            if(data[i] in clusters[j]):
                dataWithClass[i].append(j)

    writeCsvFile(dataWithClass)
    # Pop-up de conclusao.
    sg.popup('Arquivo de output gerado com sucesso!')