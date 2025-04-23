import tkinter as tk
from views.main_window import main_window  # importando a janela principal


def iniciar_app():
    # Cria a janela principal
    janela = tk.Tk()
    janela.title("Biblioteca Dotti")

    # Aqui você pode inicializar a janela principal
    main_window(janela)

    # Inicia a interface gráfica
    janela.mainloop()


if __name__ == "__main__":
    iniciar_app()
