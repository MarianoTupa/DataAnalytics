from SoftBackend import *
import pathlib
import shutil
from math import ceil
# Tkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkcalendar import Calendar, DateEntry
from datetime import datetime


window = Tk()

class Funcoes():

    def inicializar(self, arg):

        self.SoftG4 = SoftG4()

        self.SoftG4.extract_csv(arg)

        self.SoftG4.Sql_scripts()

        self.SoftG4.Sql_insert()


    def pesquisar(self):

        self.calc_.clear()

        self.listaCli.delete(*self.listaCli.get_children())
        self.Resultado.delete(*self.Resultado.get_children())

        self.data_1 = self.calendar_1.get()
        self.data_2 = self.calendar_2.get()

        nome = self.drop_.get()

        dates = self.SoftG4.date_generator(self.data_1, self.data_2)

        [self.select_tb(nome, date) for date in dates]

        self.calcular_viajens(self.calc_)

    def importar(self):
        origem = filedialog.askdirectory()
        self.inicializar(origem)
        self.menu_moto()

    def create_dirs(self):
        os.mkdir('data_csv')
        os.mkdir('sql') 

    def delete_files(self):
        try:
            shutil.rmtree('data_csv', ignore_errors=False, onerror=None)
        except Exception:
            pass
            
        try:
            shutil.rmtree('sql', ignore_errors=False, onerror=None)
        except Exception:
            pass

        try:
            os.remove('BaseG4.db')
        except Exception:
            pass

