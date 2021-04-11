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

def selectFirstCentroids(data, numberCluster):
    dataLength = data.__len__()
    return random.choices(data, k=numberCluster)

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

def recalculateCentroids(clusters, numberCluster):
    centroids = []
    for i in range(numberCluster):
        centroids.append(numpy.average(clusters[i], axis=0))
    return centroids

def kMeans(data, numberCluster):
    count = 0
    centroids = selectFirstCentroids(data, numberCluster)
    newCentroids = []
    flag = True
    while flag:
        clusters = recalculateClusters(data, centroids, numberCluster)
        newCentroids = recalculateCentroids(clusters, numberCluster)
        flag = verifyCondition(count, centroids, newCentroids, numberCluster)
        centroids = newCentroids
        count = count + 1
    return clusters


def verifyCondition(count, oldCentroid, newCentroid, numberCluster):
    hasChange = False
    if(count >= 100):
        return False
    for i in range(numberCluster):
        result = numpy.diff([newCentroid[i], oldCentroid[i]], axis=0)
        soma = numpy.sum(result[0])
        if(soma != 0):
            hasChange = True
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

    layoutNumeroCetroides = [
        [sg.Text('Quantos centróides você deseja?')],
        [sg.Input()],
        [sg.Button('Continuar')]
    ]

    # Inicio da tela
    #window = sg.Window(title, layoutPossuiClasse, element_justification='center')
    # Captura de evento e valores.
    #event, values = window.read()
    # Tela para informar se os dados possuem classe.
    #hasClass = event
    
    #if hasClass == 'Sim':
    #    removeClass(data)
    data = []
    for dado in dataWithClass:
        data.append(dado.copy())
    removeClass(data)
    data = formatarCampo(data)

    # Tela para receber quantos grupos devem existir.
    window = sg.Window(title, layoutNumeroCetroides, element_justification='center')
    event, values = window.read()
    qtdeGrupos = int(values[0])
    
    clusters = kMeans(data, qtdeGrupos)
    for i in range(len(dataWithClass)):
        for j in range(len(clusters)):
            if(data[i] in clusters[j]):
                dataWithClass[i].append(j)

    writeCsvFile(dataWithClass)
    # Pop-up de conclusao.
    sg.popup('Arquivo de Matriz de Distancia Euclidiana gerado com sucesso!')