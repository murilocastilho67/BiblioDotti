import tkinter as tk
from views.main_window import main_window

def iniciar_app():
    # Cria a janela principal
    janela = tk.Tk()
    janela.title("Biblioteca Dotti")
    janela.configure(bg="#f0f0f0")  # Fundo consistente com outras telas

    # Define o tamanho inicial da janela
    largura = 500
    altura = 400

    # Centraliza a janela na tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # Define tamanho mínimo para responsividade
    janela.minsize(400, 300)

    # Configura a janela para ser expansível
    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    # Passa a janela para a função main_window
    main_window(janela)

    # Inicia o loop da interface gráfica
    janela.mainloop()

if __name__ == "__main__":
    iniciar_app()