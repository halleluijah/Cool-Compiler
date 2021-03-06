import testeLex6 #SE MUDAR A VERSAO DO LEXICO TEM QUE ATUALIZAR AQUI E NO newToken()

def newToken():                     #chama novo token
    tok = testeLex6.retornaToken()  #OBS: Não importa se é em loop ou em recursão, um novo token é sempre novo,
    return tok                      #chamado de qualquer lugar ou a qualquer hora no programa. USE SÓ QUANDO NECESSARIO

def end(t):#Verifica se acabou os tokens
    if not t:
        return True

def error(t, STRING): #Mensagem de erro padrão
    print('Erro: o tipo %s era esperado na linha %d, mas nao apareceu.' % (STRING,t.lineno))

class Node: #Nossa arvore - Arvore genérica, cada nó tem N filhos
    def __init__(self, data, token = None):#O parametro 'token=None' permite "sobrecarga"
        self.data = data
        self.token = token
        self.children = []

    def addChild(self, node):#Adiciona filho à lista de filhos do nó
        self.children.append(node)


def isLeaf(no, t):          #Trata os nós que são folhas
    no2 = Node(t.value,t)   #Não, não escolhemos um jeito bonitinho de ver se era folha. Sabemos quando vai ser pela gramática.
    no.addChild(no2)
    
def inClass(t, tree):#Passando o último token e a raiz da árvore                  
        no = Node('CLASS')  #Essas linhas são bem padrões:                         #Devo criar um método para substituir essas 4 linhas tão comuns
        tree.addChild(no)   #Criamos um no e adiocinamos ele como filho
        isLeaf(no, t)       #Tratamos se forem folhas
        t = newToken()      #Pegamos um novo token
        if((t.type) == 'TYPE'):
            no = Node('TYPE')
            tree.addChild(no)
            isLeaf(no, t)
            t = newToken()
            if(t.type == 'INHERITS'):
                no = Node('INHERITS')
                tree.addChild(no)
                isLeaf(no, t)
                t = newToken()
                if(t.type == 'TYPE'):
                    no = Node('TYPE')
                    tree.addChild(no)
                    isLeaf(no, t)
                    t = newToken()
                else:
                    error(t, 'TYPE') #Erro passando t para pegarmos o número da linha e o que faltava        
            if(t.type == 'CHAVE_E'):
                no = Node('CHAVE_E')
                tree.addChild(no)
                isLeaf(no, t)
                t = newToken()
                if(t.type == 'ID'): #Caso especial - TODO FEATURE começa com ID
                    t = inFeature(t, tree)#chamada para FEATURE - Note que na volta da função o token nao muda, por isso forçamos com o retorno a mudar
                if(t.type == 'CHAVE_D'):
                    no = Node('CHAVE_D')
                    isLeaf(no, t)
                    tree.addChild(no)
                    t = newToken()
                else:
                    error(t, '}')
            else:
                error(t, '{')
        else:
           error(t, 'TYPE')
        if(t.type == 'SEMICOLON'):
            no = Node('SEMICOLON')
            tree.addChild(no)
            isLeaf(no, t)
        else:
            error(t, '; no final da CLASSE')


