class Cliente:
    def __init__(self, dicionario, nome):
        n_registro = None
        count =0
        for i in dicionario['Nome']:
            if nome == i:
                n_registro = count
            count = count + 1
        if n_registro == None:
            self.identificador = None
        else:
            self.dicionario = dicionario
            self.identificador = n_registro
            self.nome = dicionario['Nome'][n_registro]
            self.categoria = dicionario['Categoria'][n_registro]
            self.cashback = round(float(dicionario['Cashback'][n_registro]),2)

    def atualizar_cahback(self, dicionario):
        dicionario['Cashback'][self.identificador] = str(self.cashback)


class Pedido():
    def __init__(self):
        self.base = str()
        self.adicionais = list()
        self.preco_total = 0.00
        self.preco_final = 0.00
        self.desconto = None
        self.cashback_usado = 0.00

    def escolher_base(self):
        bases_precos = {'leite': 4.35, 'maracujá': 4.60, 'rosa': 5.85, 'manga': 5.47}
        validacao = 0
        while validacao == 0:
            self.base = input('Digite o número correspondente a base que você deseja: \n[1] Leite: R$4,35 \n[2] Maracujá: R$4,60 \n[3] Rosa: R$5,85 \n[4] Manga: R$5,47\n').lower()
            match self.base:
                case '1':
                    self.base = 'leite'
                case '2':
                    self.base = 'maracujá'
                case '3':
                    self.base = 'rosa'
                case '4':
                    self.base = 'manga'
                case _:
                    print('Opção inválida.')
            try:
                self.preco_total += bases_precos[self.base]
                validacao = 1
            except:
                validacao = 0

    def escolher_adicional(self):
        adicionais_precos = {'boba': 0.50, 'lichia': 0.75, 'geleia': 0.65, 'taro': 1.00, 'chia': 0.35}
        adicionais_numeros = {'1': 'boba', '2': 'lichia', '3': 'geleia', '4': 'taro', '5': 'chia'}
        acao_pa = 0
        while acao_pa == 0:
            add = input('Digite o número correspondente ao adicionnal que deseja: \n(Só pode ser escolhido um adiconal de cada): \n[1] Boba: R$0,50 \n[2] Lichia: R$0,75 \n[3] Geleia: R$0,65 \n[4] Taro: R$1,00 \n[5] Chia: R$0,35\n').lower()
            if adicionais_numeros.get(add) in adicionais_precos:
                if add in self.adicionais:
                    print('Você não pode repetir o adicional!')
                    acao_pa = 0
                else:
                    match add:
                        case '1':
                            self.adicionais.append('boba')
                        case '2':
                            self.adicionais.append('lichia')
                        case '3':
                            self.adicionais.append('geleia')
                        case '4':
                            self.adicionais.append('taro')
                        case '5':
                            self.adicionais.append('chia')
                        case _:
                            print('Erro.')
                    self.preco_total += adicionais_precos[adicionais_numeros.get(add)]
                    continuar = input('\nDigite [1] caso queira colocar outros adicionais. \nDigite qualquer outra coisa para continuar a compra.\n')
                    if continuar != '1':
                            acao_pa = 1
                    else:
                            acao_pa = 0
            else:
                print('Opção inválida.')
                acao_pa = 0
    
    def verificar_desconto(self, categoria):
        if categoria == 'estudante':
            self.preco_final = round(self.preco_total * 0.75, 2)
            self.desconto = 'estudante'
        elif categoria == 'professor' or categoria == 'funcionário' or categoria == 'professora' or categoria == 'funcionária':
            self.preco_final = self.preco_total - 1
            self.desconto = 'professor ou funcionário'
        else:
            self.preco_final = self.preco_total

    def escolher_cashback(self, cliente):
        print('Valor do pedido: ', self.preco_final,'Cashback na conta: R$', cliente.cashback)
        validacao = 0
        while validacao == 0:
            n = input('Deseja usar cashback?\nDigite [1] para usar ou [2] para não usar\n').lower()
            if n == '1':
                if cliente.cashback == 0:
                    print('O cliente não tem cashback.')
                else:
                    if self.preco_final >= cliente.cashback:
                        self.preco_final = round(self.preco_final - cliente.cashback, 2)
                        self.cashback_usado = cliente.cashback
                        cliente.cashback = 0.00
                        validacao = 1
                    elif cliente.cashback > self.preco_final:
                        cliente.cashback = round(cliente.cashback - self.preco_final, 2)
                        self.cashback_usado = self.preco_final
                        self.preco_final = 0.00
                        validacao = 1
            elif n == '2':
                self.cashback_usado = 0.00
                validacao = 1
            else:
                print('Opcção invpalida.')
                validacao = 0
        #Adicionando cashback da compra atual
        cliente.cashback = cliente.cashback + round(self.preco_final*0.1, 2)
        

    
def resumo_pedido(pedido, cliente):
    print('RESUMO DO PEDIDO:')
    print('Cliente: ', cliente.nome)
    print('Base: ', pedido.base)
    print('Adicionais: ', ', '.join(pedido.adicionais))
    if pedido.desconto != None:
        print('Cliente com desconto de', pedido.desconto)
    print('Valor total: R$', pedido.preco_final)
    if pedido.cashback_usado == 0:
        print('Cashback não utilizado.')
    elif pedido.cashback_usado == None:
        print('ERRO!')
    else:
        print('Cashback usado: R$', pedido.cashback_usado)
    print('Saldo de cashback atual: R$', cliente.cashback)

def registro_pedido(pedido, cliente):
    arquivo = 'historico_pedidos.csv'
    try:
     with open(arquivo) as file:
          data_registro = file.readlines()
    except:
        with open(arquivo, mode='w') as file:
            file.write('Cliente;Ocupação;Cashback;Preço_total;Base;Adicionais;Cashback_usado;Preço_final\n')
        with open(arquivo) as file:
            data_registro = file.readlines()
    pedido.cashback_usado = str(pedido.cashback_usado)
    data_registro.append(cliente.nome + ';' + cliente.categoria+';'+cliente.cashback+';'+str(pedido.preco_total)+';'+str(pedido.base)+';'+pedido.adicionais+';'+str(pedido.cashback_usado)+';'+str(pedido.preco_final)+'\n')
    registro = str()
    
    for i in range(data_registro):
        registro += data_registro[i]
    
    with open(arquivo, mode='w') as file:
        file.write(registro)