# main.py
import tkinter as tk
from gui import RoutingSimulatorApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Imposta la dimensione della finestra
    app = RoutingSimulatorApp(root)  # Crea l'istanza dell'app
    root.mainloop()  # Avvia il loop dell'interfaccia grafica