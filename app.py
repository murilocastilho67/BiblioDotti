import tkinter as tk
from views.main_window import main_window  # Importa só a função que monta a janela principal

def iniciar_app():
    # Cria a janela principal
    janela = tk.Tk()
    janela.title("Biblioteca Dotti")

    # Define o tamanho desejado
    largura = 500
    altura = 400

    # Calcula a posição para centralizar a janela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela - largura) // 2
    pos_y = (altura_tela - altura) // 2

    # Define o tamanho e a posição
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # Passa a janela criada para a função main_window
    main_window(janela)

    # Inicia o loop da interface gráfica
    janela.mainloop()

if __name__ == "__main__":
    iniciar_app()
