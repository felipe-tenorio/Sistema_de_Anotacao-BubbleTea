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
        self.cashback_usado = None

    def escolher_base(self):
        bases_precos = {'leite': 4.35, 'maracujá': 4.60, 'rosa': 5.85, 'manga': 5.47}
        validacao = 0
        while validacao == 0:
            self.base = input('Digite qual dessas bases você deseja: \n[Leite: R$4,35] \n[Maracujá: R$4,60] \n[Rosa: R$5,85] \n[Manga: R$5,47]\n').lower()
            try:
                self.preco_total += bases_precos[self.base]
                validacao = 1
            except:
                print('Opção inválida.')
                validacao = 0

    def escolher_adicional(self):
        adicionais_precos = {'boba': 0.50, 'lichia': 0.75, 'geleia': 0.65, 'taro': 1.00, 'chia': 0.35}
        acao_pa = 0
        while acao_pa == 0:
            add = input('Digite qual desses adicionais você deseja (Só pode ser escolhido um adiconal de cada): \n[Boba: R$0,50] \n[Lichia: R$0,75] \n[Geleia: R$0,65] \n[Taro: R$1,00] \n[Chia: R$0,35]\n').lower()
            if add in adicionais_precos:
                if add in self.adicionais:
                    print('Você não pode repetir o adicional!')
                    acao_pa = 0
                else:
                    self.adicionais.append(add)
                    self.preco_total += adicionais_precos[add]
                    continuar = input('Digite [1] caso queira colocar outros adicionais. \nDigite qualquer outra coisa para continuar a compra.\n')
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