def inFeature(t, tree):
    isEnd = False #Desnecessario, mas ja estava tarde kkk
    
    while not isEnd:#Enquanto nao for o fim - Lembrar do if(t.type == 'ID'): no final do while
        no = Node('FEATURE')
        tree.addChild(no)#PERCEBA A MALDADE DO TREE, NO E NO2 A PARTIR DESSE PONTO KKKKK
        no2 = Node('ID')
        isLeaf(no2, t)
        no.addChild(no2)#Essa ordem com a linha de cima importa?
        t = newToken()
        if(t.type == 'COLON'): #COLON é :
            no2 = Node('COLON')
            no.addChild(no2)
            isLeaf(no2, t)
            t = newToken()
            if(t.type == 'TYPE'):
                no2 = Node('TYPE')
                no.addChild(no2)
                isLeaf(no2, t)
                t = newToken()
                if(t.type == 'ATRIB'):
                    no2 = Node('ATRIB')
                    no.addChild(no2)
                    isLeaf(no2, t)
                    t = newToken()
                    if(isExp(t)):#Se for verdadeiro, chama inExp
                        t = inExp(t, no)#Provavelmente vai ter que ter um retorno t
                        if(t.type == 'SEMICOLON'):
                            no2 = Node('SEMICOLON')
                            no.addChild(no2)
                            isLeaf(no2, t)
                            t = newToken()
                            if(t.type != 'ID'):
                                break
                        else:
                            error(t, ';')
                    else:
                        error(t, 'EXPRESSÃO')
                if(t.type == 'SEMICOLON'):
                    no2 = Node('SEMICOLON')
                    no.addChild(no2)
                    isLeaf(no2, t)
                    t = newToken()
                    if(t.type != 'ID'):#TA FODA, MAS NOIS E TRETUDO KKK
                        break
                    else:
                        error(t, '}')
                else:
                    error(t, ';')
            else:
                error(t, 'TYPE')    
        else: #Jefferson, quero ver entender esse pedaço! HA HA HA
            if(t.type != 'PAREN_E'):
                error(t, ': ou (')
                break            
            if(t.type == 'PAREN_E'):                
                no2 = Node('PAREN_E')
                no.addChild(no2)
                isLeaf(no2, t)
                t = newToken()
                if(t.type == 'ID'): #Aqui vai começar o FORMAL, por isso verifico se é um 'ID'
                    t = inFormal(t, no)#Provavelmente vai ter que ter um retorno t
                else:
                    if(t.type != 'PAREN_D'):
                        error(t, 'FORMAL do tipo: " ID : TYPE " ou )')
                if(t.type == 'PAREN_D'):
                    no2 = Node('PAREN_D')
                    no.addChild(no2)
                    isLeaf(no2, t)
                    t = newToken()
                    if(t.type == 'COLON'):
                        no2 = Node('COLON')
                        no.addChild(no2)
                        isLeaf(no2, t)
                        t = newToken()
                        if(t.type == 'TYPE'):
                            no2 = Node('TYPE')
                            no.addChild(no2)
                            isLeaf(no2, t)
                            t = newToken()
                            if(t.type == 'CHAVE_E'):
                                no2 = Node('CHAVE_E')
                                no.addChild(no2)
                                isLeaf(no2, t)
                                t = newToken()
                                if(isExp(t)):#Se for verdadeiro, chama inExp
                                    t = inExp(t, no)#Provavelmente vai ter que ter um retorno t
                                    if(t.type == 'CHAVE_D'):
                                        no2 = Node('CHAVE_D')
                                        no.addChild(no2)
                                        isLeaf(no2, t)
                                        t = newToken()
                                        if(t.type == 'SEMICOLON'):
                                            no2 = Node('SEMICOLON')
                                            no.addChild(no2)
                                            isLeaf(no2, t)
                                            t = newToken()
                                            if(t.type != 'ID'):
                                                break
                                        else:
                                            error(t, ';')
                                    else:
                                        error(t, '}')
                                else: #LEMBRAR DE TRATAR '}' ANTES DE SAIR DO inExp()
                                    error(t, 'EXPRESSÃO') 
                            else:
                                error(t, '{')
                                break
                        else:
                            error(t, 'TYPE')
                    else:
                        error(t, ':')
                else:
                    error(t, ')')
    return t
                

def isExp(t): #Método para verificar se um token é ou nao uma expressão - só pode ser usado em pontos específicos [?]
    aux = False
    if(t.type == 'ID'):
        aux = True
    if(t.type == 'IF'):
        aux = True
    if(t.type == 'WHILE'):
        aux = True
    if(t.type == 'CHAVE_E'):
        aux = True
    if(t.type == 'LET'):
        aux = True
    if(t.type == 'CASE'):
        aux = True
    if(t.type == 'NEW'):
        aux = True
    if(t.type == 'ISVOID'):
        aux = True
    if(t.type == 'OP'):
        aux = True
    if(t.type == 'TIL'):
        aux = True
    if(t.type == 'COMP'):
        aux = True
    if(t.type == 'NOT'):
        aux = True
    if(t.type == 'PAREN_E'):
        aux = True
    if(t.type == 'NUMBER'):
        aux = True
    if(t.type == 'STRING'):
        aux = True
    if(t.type == 'TRUE'):
        aux = True
    if(t.type == 'FALSE'):
        aux = True
    return aux
        
       
