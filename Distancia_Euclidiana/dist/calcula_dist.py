import csv
import math

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

# Método para calcular a distancia euclidiana entre dois pontos.
# Dados dois pontos é encontrado a quantidade de dimencoes e com isso calculado a distancia.
def calcEuclidianDistance(pointOne, pointTwo):
    dim, soma = len(pointOne), 0
    for i in range(dim):
        soma += math.pow(float(pointOne[i]) - float(pointTwo[i]), 2)
    return math.sqrt(soma)

# Método para calcular a distancia de um conjunto de dados.
# Dado um conjunto de dados é retornado uma matriz de distancia entre eles.
def calcDataDistance(data):
    matrizDistancias = []
    lenght = len(data)
    for i in range(lenght):
        row = []
        for j in range(lenght):
            distance = calcEuclidianDistance(data[i], data[j])
            row.append(round(distance, 4))
        matrizDistancias.append(row)
        
    return matrizDistancias

if __name__ == "__main__":
    # Pop-up da tela de selecionar o arquivo.
    csvFileName = sg.popup_get_file('Informe o diretório do arquivo: ')

    # Layout da tela de perguntar se possui classe.
    layout = [
        [sg.Text('O arquivo possui classe?')],
        [sg.Button('Sim'), sg.Button('Nao')]
    ]

    # Inicio da tela
    window = sg.Window('Calculo da Distancia Euclidiana', layout, element_justification='center')

    # Captura de evento e valores.
    event, values = window.read()

    hasClass = event
    irisData = readCsvFile(csvFileName)
    if hasClass == 'Sim':
        removeClass(irisData)
    matrizDistancias = calcDataDistance(irisData)
    writeCsvFile(matrizDistancias)

    # Pop-up de conclusao.
    sg.popup('Arquivo de Matriz de Distancia Euclidiana gerado com sucesso!')