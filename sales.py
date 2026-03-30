import tkinter as tk
from tkinter import messagebox

# ---------------- LOGIN WINDOW ----------------
def login():
    if username_entry.get().strip() == "admin" and password_entry.get().strip() == "admin123":
        login_window.destroy()
        main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

login_window = tk.Tk()
login_window.title("Login | Sales System")
login_window.geometry("380x440")
login_window.configure(bg="#0f172a")
login_window.resizable(False, False)

tk.Label(login_window, text="Welcome Back",
         font=("Segoe UI", 22, "bold"),
         bg="#0f172a", fg="white").pack(pady=(30, 5))

tk.Label(login_window, text="Sales Management System",
         font=("Segoe UI", 11),
         bg="#0f172a", fg="#94a3b8").pack(pady=5)

card = tk.Frame(login_window, bg="#1e293b")
card.pack(padx=30, pady=25, fill=tk.BOTH, expand=True)

tk.Label(card, text="Username",
         bg="#1e293b", fg="white",
         font=("Segoe UI", 10)).pack(pady=(25, 5))
username_entry = tk.Entry(card, font=("Segoe UI", 11))
username_entry.pack(ipady=6, padx=30)

tk.Label(card, text="Password",
         bg="#1e293b", fg="white",
         font=("Segoe UI", 10)).pack(pady=(20, 5))
password_entry = tk.Entry(card, show="*", font=("Segoe UI", 11))
password_entry.pack(ipady=6, padx=30)

tk.Button(card, text="LOGIN",
          bg="#3b82f6", fg="white",
          font=("Segoe UI", 11, "bold"),
          bd=0, cursor="hand2",
          command=login).pack(pady=30, ipadx=30, ipady=8)


# ---------------- MAIN APPLICATION ----------------
def main_app():
   
    global status_label, selected_product
    global entry_customer, entry_quantity, entry_price, search_entry

    products = {
        "Laptop": [],
        "Mobile": [],
        "Tablet": [],
        "Keyboard": [],
        "Headphones": []
    }

    undo_stack = []
    total_sales = {"amount": 0}

    def add_sale():
        product = selected_product.get()
        customer = entry_customer.get().strip()
        qty = entry_quantity.get().strip()
        price = entry_price.get().strip()

        if customer == "" or qty == "" or price == "":
            messagebox.showerror("Error", "All fields required")
            return

        amount = int(qty) * float(price)
        sale = (customer, int(qty), amount)

        products[product].append(sale)
        undo_stack.append((product, sale))
        total_sales["amount"] += amount

        messagebox.showinfo(
            "Sale Added",
            f"Product: {product}\nCustomer: {customer}\nAmount: ₹{amount}"
        )

        status_label.config(text="✔ Sale Added")
        entry_customer.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_price.delete(0, tk.END)

    def view_sales():
        product = selected_product.get()
        sales = products[product]

        if not sales:
            messagebox.showinfo("Sales", f"No sales found for {product}")
            return

        result = f"Sales for {product}:\n\n"
        total = 0

        for s in sales:
            result += f"{s[0]} | Qty:{s[1]} | ₹{s[2]}\n"
            total += s[2]

        result += f"\nTotal {product} Sales: ₹{total}"
        messagebox.showinfo("Sales", result)

    def view_all_sales():
        result = ""
        for product, sales in products.items():
            result += f"{product}\n"
            if sales:
                for s in sales:
                    result += f"  {s[0]} | Qty:{s[1]} | ₹{s[2]}\n"
            else:
                result += "  No sales\n"
            result += "\n"

        result += f"TOTAL SALES: ₹{total_sales['amount']}"
        messagebox.showinfo("All Sales", result)

    def search_customer():
        name = search_entry.get().strip()
        if name == "":
            messagebox.showwarning("Search", "Enter customer name")
            return

        found = False
        result = f"Sales for '{name}':\n\n"

        for product, sales in products.items():
            for s in sales:
                if s[0].lower() == name.lower():
                    result += f"{product} | Qty:{s[1]} | ₹{s[2]}\n"
                    found = True

        if found:
            messagebox.showinfo("Search Result", result)
        else:
            messagebox.showinfo("Search Result", "No record found")

    def undo_sale():
        if not undo_stack:
            messagebox.showwarning("Undo", "Nothing to undo")
            return

        product, sale = undo_stack.pop()
        products[product].remove(sale)
        total_sales["amount"] -= sale[2]

        messagebox.showinfo(
            "Undo Successful",
            f"Product: {product}\nCustomer: {sale[0]}\nQuantity: {sale[1]}\nAmount: ₹{sale[2]}"
        )

    # GUI
    root = tk.Tk()
    root.title("Sales Management System")
    root.geometry("620x680")
    root.configure(bg="#f2f6ff")

    header = tk.Frame(root, bg="#34495e", height=90)
    header.pack(fill=tk.X)

    tk.Label(header, text="Sales Management System",
             font=("Arial", 22, "bold"),
             bg="#34495e", fg="white").pack(pady=20)

    card = tk.Frame(root, bg="white", bd=3, relief=tk.RIDGE)
    card.pack(padx=25, pady=20, fill=tk.BOTH, expand=True)

    form = tk.Frame(card, bg="white")
    form.pack(pady=10)

    tk.Label(form, text="Product").grid(row=0, column=0, pady=5)
    selected_product = tk.StringVar(value="Laptop")
    tk.OptionMenu(form, selected_product, *products.keys()).grid(row=0, column=1)

    tk.Label(form, text="Customer Name").grid(row=1, column=0, pady=5)
    entry_customer = tk.Entry(form)
    entry_customer.grid(row=1, column=1)

    tk.Label(form, text="Quantity").grid(row=2, column=0, pady=5)
    entry_quantity = tk.Entry(form)
    entry_quantity.grid(row=2, column=1)

    tk.Label(form, text="Price").grid(row=3, column=0, pady=5)
    entry_price = tk.Entry(form)
    entry_price.grid(row=3, column=1)

    tk.Button(card, text="Add Sale", width=25, bg="#27ae60", fg="white", command=add_sale).pack(pady=5)
    tk.Button(card, text="View Sales", width=25, bg="#8e44ad", fg="white", command=view_sales).pack(pady=5)
    tk.Button(card, text="View All Sales", width=25, bg="#2980b9", fg="white", command=view_all_sales).pack(pady=5)
    tk.Button(card, text="Undo Sale", width=25, bg="#f39c12", fg="white", command=undo_sale).pack(pady=5)

    tk.Label(card, text="Search by Customer").pack(pady=5)
    search_entry = tk.Entry(card)
    search_entry.pack()
    tk.Button(card, text="Search", command=search_customer).pack(pady=5)

    status_label = tk.Label(root, text="Ready", bg="#f2f6ff", fg="gray")
    status_label.pack(pady=8)

    root.mainloop()

login_window.mainloop()