class Application(Funcoes):

    def __init__(self):

        self.delete_files()

        self.create_dirs()

        self.calc_ = []

        self.window = window

        self.tela()
        self.menu_topo()
        self.frames_tela()
        self.textos()
        self.menu_moto()
        self.calendario()
        self.botoes()
        self.Treeview_frame_1()
        self.Treeview_frame_2()


        window.mainloop()

        self.delete_files()

    def tela(self):
        self.window.title("Soft G4")
        self.window.configure(background='#1e3743')
        self.window.geometry('800x700')
        self.window.resizable(True, True)
        self.window.maxsize(width=800, height=600)
        self.window.minsize(width=500, height=400)

    def menu_topo(self):

        menubar = Menu(self.window, tearoff=0)

        self.window.config(menu=menubar)

        menu_arquivos = Menu(menubar, tearoff=0)
        menu_ajuda = Menu(menubar, tearoff=0)

        menu_arquivos.add_command(label="Importar", command=self.importar)
        menu_arquivos.add_command(label="Exportar", command=None)
        menu_arquivos.add_command(label="sair", command=None)

        menubar.add_cascade(label="Arquivo", menu=menu_arquivos)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

    def frames_tela(self):

        self.frame_1 = Frame(self.window, bd=4, bg='#dfe3ee',
            highlightbackground='#759fe6', highlightthickness=3)

        self.frame_2 = Frame(self.window, bd=4, bg='#dfe3ee',
            highlightbackground='#759fe6', highlightthickness=3)

        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96,relheight=0.46)

        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def menu_moto(self):

        def list_moto():
            list_ = [""]
            arquivos = os.listdir('data_csv/')
            [list_.append(str(i)[:-4].replace(" ", "_")) for i in arquivos]
            return list_

        self.options_menu_moto = list_moto()

        self.drop_ = StringVar()

        self.drop_.set("MOTORISTA")

        self.drop = OptionMenu(self.frame_1, self.drop_, *self.options_menu_moto)

        self.drop.place(relx=0.05, rely = 0.1, relwidth = 0.40, relheight = 0.15)

    def calendario(self):
        
        # Criando calendario
        self.calendar_1 = DateEntry(self.frame_1, width=12, background='#3D51C3', foreground='white', 
            borderwidth=2, font="Arial 12", selectmode='day', cursor="hand1", year=2021, month=1, day=31, date_pattern='dd/mm/Y')

        self.calendar_2 = DateEntry(self.frame_1, width=12, background='#3D51C3',foreground='white', 
            borderwidth=2, font="Arial 12", selectmode='day', cursor="hand1", year=2021, month=2, day=7, date_pattern='dd/mm/Y')

        self.calendar_1.place(relx=0.05, rely=0.35, relwidth=0.19, relheight=0.1)

        self.calendar_2.place(relx=0.26, rely=0.35, relwidth=0.19, relheight=0.1)

    def botoes(self):

        self.bt_pesquisar = Button(self.frame_1, text="PESQUISAR", bd=2, 
            bg='#364094', fg='white', font=('verdana', 10, 'bold'), command=self.pesquisar)

        self.bt_export_pdf = Button(self.frame_1, text="EXPORTAR PDF", bd=2, 
            bg='#364094', fg='white', font=('verdana', 8, 'bold'), command=None)

        self.bt_exportar_todos = Button(self.frame_1, text="EXPORTAR TUDO", bd=2, 
            bg='#D92A2A', fg='white', font=('verdana', 8, 'bold'), command=self.gerar_analise)

        self.bt_pesquisar.place(relx=0.05, rely=0.5, relwidth=0.4, relheight=0.2)

        self.bt_export_pdf.place(relx=0.05, rely=0.725, relwidth=0.19, relheight=0.15)

        self.bt_exportar_todos.place(relx=0.26, rely=0.725, relwidth=0.19, relheight=0.15)

    def textos(self):

        self.lb_motorista = Label(self.frame_1, text="Escolha o motorista: ", bg='#dfe3ee', font=('Arial', 10, 'bold'))

        self.lb_resultado = Label(self.frame_1, text="Analise dos resultados", bg='#dfe3ee', font=('Arial', 10, 'bold'))

        self.lb_data_inicial = Label(self.frame_1, text = "Data inicial:", bg = '#dfe3ee')

        self.lb_data_final = Label(self.frame_1, text = "Data final:", bg = '#dfe3ee')


        self.lb_motorista.place(relx=0.05, rely=0.005)

        self.lb_resultado.place(relx=0.5, rely=0.005)

        self.lb_data_inicial.place(relx = 0.05, rely = 0.27)

        self.lb_data_final.place(relx = 0.26, rely = 0.27)

    def Treeview_frame_1(self):
        self.Resultado = ttk.Treeview(self.frame_1, height=3, 
            column=("coll1", "coll2", "coll3", "coll4"))

        self.scroll_list = Scrollbar(self.frame_1, orient='vertical', command=self.Resultado.yview)
        self.Resultado.configure(yscrollcommand=self.scroll_list.set)

        self.Resultado.heading("#0", text="")
        self.Resultado.heading("#1", text="Valores")
        self.Resultado.heading("#2", text="N° de viajens")
        self.Resultado.heading("#3", text="Total")
        self.Resultado.heading("#4", text="Porcentagens")

        self.Resultado.column("#0", width=0)
        self.Resultado.column("#1", width=50)
        self.Resultado.column("#2", width=50)
        self.Resultado.column("#3", width=75)
        self.Resultado.column("#4", width=75)
        
        self.Resultado.place(relx=0.50, rely=0.1, relwidth=0.435, relheight=0.85)
        self.scroll_list.place(relx=0.93, rely=0.1, relwidth=0.025, relheight=0.85)

    def Treeview_frame_2(self):

        self.listaCli = ttk.Treeview(self.frame_2, height=3, 
            column=("coll1", "coll2", "coll3", "coll4"))

        self.scroll_list = Scrollbar(self.frame_2, orient='vertical', command=self.listaCli.yview)

        self.listaCli.configure(yscrollcommand=self.scroll_list.set)

        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="cod")
        self.listaCli.heading("#2", text="data")
        self.listaCli.heading("#3", text="hora")
        self.listaCli.heading("#4", text="valor")

        self.listaCli.column("#0", width=0)
        self.listaCli.column("#1", width=10)
        self.listaCli.column("#2", width=45)
        self.listaCli.column("#3", width=45)
        self.listaCli.column("#4", width=45)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroll_list.place(relx=0.96, rely=0.1, relwidth=0.03, relheight=0.85)





