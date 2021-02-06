import pandas as pd

from datetime import datetime, date, timedelta

import sqlite3

import csv
import os
import re


# Diretorio dos arquivos sql
dir_sql = 'sql'

format_csv = '.csv'

# Trata e salva os dados em csv's
class SoftG4():        

    def extract_csv(self, dir_conversas):

        self.data_frame = []

        def filtrar(arg):

            # Separa apenas as informações desejadas
            data = re.findall(r"\d+/\d+/\d+", arg)

            hora = re.findall(r"\d+\:\d+", arg)
            valor = re.findall(r"\d+\sreais", arg)
            r = [data, hora, valor]

            if not r[0]:
                r[0] = self.data_frame[-1][0]

            # Remove caracteres indesejados
            try:
                for i, j in enumerate(r):
                    r[i] = j[0].replace(',','[').replace('!',']').replace('.','')
            except Exception as e:
                print('Erro inesperado ao filtrar conversa: ', e)
                return True

            r[2] = "R$"+r[2][:-6]+",00"

            # Incere os dados em uma lista usada pelo Pandas
            self.data_frame.append(r)

        def extrair(file):
            # Abre a conversa e cria uma lista que separa cada linha.
            conversa = open(os.path.join(dir_conversas, file), 'r', 
                encoding = 'utf-8').read().splitlines()

            # Captura o nome que será usado para salvar o arquivo
            nome_csv = os.path.basename(dir_conversas+file)[9:][:-4][25:]

            print("Analisando: ", nome_csv)

            # Filtra apenas as mensagens com G4 MOBILE.
            data_conversa_mobile = [linha for linha in conversa if 'G4 MOBILE:' in linha]

            # Filtra apenas as mensagens com reais.
            data_conversa_reais = [linha for linha in data_conversa_mobile if 'reais' in linha]

            # Estrutura de laço que invoca a função filtrar.
            [filtrar(str(i)) for i in data_conversa_reais]

            nome = os.path.join('data_csv', nome_csv+'.csv')

            print(nome)

            # Cria e salva um DataFrame Pandas em um arquico csv.
            [pd.DataFrame(self.data_frame).to_csv((nome), header=False, encoding='utf-8', index=False)]
            
            #Fecha o DataFrame
            self.data_frame.clear()

        print(dir_conversas)

        [extrair(file) for file in os.listdir(dir_conversas)]

        print()

    def Sql_scripts(self):

        def write_sql_table(arg):
            table = open(os.path.join('sql', "schema_table.sql"), "a")
            schema_ = "CREATE TABLE {} (cod INTEGER PRIMARY KEY, data TEXT NOT NULL, hora INTEGER, valor VARCHAR(11) NOT NULl);\n".format(arg)
            table.write(schema_)

        def write_sql_insert(tb_name, name):

            table = open('sql/'+name+'.sql', "w")

            schema_ = "INSERT INTO {} (data, hora, valor) VALUES (?,?,?)".format(tb_name)

            table.write(schema_)

        def write_sql_search(tb_name):

            table = open(os.path.join('sql', 'SEARCH_'+tb_name+'.sql'), "w")

            schema_ = "SELECT cod, data, hora, valor FROM {} WHERE data=?".format(tb_name)

            table.write(schema_)

        # Para cada .csv em dir_csv aciona loop_dir
        for file in os.listdir('data_csv'):
            nome_csv = os.path.basename(file)[:-4]
            print(nome_csv)

            # Substitui espaços por _ para instanciar dentro do sqlite3
            name = nome_csv.replace(" ", "_")
            print(name)

            # Invoca as funções write
            write_sql_table(name)
            write_sql_insert(name, nome_csv)
            write_sql_search(name)

    def Sql_insert(self):

        # Cria as tabelas coms os scripts .sql
        def create_tables():
            schemas = open(os.path.join('sql', 'schema_table.sql')).read()

            self.db.cursor.executescript(schemas)

        # Incere os dados do csv na respectiva tabela
        def csv_inject(arg):

            # Captura o nome do arquivo

            # Abrir script Sqlite3
            x = open(os.path.join('sql', arg[:-4]+'.sql'), 'r').read()

            # Abrir arquivo csv
            reader = csv.reader(open(os.path.join('data_csv', arg), 'rt'), delimiter=',')

            # Executa os camandos sql instanciando os dados do csv.
            [self.db.cursor.execute(x, linha) for linha in reader]
            self.db.commit_db()

        self.db = Connect()

        create_tables()

        #Looping que chama as funções
        [csv_inject(file) for file in os.listdir('data_csv')]

        self.db.close_db()

    def date_generator(self, data_inicial, data_final):


        data_inicio = datetime.strptime(data_inicial, '%d/%m/%Y').date()

        data_fim = datetime.strptime(data_final, '%d/%m/%Y').date()

        # crio somente 1 timedelta (de 1 dia)
        incremento = timedelta(days=1)

        lista_datas = []
        # vou somando 1 dia na data_inicio, até que ela seja maior que data_fim
        while data_inicio <= data_fim:
            lista_datas.append(data_inicio.strftime('%d/%m/%Y'))
            data_inicio += incremento
        return lista_datas


class Connect():

    def __init__(self):

        try:
            # conectando...
            self.conn = sqlite3.connect('BaseG4.db')
            self.cursor = self.conn.cursor()
        except sqlite3.Error:
            print("Erro ao abrir banco.")
            return False
        
    # Salva modificações na db
    def commit_db(self):
        if self.conn:
            self.conn.commit()

    # Fecha conexão com a base de dados
    def close_db(self):
        if self.conn:
            self.conn.close()
            

