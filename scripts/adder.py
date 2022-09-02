import json
import utils
from simple_term_menu import TerminalMenu

def update_json(file,amount,id):
    """Função responsável por atualizar ficheiros JSON com novas perguntas"""
    
    ## Parsing do JSON
    jsonFile = open(file, "r") 
    data = json.load(jsonFile) 
    jsonFile.close()

    ## Adicionar novas perguntas
    if amount:
        x='a'
        while x.isnumeric()==False:
            print('\033c')  
            x=input("Numero desejado de perguntas a adicionar: ")
        amount=int(x)-1
    amount+=1

    while amount:
        print('\033c')  
        print('Pergunta: ')
        q=utils.get_multiline()
        print('Resposta: ')
        a=utils.get_multiline()
        print('Exemplo\nInput: ')
        i=utils.get_multiline()
        print('Output: ')
        o=utils.get_multiline()
        d = utils.get_int('Nivel de Dificuldade (1~10): ')
        while d<0 or d>11:
            print('Por favor introduza um valor entre 1 e 10!(inclusive)')
            d = utils.get_int('Nivel de Dificuldade (1~10): ')
        data["Questoes"].append({"Pergunta":q,"Resposta":a,"Exemplo":{"Input":i,"Output":o},"Dificuldade":d})
        data["Total"]+=1
        amount-=1

    ## Guardar nova versão do JSON
    jsonFile = open(file, "w+")
    jsonFile.write(json.dumps(data, indent=2))
    jsonFile.close()

    ## Update de informação global 
    with open("data/data.json", "r") as read_file:
        gdata = json.load(read_file)
    ((gdata["Languages"])[id])["Total"]=data["Total"];
    jsongdata = open("data/data.json", "w+")
    jsongdata.write(json.dumps(gdata, indent=2))
    jsongdata.close()

def menu_ql():
    """Menu Questoes"""

    ## Parsing de dados locais
    with open("data/data.json", "r") as read_file:
        data = json.load(read_file)
    options = []
    flist = []
    total=0
    for l in data["Languages"]:
        options.append("["+l["Alias"]+"] "+l["Name"])
        flist.append(l["Path"])
        total=total+1
    options.append("[s] Sair")

    while True:
        
        ## Menu Linguagens
        terminal_menu = TerminalMenu(options, title="Linguagem")
        menu_entry_index = terminal_menu.show()
        if (menu_entry_index==total):
            return
        
        ## Menu Tamanho 
        amount = ["[a] 1 Questao", "[b] Varias", "[s] Sair"]
        amount_menu = TerminalMenu(amount, title="Quantidade")
        amount_entry_index = amount_menu.show()
        if (amount_entry_index==2):
            return
       
        ## Update Used JSON
        update_json(flist[menu_entry_index], amount_entry_index, menu_entry_index)

        ## Clear screen
        print('\033c')  

def menu_qp():
    """Menu Questoes"""

    ## Parsing de dados locais
    with open("data/data.json", "r") as read_file:
        data = json.load(read_file)
    options = []
    flist = []
    total=0
    for l in data["Presets"]:
        options.append("["+l["Alias"]+"] "+l["Name"])
        flist.append(l["Path"])
        total=total+1
    options.append("[s] Sair")

    while True:

        ## Menu Linguagens
        terminal_menu = TerminalMenu(options, title="Presets")
        menu_entry_index = terminal_menu.show()
        if (menu_entry_index == total):
            return

        ## Menu Tamanho
        amount = ["[a] 1 Questao", "[b] Varias", "[s] Sair"]
        amount_menu = TerminalMenu(amount, title="Quantidade")
        amount_entry_index = amount_menu.show()
        if (amount_entry_index == 2):
            return

        ## Update Used JSON
        update_json(flist[menu_entry_index],
                    amount_entry_index, menu_entry_index)

        ## Clear screen
        print('\033c')

def menu_l():
    """Menu Linguagens"""

    ## Parsing de dados locais
    with open("data/data.json", "r") as read_file:
        data = json.load(read_file)
    langs = []
    aliases = ['s']
    for l in data["Languages"]:
        langs.append((l["Name"]).lower())
        aliases.append(l["Alias"])

    ## Get New Language
    while True:
        l = input("Nome da nova linguagem a adicionar: ")
        if l.lower() in langs:
            print("Linguage ja existente! Tente novamente!")
        else:
            while True:
                a=(input("Novo alias para linguagem: ")).lower()
                if a in aliases:
                    print("Alias ja existente! Tente novamente!")
                elif len(a)!=1:
                    print("O alias apenas deve conter um caracter!")
                else:
                    break
            break
    
    ## Create file for new language
    new_path = "data/languages/"+l.lower()+".json"
    jsonl = open(new_path, "w+")
    jsonl.write("{\n  \"Questoes\": [],\n  \"Total\": 0\n}")
    jsonl.close()

    ## Add new language to global data file
    data["Languages"].append({"Name":l,"Alias":a,"Path":new_path,"Total":0})
    jsonFile = open("data/data.json", "w+")
    jsonFile.write(json.dumps(data, indent=2))
    jsonFile.close()

def menu_p():
    """Menu Presets"""

    ## Parsing de dados locais
    with open("data/data.json", "r") as read_file:
        data = json.load(read_file)
    langs = []
    aliases = ['s']
    for l in data["Presets"]:
        langs.append((l["Name"]).lower())
        aliases.append(l["Alias"])

    ## Get New Language
    while True:
        l = input("Nome do novo Preset: ")
        if l.lower() in langs:
            print("Nome ja existente! Tente novamente!")
        else:
            while True:
                a = (input("Novo alias para preset: ")).lower()
                if a in aliases:
                    print("Alias ja existente! Tente novamente!")
                elif len(a) != 1:
                    print("O alias apenas deve conter um caracter!")
                else:
                    break
            break

    am = utils.get_int('Numero de perguntas por teste: ')

    ## Create file for new language
    new_path = "data/presets/"+l.lower()+".json"
    jsonl = open(new_path, "w+")
    jsonl.write("{\n  \"Questoes\": [],\n  \"Total\": 0\n}")
    jsonl.close()

    ## Add new language to global data file
    data["Languages"].append({"Name": l, "Alias": a, "Path": new_path, "Total": 0, "Amount": am})
    jsonFile = open("data/data.json", "w+")
    jsonFile.write(json.dumps(data, indent=2))
    jsonFile.close()

def menu():
    """Menu Principal"""
    while True:
        options = ["[1] Adicionar Questoes a Linguagem", "[2] Adicionar Questoes a Preset",
                   "[3] Adicionar Linguagens", "[4] Criar Preset", "[0] Sair"]
        terminal_menu = TerminalMenu(options, title="Menu")
        menu_entry_index = terminal_menu.show()
        if (menu_entry_index == 0):
            menu_ql()
        elif (menu_entry_index == 0):
            menu_qp()
        elif (menu_entry_index == 2):
            menu_l()
        elif (menu_entry_index == 3):
            menu_p()
        elif (menu_entry_index == 4):
            quit()

        ## Clear screen
        print('\033c')

def main():
    """Função de inicio"""
    print('\033c')  #cls
    menu()

if __name__ == "__main__":
    main()
