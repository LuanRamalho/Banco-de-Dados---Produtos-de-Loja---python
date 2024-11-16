import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Nome do arquivo JSON para armazenamento de dados
db_filename = 'loja_produtos.json'

# Função para salvar produtos no banco de dados JSON
def save_products_to_db(products):
    with open(db_filename, 'w') as db_file:
        json.dump(products, db_file)

# Função para carregar produtos do banco de dados JSON
def load_products_from_db():
    if os.path.exists(db_filename):
        with open(db_filename, 'r') as db_file:
            return json.load(db_file)
    return []

# Função para adicionar um produto à tabela
def add_product():
    name = entry_name.get()
    try:
        price = round(float(entry_price.get()), 2)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um preço válido.")
        return

    if name and price >= 0:
        products.append({'name': name, 'price': price})
        save_products_to_db(products)
        update_product_table()
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Por favor, insira nome e preço do produto.")

# Função para atualizar a tabela de produtos
def update_product_table(search_term=""):
    for row in table.get_children():
        table.delete(row)

    for index, product in enumerate(products):
        if search_term.lower() in product['name'].lower() or search_term in f"{product['price']:.2f}":
            table.insert("", "end", values=(product['name'], f"R$ {product['price']:.2f}", index))

# Função para editar um produto
def edit_product():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Seleção necessária", "Por favor, selecione um produto para editar.")
        return
    
    item_index = int(table.item(selected_item)['values'][2])
    product = products[item_index]
    new_name = entry_name.get()
    try:
        new_price = round(float(entry_price.get()), 2)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um preço válido.")
        return

    if new_name:
        product['name'] = new_name
        product['price'] = new_price
        save_products_to_db(products)
        update_product_table()
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Por favor, insira o nome do produto.")

# Função para excluir um produto
def delete_product():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Seleção necessária", "Por favor, selecione um produto para excluir.")
        return
    
    item_index = int(table.item(selected_item)['values'][2])
    products.pop(item_index)
    save_products_to_db(products)
    update_product_table()

# Função para buscar produtos na tabela
def search_products(event=None):
    search_term = entry_search.get()
    update_product_table(search_term)

# Configuração da janela principal
app = tk.Tk()
app.title("Loja de Produtos")
app.geometry("600x500")
app.configure(bg="#e0f7fa")

# Título principal
title = tk.Label(app, text="Loja de Produtos", font=("Segoe UI", 18, "bold"), bg="#e0f7fa", fg="#00796b")
title.pack(pady=10)

# Seção de entrada para adicionar produtos
frame_add = tk.Frame(app, bg="#ffffff", padx=20, pady=20)
frame_add.pack(fill="x", pady=(0, 20))

label_name = tk.Label(frame_add, text="Nome do Produto:", font=("Segoe UI", 12), bg="#ffffff", fg="#00796b")
label_name.grid(row=0, column=0, sticky="e", pady=5)
entry_name = tk.Entry(frame_add, font=("Segoe UI", 12), width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

label_price = tk.Label(frame_add, text="Preço do Produto (R$):", font=("Segoe UI", 12), bg="#ffffff", fg="#00796b")
label_price.grid(row=1, column=0, sticky="e", pady=5)
entry_price = tk.Entry(frame_add, font=("Segoe UI", 12), width=30)
entry_price.grid(row=1, column=1, padx=10, pady=5)

btn_add = tk.Button(frame_add, text="Adicionar Produto", command=add_product, bg="#ff5722", fg="white", font=("Segoe UI", 12), relief="ridge")
btn_add.grid(row=2, columnspan=2, pady=10)

# Campo de busca
entry_search = tk.Entry(app, font=("Segoe UI", 12), width=40)
entry_search.insert(0, "Buscar por nome ou preço")
entry_search.bind("<KeyRelease>", search_products)
entry_search.pack(pady=10)

# Tabela de produtos
columns = ("Nome do Produto", "Preço (R$)", "Index")
table = ttk.Treeview(app, columns=columns, show="headings", selectmode="browse", height=10)
table.heading("Nome do Produto", text="Nome do Produto")
table.heading("Preço (R$)", text="Preço (R$)")
table.column("Index", width=0, stretch=False)  # Coluna oculta para índice

table.pack(fill="both", padx=20)
for heading in columns[:-1]:
    table.heading(heading, text=heading)

# Botões de edição e exclusão
frame_actions = tk.Frame(app, bg="#e0f7fa")
frame_actions.pack(fill="x", pady=10)

btn_edit = tk.Button(frame_actions, text="Editar Produto", command=edit_product, bg="#ffc107", fg="white", font=("Segoe UI", 12))
btn_edit.pack(side="left", padx=10)

btn_delete = tk.Button(frame_actions, text="Excluir Produto", command=delete_product, bg="#dc3545", fg="white", font=("Segoe UI", 12))
btn_delete.pack(side="right", padx=10)

# Carregar produtos ao iniciar o aplicativo
products = load_products_from_db()
update_product_table()

app.mainloop()
