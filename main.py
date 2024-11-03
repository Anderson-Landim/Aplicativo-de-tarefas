import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage

# Criação da janela principal do aplicativo
janela = tk.Tk()
janela.title("Meu App de Tarefas")  # Define o título da janela
janela.configure(bg="#F0F0F0")  # Define a cor de fundo da janela
janela.geometry("500x600")  # Define o tamanho da janela principal

# Variável para armazenar o frame da tarefa que está sendo editada
frame_em_edicao = None


# Função para adicionar uma tarefa à lista
def adicionar_tarefa():
    global frame_em_edicao
    tarefa = entrada_tarefa.get().strip()  # Obtém o texto da tarefa, removendo espaços extras
    # Verifica se a tarefa não está vazia e se não é o texto padrão
    if tarefa and tarefa != "Escreva sua tarefa aqui":
        # Verifica se uma tarefa está em edição e atualiza o texto, caso positivo
        if frame_em_edicao is not None:
            atualizar_tarefa(tarefa)
            frame_em_edicao = None  # Limpa a variável de edição após atualizar
        else:
            # Adiciona uma nova tarefa à lista
            adicionar_item_tarefa(tarefa)
        entrada_tarefa.delete(0, tk.END)  # Limpa a entrada de texto após adicionar
    else:
        # Exibe um aviso caso a entrada seja inválida
        messagebox.showwarning(
            "Entrada Inválida", "Por favor, insira uma tarefa válida."
        )


# Função que cria um item de tarefa com botões de editar e deletar
def adicionar_item_tarefa(tarefa):
    # Cria um frame para cada tarefa na lista
    frame_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)

    # Cria um rótulo para exibir o texto da tarefa
    label_tarefa = tk.Label(
        frame_tarefa,
        text=tarefa,
        font=("Garamond", 15),
        bg="white",
        width=25,
        height=2,
        anchor="w",
    )
    label_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5)

    # Botão para editar a tarefa
    botao_editar = tk.Button(
        frame_tarefa,
        image=icon_editar,
        command=lambda f=frame_tarefa, l=label_tarefa: preparar_edicao(f, l),
        bg="white",
        relief=tk.FLAT,
    )
    botao_editar.pack(side=tk.RIGHT, padx=5)

    # Botão para deletar a tarefa
    botao_deletar = tk.Button(
        frame_tarefa,
        image=icon_deletar,
        command=lambda f=frame_tarefa: deletar_tarefa(f),
        bg="white",
        relief=tk.FLAT,
    )
    botao_deletar.pack(side=tk.RIGHT, padx=5)

    # Adiciona o frame da tarefa no frame de lista de tarefas
    frame_tarefa.pack(fill=tk.X, padx=5, pady=5)

    # Cria um Checkbutton para marcar a tarefa como concluída
    checkbutton = ttk.Checkbutton(
        frame_tarefa, command=lambda label=label_tarefa: alternar_sublinhado(label)
    )
    checkbutton.pack(side=tk.RIGHT, padx=5)

    # Atualiza a área de rolagem para incluir a nova tarefa
    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# Função para preparar a edição de uma tarefa existente
def preparar_edicao(frame_tarefa, label_tarefa):
    global frame_em_edicao
    frame_em_edicao = frame_tarefa  # Define o frame em edição
    entrada_tarefa.delete(0, tk.END)  # Limpa o campo de entrada
    entrada_tarefa.insert(0, label_tarefa.cget("text"))  # Insere o texto da tarefa atual


# Função para atualizar o texto de uma tarefa em edição
def atualizar_tarefa(nova_tarefa):
    global frame_em_edicao
    # Verifica se o frame de edição ainda existe
    if frame_em_edicao is not None and frame_em_edicao.winfo_exists():
        for widget in frame_em_edicao.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(text=nova_tarefa)  # Atualiza o texto do rótulo
    else:
        print("Erro: frame_em_edicao não existe mais ou foi deletado.")


# Função para deletar uma tarefa da lista
def deletar_tarefa(frame_tarefa):
    frame_tarefa.destroy()  # Remove o frame da tarefa
    canvas_interior.update_idletasks()  # Atualiza a área de rolagem
    canvas.config(scrollregion=canvas.bbox("all"))


# Função para alternar o sublinhado de uma tarefa (indicando conclusão)
def alternar_sublinhado(label):
    fonte_atual = label.cget("font")
    # Alterna entre sublinhado e normal para indicar uma tarefa concluída ou não
    if "overstrike" in fonte_atual:
        nova_fonte = fonte_atual.replace(" overstrike", "")
    else:
        nova_fonte = fonte_atual + " overstrike"
    label.config(font=nova_fonte)


# Função para limpar o texto padrão da entrada quando clicado
def ao_clicar_entrada(event):
    if entrada_tarefa.get() == "Escreva sua tarefa aqui":
        entrada_tarefa.delete(0, tk.END)  # Limpa o texto padrão
        entrada_tarefa.configure(fg="black")  # Muda a cor para o texto ativo


# Função para restaurar o texto padrão se a entrada estiver vazia ao perder o foco
def ao_sair_foco(event):
    if not entrada_tarefa.get().strip():
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.insert(0, "Escreva sua tarefa aqui")
        entrada_tarefa.configure(fg="grey")


# Carregar ícones (assegure-se que os arquivos estão na mesma pasta que o script)
icon_editar = PhotoImage(file="editar.png").subsample(12, 12)  # Ícone de edição
icon_deletar = PhotoImage(file="excluir.png").subsample(12, 12)  # Ícone de exclusão

# Criação de uma fonte para o cabeçalho
fonte_cabecalho = font.Font(family="Garamond", size=24, weight="bold")

# Criação do rótulo de cabeçalho
rotulo_cabecalho = tk.Label(
    janela, text="Meu App de Tarefas", font=fonte_cabecalho, bg="#F0F0F0", fg="#333"
)
rotulo_cabecalho.pack(pady=20)  # Adiciona o cabeçalho à janela principal

# Frame que contém a entrada de tarefas e o botão de adicionar
frame = tk.Frame(janela, bg="#F0F0F0")
frame.pack(pady=10)

# Entrada de texto para o usuário digitar uma nova tarefa
entrada_tarefa = tk.Entry(
    frame, font=("Garamond", 14), relief=tk.FLAT, bg="white", fg="grey", width=30
)
entrada_tarefa.insert(0, "Escreva sua tarefa aqui")  # Texto padrão na entrada
entrada_tarefa.bind("<FocusIn>", ao_clicar_entrada)  # Limpa texto padrão ao focar
entrada_tarefa.bind("<FocusOut>", ao_sair_foco)  # Restaura texto padrão ao perder foco
entrada_tarefa.pack(side=tk.LEFT, padx=10)

# Botão para adicionar uma nova tarefa
botao_adicionar = tk.Button(
    frame,
    text="Adicionar Tarefa",
    command=adicionar_tarefa,
    bg="#4CAF50",
    fg="white",
    height=1,
    width=15,
    font=("Roboto", 11),
    relief=tk.FLAT,
)
botao_adicionar.pack(side=tk.LEFT, padx=10)

# Frame para a lista de tarefas com barra de rolagem
frame_lista_tarefas = tk.Frame(janela, bg="white")
frame_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
canvas = tk.Canvas(frame_lista_tarefas, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Barra de rolagem para a lista de tarefas
scrollbar = ttk.Scrollbar(frame_lista_tarefas, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_interior, anchor="nw")

# Atualiza a região de rolagem quando o frame interior é configurado
canvas_interior.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Inicia o loop principal do Tkinter
janela.mainloop()
