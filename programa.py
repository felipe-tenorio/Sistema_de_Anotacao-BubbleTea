from biblioteca import *


#Recebendo dados do arquivo
arquivo = "dados.csv"
try:
     with open(arquivo) as file:
          data_clientes = file.readlines()
except:
     with open(arquivo, mode='w') as file:
          file.write('Nome;Categoria;Cashback\n')
     with open(arquivo) as file:
          data_clientes = file.readlines()

#Transformando os dados do arquivo em um dicionario com valores em formato de lista
dicionario = dict()
chaves = data_clientes[0].strip('\n').split(';')
for i in range(len(data_clientes)):
     data_clientes[i] = data_clientes[i].strip('\n').split(';')

for c in chaves:
     dicionario[c] = []

for i in range(1, len(data_clientes)):
     for x in range(len(chaves)):
          dicionario[chaves[x]].append(data_clientes[i][x])

#Cadastro/Login
continuar = 0
while continuar == 0:
     acao = input('Digite [0] fazer o pedido de um cliente. \nDigite [1] para mostrar o histórico de pedidos. \nDigite [2] para sair do programa.')
     match acao:
          case '0':
               validacao = 0
               while validacao == 0:
                    nome = input('Digite o nome do cliente: \n').lower()
                    if ';' in nome or chr(92) in nome:
                         print('Simbólos não permitidos foram utilizados.')
                         validacao = 0
                    else:
                         validacao = 1
               cliente = Cliente(dicionario, nome)
               if cliente.identificador == None:
                    dicionario[chaves[0]].append(nome)
                    dicionario[chaves[1]].append(input('Qual a profissão do cliente? ').lower())
                    dicionario[chaves[2]].append('0')
                    print('O cliente foi registrado\n')
                    cliente = Cliente(dicionario, nome)
               else:
                    print('Cliente indentificado\n')

               pedido = Pedido()
               pedido.escolher_base()
               pedido.escolher_adicional()
               pedido.verificar_desconto(cliente.categoria)
               pedido.escolher_cashback(cliente)
               resumo_pedido(pedido, cliente)
               cliente.atualizar_cahback(dicionario)
               registro_pedido(pedido, cliente)

          case '1':
               print('Em produção')
          case '2':
               continuar = 1

#Guardar informações no aruivos 'dados.csv'
lista = ['Nome;Categoria;Cashback\n']
for i in range(len(dicionario[chaves[0]])):
     string = dicionario[chaves[0]][i]+';'+dicionario[chaves[1]][i]+';'+dicionario[chaves[2]][i]+'\n'
     lista.append(string)
dados = str()
for i in range(len(lista)):
     dados += lista[i]

with open(arquivo, mode='w') as file:
     file.write(dados)