def inFormal(t, tree):#falta implementar
    while True:
        no = Node('FORMAL')
        tree.addChild(no)
        no2 = Node('ID')
        isLeaf(no2, t)
        no.addChild(no2)
        t = newToken()
        if(t.type == 'COLON'):
            no2 = Node('COLON')
            no.addChild(no2)
            isLeaf(no2, t)
            t = newToken()
            if(t.type == 'TYPE'):
                no2 = Node('TYPE')
                no.addChild(no2)
                isLeaf(no2, t)
                t = newToken()
                if(t.type == 'COMMA'):
                    no2 = Node('COMMA')
                    no.addChild(no2)
                    isLeaf(no2, t)
                    t = newToken()
                    if(t.type != 'ID'):
                        error(t, 'ID')
                        break
                else:
                    if(t.type != 'PAREN_D'):
                        error(t, '" , " ou " ) "')
                        break #Tenho que dar break aqui?
            else:
                error(t, 'TYPE')
        else:
            error(t, ':')
        if(t.type == 'PAREN_D'):
            break
    return t

def inExp(t, tree, t2 = None): #Falta implementar
    # a partir daqui é que começa a inExp
    while True:
        no = Node('EXP')
        tree.addChild(no)
        if(t.type == 'TRUE'):#SE FOR TRUE
            no2 = Node('TRUE')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        if(t.type == 'FALSE'):#SE FOR FALSE
            no2 = Node('FALSE')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        if(t.type == 'STRING'):#SE FOR STRING
            no2 = Node('STRING')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        if(t.type == 'NUMBER'):#SE FOR INTEGER
            no2 = Node('NUMBER')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
        if(t.type == 'NEW'):#SE FOR NEW
            no2 = Node('NEW')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            if(t.type == 'TYPE'):#SE FOR INTEGER
                no2 = Node('TYPE')
                isLeaf(no2, t)
                no.addChild(no2)
                t = newToken()
            else:
                error(t, 'TYPE')
            break
        if(t.type == 'ID'):#SE FOR ID
            no2 = Node('ID')
            isLeaf(no2, t)
            no.addChild(no2)
            t = newToken()
            break
            
    return t #Fim do método retornando t
        
def imprimeArvore(tree):
    for i in tree.children:
        print(i.data)
        imprimeArvore(i)
                      
#Aqui começa o equivalente a Main, vulgo: MEIN INERITS AIOOOOU!!!!!    
aux=0
tree = Node('PROGRAM')
#t1 = newToken()
while True: #loop infinito
    #t2 = newToken() #pega novo token
    t = newToken()#nao tinha o t = newToken() aqui
    if(not end(t)): #enquanto nao chegar ao final dos tokens
        if(not aux): #se for a primeira linha do programa ---- SIM, AINDA NÃO FAZ NADA, MAS VAI FAZER [?] TALVEZ NÃO
            #tree = Node('PROGRAM')
            #tinha o t = newToken() aqui
            if(t.type == 'CLASS'):
                inClass(t,tree)
            else:
                error(t, 'DEU PAU') #Falta escrever um erro bonitinho pra cá
    else: #Se chegou ao fim dos tokens então break pra sair do loop infinito
        break

imprimeArvore(tree)
'''
#Prints para testar
print(tree.data)
for i in tree.children:
    print(i.data)
    for j in i.children:#Sim, isso é necessário
        print(j.data)
        for k in j.children:#Sim, isso tambem!
            print(k.data)
            for l in k.children:#Sim, isso tambem!
                print(l.data)
'''
print("\n\nACABOU !!!")#ACABOU
    
                
