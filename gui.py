# gui.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from node import Node
from routing_table import RoutingTableManager


class RoutingSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distance Vector Routing Simulator")

        self.nodes = []
        self.node_positions = {}
        self.selected_node = None
        self.zoom_level = 1.0

        self.routing_table_manager = RoutingTableManager(self.nodes)  # Manager per le tabelle di routing

        # GUI Layout
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white", scrollregion=(0, 0, 2000, 2000))
        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.canvas.config(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")

        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X)

        tk.Button(self.control_frame, text="Add Node", command=self.add_node).pack(side=tk.LEFT, padx=10)
        tk.Button(self.control_frame, text="Add Link", command=self.add_link).pack(side=tk.LEFT, padx=10)
        tk.Button(self.control_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=10)


        # Mouse Events
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Button-3>", self.show_routing_table)
        self.canvas.bind("<Button-2>", self.show_routing_table)

        self.canvas.bind("<Double-1>", self.rename_node)

    def add_node(self):
        name = f"Node {len(self.nodes) + 1}"
        node = Node(name)
        self.nodes.append(node)
        x, y = 100 + len(self.nodes) * 50, 200
        self.node_positions[node] = (x, y)

        # Aggiornare automaticamente le tabelle di routing
        self.routing_table_manager.update_routing_tables()
        self.draw_all()

    def add_link(self):
        if len(self.nodes) < 2:
            messagebox.showwarning("Warning", "Add at least 2 nodes first!")
            return
    
        def on_submit():
            try:
                n1 = nodes_var1.get()
                n2 = nodes_var2.get()
                cost = int(cost_var.get())
    
                # Controllo se il costo è negativo
                if cost < 0:
                    messagebox.showerror("Error", "Cost cannot be negative!")
                    return  # Non eseguire il resto del codice se il costo è negativo
    
                # Trova i nodi corrispondenti
                node1 = next(node for node in self.nodes if node.name == n1)
                node2 = next(node for node in self.nodes if node.name == n2)
    
                # Controllo se esiste già un collegamento tra i due nodi
                if node2 in node1.neighbors or node1 in node2.neighbors:
                    messagebox.showerror("Error", "A link already exists between these nodes!")
                    return
    
                # Aggiungi il collegamento se non esiste già
                node1.add_neighbor(node2, cost)
                node2.add_neighbor(node1, cost)
    
                # Aggiornamento delle tabelle di routing subito dopo aver aggiunto il collegamento
                self.routing_table_manager.update_routing_tables()
    
                # Ridisegnare la scena per includere il nuovo collegamento
                self.draw_all()  
    
                link_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
        link_window = tk.Toplevel(self.root)
        link_window.title("Add Link")
    
        nodes = [node.name for node in self.nodes]
        nodes_var1 = tk.StringVar(value=nodes[0])
        nodes_var2 = tk.StringVar(value=nodes[1])
        cost_var = tk.StringVar(value="1")
    
        tk.Label(link_window, text="Node 1:").grid(row=0, column=0)
        tk.OptionMenu(link_window, nodes_var1, *nodes).grid(row=0, column=1)
    
        tk.Label(link_window, text="Node 2:").grid(row=1, column=0)
        tk.OptionMenu(link_window, nodes_var2, *nodes).grid(row=1, column=1)
    
        tk.Label(link_window, text="Cost:").grid(row=2, column=0)
        tk.Entry(link_window, textvariable=cost_var).grid(row=2, column=1)
    
        tk.Button(link_window, text="Add Link", command=on_submit).grid(row=3, column=0, columnspan=2)
        self.routing_table_manager.update_routing_tables()

        # Ridisegnare la scena per includere il nuovo collegamento
        self.draw_all()  
    
    def reset(self):
        self.nodes = []
        self.node_positions = {}
        self.selected_node = None
        self.canvas.delete("all")

    def draw_all(self):
        self.canvas.delete("all")  # Cancella tutto dalla tela
        self.draw_links()          # Disegna tutti i collegamenti
        self.draw_nodes()          # Disegna tutti i nodi


    def draw_nodes(self):
        for node, (x, y) in self.node_positions.items():
            x, y = int(x), int(y)
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue", tags=f"node_{node.name}")
            self.canvas.create_text(x, y, text=node.name, tags=f"node_{node.name}")

    def draw_links(self):
     drawn_links = set()  # Per tenere traccia dei collegamenti già disegnati
     for node, (x1, y1) in self.node_positions.items():
         for neighbor, cost in node.neighbors.items():
             link = (node.name, neighbor.name)  # Identifica il collegamento
             if link not in drawn_links and (neighbor.name, node.name) not in drawn_links:
                 x1, y1 = int(x1), int(y1)
                 x2, y2 = int(self.node_positions[neighbor][0]), int(self.node_positions[neighbor][1])
 
                 line_width = 2
                
                 # Disegna il collegamento con la larghezza della linea variabile
                 line = self.canvas.create_line(x1, y1, x2, y2, fill="black", width=line_width)
                 self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(cost), fill="black")
                 drawn_links.add(link)
                 self.canvas.tag_bind(line, "<Button-1>", lambda event, node=node, neighbor=neighbor: self.on_link_click(event, node, neighbor))

    def on_link_click(self, event, node, neighbor):
        def on_submit():
            try:
                new_cost = int(cost_var.get())
                
                # Verifica se il costo è negativo
                if new_cost < 0:
                    messagebox.showerror("Error", "Cost cannot be negative!")
                    return  # Non eseguire il resto del codice se il costo è negativo
    
                # Modifica il costo del collegamento tra i due nodi
                node.neighbors[neighbor] = new_cost
                neighbor.neighbors[node] = new_cost
    
                # Aggiorna le tabelle di routing subito dopo aver modificato il costo
                self.routing_table_manager.update_routing_tables()
    
                # Ridisegna la rete per riflettere il cambiamento
                self.draw_all()
    
                # Chiudi la finestra di dialogo dopo l'aggiornamento
                link_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
    
        # Crea la finestra per la modifica del collegamento
        link_window = tk.Toplevel(self.root)
        link_window.title(f"Edit Link {node.name} <-> {neighbor.name}")
    
        # Imposta il valore iniziale del campo di input al costo attuale del collegamento
        cost_var = tk.StringVar(value=str(node.neighbors[neighbor]))
    
        # Interfaccia per aggiornare il costo
        #tk.Label(link_window, text="New Cost:").grid(row=0, column=0)
        #tk.Entry(link_window, textvariable=cost_var).grid(row=0, column=1)
    
        #tk.Button(link_window, text="Update", command=lambda: self.update_link(node, neighbor, link_window)).grid(row=1, column=0, columnspan=2)

        # Aggiungi l'opzione per rimuovere il collegamento
        tk.Button(link_window, text="Remove Link", command=lambda: self.remove_link(node, neighbor, link_window)).grid(row=2, column=0, columnspan=2)
    
    def remove_link(self, node, neighbor, link_window):
        node.remove_neighbor(neighbor)
        neighbor.remove_neighbor(node)
        self.routing_table_manager.update_routing_tables()
        self.draw_all()

        link_window.destroy()
        
    def update_link(self, node, neighbor, link_window):
        node.remove_neighbor(neighbor)
        neighbor.remove_neighbor(node)
        self.routing_table_manager.update_routing_tables()
        self.draw_all()

        link_window.destroy()

    def show_routing_table(self, event):
        self.routing_table_manager.update_routing_tables()
        self.draw_all()
        for node, (x, y) in self.node_positions.items():
            if (x - 20 <= event.x <= x + 20) and (y - 20 <= event.y <= y + 20):
                table_window = tk.Toplevel(self.root)
                table_window.title(f"Routing Table: {node.name}")
                tk.Label(table_window, text=node.get_routing_table_str(), justify=tk.LEFT).pack()
                self.draw_all()
                break

    def rename_node(self, event):
        for node, (x, y) in self.node_positions.items():
            if (x - 20 <= event.x <= x + 20) and (y - 20 <= event.y <= y + 20):
                new_name = simpledialog.askstring("Rename Node", "Enter new name:", initialvalue=node.name)
                if new_name and new_name != node.name:
                    node.name = new_name
                    self.draw_all()
                break

    def on_mouse_down(self, event):
        for node, (x, y) in self.node_positions.items():
            x, y = int(x * self.zoom_level), int(y * self.zoom_level)
            if (x - 20 <= event.x <= x + 20) and (y - 20 <= event.y <= y + 20):
                self.selected_node = node
                self.draw_all()
                break

    def on_mouse_drag(self, event):
        if self.selected_node:
            self.node_positions[self.selected_node] = (event.x, event.y)
            self.draw_all()

    def on_mouse_up(self, event):
        self.selected_node = None