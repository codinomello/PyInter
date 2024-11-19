import sqlite3 as pp
import ctypes
import ttkbootstrap as ttk
from tkinter import Menu, messagebox, Label, Listbox, PhotoImage, END

# janela principal
janela = ttk.Window(themename="darkly")  # tema padrão
janela.title("Sistema de Cadastro")
janela.geometry("500x450")
janela.resizable(True, True)

# função que cria e conecta ao banco de dados
def conectar_banco():
  conexão = pp.connect("ong.db")
  cursor = conexão.cursor()
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS morador (
  ID_morador INTEGER PRIMARY KEY AUTOINCREMENT,
  RG VARCHAR(12) NOT NULL,
  Nome_morador VARCHAR(30) NOT NULL,
  Sobrenome_morador VARCHAR(40),
  Telefone VARCHAR(12),
  Rua VARCHAR(40),
  Numero VARCHAR(5),
  Bairro VARCHAR(25)
  );
  ''')
  conexão.commit()
  conexão.close()

# função para criar a página inicial do sistema
def criar_página(contêiner):
  for widget in contêiner.winfo_children():
    widget.destroy()

  Label(contêiner, text="Sistema de Cadastro", font=("Poppins", 16, "bold")).pack(pady=(40, 10))
  Label(contêiner, text="Bem-vindo ao sistema de cadastro e gestão de moradores.", font=("Poppins", 10)).pack(pady=(0, 5))
  Label(contêiner, text="Escolha uma opção no menu para começar:", font=("Poppins", 10)).pack(pady=(0, 20))

  botão_cadastro = ttk.Button(contêiner, text="Cadastrar Morador", command=lambda: mostrar_tela(criar_tela_cadastro_morador), style="primary.TButton")
  botão_cadastro.pack(pady=(10, 10))

  botão_consulta = ttk.Button(contêiner, text="Consultar Moradores", command=lambda: mostrar_tela(criar_tela_consulta_moradores), style="info.TButton")
  botão_consulta.pack(pady=(20, 10))
  
  Label(contêiner, text="Gabriel Mello", font=("Poppins", 10)).pack(pady=(35, 0))
  Label(contêiner, text="@projetoplamt", font=("Poppins", 10)).pack(pady=(0, 0))

# função para criar a tela de cadastro de morador
def criar_tela_cadastro_morador(contêiner):
  for widget in contêiner.winfo_children():
    widget.destroy()

  Label(contêiner, text="Cadastrar Novo Morador", font=("Poppins", 14, "bold")).grid(row=0, column=0, columnspan=2, padx=(120, 0), pady=(10, 10))

  # campos separados para entradas
  Label(contêiner, text="RG:", font=("Poppins", 10)).grid(row=1, column=0, padx=10, pady=5)
  entrada_rg = ttk.Entry(contêiner, width=30)
  entrada_rg.grid(row=1, column=1, padx=10, pady=5)

  Label(contêiner, text="Nome:", font=("Poppins", 10)).grid(row=2, column=0, padx=10, pady=5)
  entrada_nome = ttk.Entry(contêiner, width=30)
  entrada_nome.grid(row=2, column=1, padx=10, pady=5)

  Label(contêiner, text="Sobrenome:", font=("Poppins", 10)).grid(row=3, column=0, padx=10, pady=5)
  entrada_sobrenome = ttk.Entry(contêiner, width=30)
  entrada_sobrenome.grid(row=3, column=1, padx=10, pady=5)

  Label(contêiner, text="Telefone:", font=("Poppins", 10)).grid(row=4, column=0, padx=10, pady=5)
  entrada_telefone = ttk.Entry(contêiner, width=30)
  entrada_telefone.grid(row=4, column=1, padx=10, pady=5)

  Label(contêiner, text="Rua:", font=("Poppins", 10)).grid(row=5, column=0, padx=10, pady=5)
  entrada_rua = ttk.Entry(contêiner, width=30)
  entrada_rua.grid(row=5, column=1, padx=10, pady=5)

  Label(contêiner, text="Número:", font=("Poppins", 10)).grid(row=6, column=0, padx=10, pady=5)
  entrada_numero = ttk.Entry(contêiner, width=30)
  entrada_numero.grid(row=6, column=1, padx=10, pady=5)

  Label(contêiner, text="Bairro:", font=("Poppins", 10)).grid(row=7, column=0, padx=10, pady=5)
  entrada_bairro = ttk.Entry(contêiner, width=30)
  entrada_bairro.grid(row=7, column=1, padx=10, pady=5)

  # função para inserir morador no banco de dados
  def inserir_morador():
    conexão = pp.connect("ong.db")
    cursor = conexão.cursor()
    cursor.execute('''
    INSERT INTO morador (RG, Nome_morador, Sobrenome_morador, Telefone, Rua, Numero, Bairro)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''',
    (entrada_rg.get(), entrada_nome.get(), entrada_sobrenome.get(), entrada_telefone.get(), entrada_rua.get(), entrada_numero.get(), entrada_bairro.get()))
    conexão.commit()
    conexão.close()

    messagebox.showinfo("Sucesso", "Morador cadastrado com sucesso!")
    # Limpa os campos após cadastro
    entrada_rg.delete(0, END)
    entrada_nome.delete(0, END)
    entrada_sobrenome.delete(0, END)
    entrada_telefone.delete(0, END)
    entrada_rua.delete(0, END)
    entrada_numero.delete(0, END)
    entrada_bairro.delete(0, END)

  ttk.Button(contêiner, text="Cadastrar", command=inserir_morador, style="success.TButton").grid(row=8, column=1, pady=(15, 5))
  ttk.Button(contêiner, text="Voltar para Página Inicial", command=lambda: mostrar_tela(criar_página), style="secondary.TButton").grid(row=9, column=1, pady=(5, 10))

# função para criar a tela de consulta de moradores
def criar_tela_consulta_moradores(contêiner):
  for widget in contêiner.winfo_children():
    widget.destroy()

  Label(contêiner, text="Consulta de Moradores", font=("Poppins", 14, "bold")).pack(pady=(10, 0))

  Label(contêiner, text="Digite o RG do Morador:", font=("Poppins", 10)).pack(pady=5)
  entrada_rg = ttk.Entry(contêiner, width=65)
  entrada_rg.pack(padx=10, pady=10)

  lista_moradores = Listbox(contêiner, width=50, height=7, font=("Poppins", 10))
  lista_moradores.pack(padx=10, pady=10)

  def buscar_por_rg():
    rg = entrada_rg.get().strip()  # remove espaços em branco antes e depois
    lista_moradores.delete(0, END)  # limpa a lista antes de adicionar novos itens
    if rg:
      conexão = pp.connect("ong.db")
      cursor = conexão.cursor()
      cursor.execute("SELECT * FROM morador WHERE RG = ?", (rg,))
      registros = cursor.fetchall()
      conexão.close()
      
      if registros:
        for registro in registros:
          lista_moradores.insert(END, f"ID: {registro[0]}, Nome: {registro[2]} {registro[3]}, Telefone: {registro[4]}, RG: {registro[1]}")
      else:
        messagebox.showinfo("Resultado", "Nenhum morador encontrado com esse RG.")
    else:
      messagebox.showwarning("Aviso", "Por favor, digite um RG válido.")

  ttk.Button(contêiner, text="Buscar por RG", command=buscar_por_rg, style="primary.TButton").pack(pady=(10, 5))
  ttk.Button(contêiner, text="Voltar para Página Inicial", command=lambda: mostrar_tela(criar_página), style="secondary.TButton").pack(pady=(10, 5))

# função para limpar e exibir nova tela
def mostrar_tela(função):
  função(contêiner)

# define o ícone da janela
try:
  janela.iconphoto(False, PhotoImage(file='./image/plamt.png'))
  plamt = 'plamt'  # habilita o ícone na barra de tarefas
  ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(plamt)
except Exception as erro:
  print(f"Erro ao carregar o ícone: {erro}")

# barra de menu
menu_barra = Menu(janela)
janela.config(menu=menu_barra)

# contêiner para as telas
contêiner = ttk.Frame(janela)
contêiner.pack(fill="both", expand=True)

# menu de opções
menu_cadastro = Menu(menu_barra, tearoff=0)
menu_cadastro.add_command(label="Novo Morador", command=lambda: mostrar_tela(criar_tela_cadastro_morador))
menu_barra.add_cascade(label="Cadastro", menu=menu_cadastro)

menu_consulta = Menu(menu_barra, tearoff=0)
menu_consulta.add_command(label="Ver Moradores", command=lambda: mostrar_tela(criar_tela_consulta_moradores))
menu_barra.add_cascade(label="Consulta", menu=menu_consulta)

# inicializa o banco de dados
conectar_banco()

# exibe a página inicial
criar_página(contêiner)

# loop da janela
janela.mainloop()