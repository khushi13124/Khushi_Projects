import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
import csv  # Added for CSV operations
from PIL import Image, ImageTk

# Function to read products from the file
def read_products():
    products = []
    try:
        with open("supermarket.txt", "r") as file:
            for line in file:
                products.append(line.strip().split(","))
    except FileNotFoundError:
        open("supermarket.txt", "w").close()  # Create the file if it doesn't exist
    return products

# Function to write a new product to the file
def write_product(name, qty, price, image_url):
    with open("supermarket.txt", "a") as file:
        file.write(f"{name},{qty},{price},{image_url}\n")

# Function to update product details in the file
def update_product(product_no, new_qty, new_price):
    products = read_products()
    if product_no <= len(products):
        product = products[product_no - 1]
        product[1] = str(new_qty) if new_qty is not None else product[1]
        product[2] = str(new_price) if new_price is not None else product[2]

        with open("supermarket.txt", "w") as file:
            for p in products:
                file.write(",".join(p) + "\n")
        return True
    return False

# Function to delete a product from the file
def delete_product(product_no):
    products = read_products()
    if product_no <= len(products):
        del products[product_no - 1]
        with open("supermarket.txt", "w") as file:
            for p in products:
                file.write(",".join(p) + "\n")
        return True
    return False

class SupermarketApp:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')
        self.root.resizable(False,False)

        # Set background color to light grey
        self.root.configure(bg='#f0f4f8')  # Light grey

        self.cart = []  # Initialize cart for current session
        self.customer_name = ""
        self.is_admin_logged_in = False  # Track admin login state
        self.show_login_screen()

    def on_button_hover(self, button, event):
        button.config(bg='#0f4173')  # Darker blue on hover

    def on_button_leave(self, button, event):
        button.config(bg='#1f4b80')  # Dark blue

    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command, font=("Arial", 12), bg='#1f4b80', fg='white', activebackground='#0f4173', activeforeground='white')
        button.bind("<Enter>", lambda event: self.on_button_hover(button, event))
        button.bind("<Leave>", lambda event: self.on_button_leave(button, event))
        return button
   
    def show_image(self,path,x,y):
        self.img = Image.open(path)  
        self.img = self.img.resize((x, y))
        self.photo = ImageTk.PhotoImage(self.img)
        return self.photo
   
    def show_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Welcome to Supermarket Management System", font=("Arial", 24), bg='#f0f4f8', fg='#003366').pack(pady=40)
        
        # Create a frame for the grid layout (images + buttons)
        grid_frame = tk.Frame(self.root, bg='#f0f4f8')
        grid_frame.pack()
        
        user_frame= tk.Frame(grid_frame,bg='#f0f4f8')
        user_frame.pack(side=tk.LEFT, fill=tk.Y, padx=80,pady=80)
        
        admin_frame=tk.Frame(grid_frame,bg='#f0f4f8')
        admin_frame.pack(side=tk.RIGHT, fill=tk.Y,padx=80,pady=80)

        # User section
        user_image = Image.open("customer_icon.png")
        user_image = user_image.resize((150, 130))
        self.user_photo = ImageTk.PhotoImage(user_image)
        tk.Label(user_frame, image=self.user_photo, bg='#f0f4f8').grid(row=0, column=0, padx=20, pady=10)
        user_button = self.create_button(user_frame, "Login as User", self.show_user_menu)
        user_button.grid(row=1, column=0, padx=30, pady=20)

        # Admin section
        admin_image = Image.open("admin_icon.png")
        admin_image = admin_image.resize((100, 100))
        self.admin_photo = ImageTk.PhotoImage(admin_image)
        tk.Label(admin_frame, image=self.admin_photo, bg='#f0f4f8').grid(row=0, column=0, padx=20, pady=35)
        admin_button = self.create_button(admin_frame, "Login as Admin", self.show_admin_login)
        admin_button.grid(row=1, column=0, padx=30, pady=0)
        
        exit_button=self.create_button(self.root, "Exit", self.exit)
        exit_button.pack(pady=10,padx=0)
        
    def exit(self):
        self.root.destroy();
        
    def show_admin_login(self):
        self.clear_window()

        tk.Label(self.root, text="Admin Login", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)

        tk.Label(self.root, image=self.show_image('admin_icon.png',100,100), bg='#f0f4f8').pack(pady=10)
        tk.Label(self.root, text="Username:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_password = tk.Entry(self.root, show='*')
        self.entry_password.pack(pady=5)

        # Login button
        login_button = self.create_button(self.root, "Login", self.login_admin)
        login_button.pack(pady=10)

        # Back button
        back_button = self.create_button(self.root, "Back to Main Menu", self.show_login_screen)
        back_button.pack(pady=5)

    def login_admin(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if self.verify_credentials(username, password):
            self.is_admin_logged_in = True  # Login status
            self.show_admin_menu()  # Call the method to show admin menu
        else:
            messagebox.showerror("Login Error", "Invalid credentials")

    def verify_credentials(self, username, password):
        return username == "admin" and password == "admin"

    def show_admin_menu(self):
        if not self.is_admin_logged_in:
            messagebox.showerror("Error", "Please log in first.")
            return
   
        self.clear_window()
   
        #Main frame to hold both columns
        main_frame = tk.Frame(self.root, bg='#f0f4f8')
        main_frame.pack(fill=tk.BOTH, expand=True)
   
        #Left Column for Images and Labels
        left_frame = tk.Frame(main_frame,bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
   
        #Scrollbar for left column
        canvas = tk.Canvas(left_frame,bg='#f0f4f8')
        scrollbar = tk.Scrollbar(left_frame, orient="vertical",command=canvas.yview, bg='#1f4b80')
       
        scrollable_frame = tk.Frame(canvas,bg='#f0f4f8')
   
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
   
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
   
        # Pack the canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
   
        #Grid of images and labels
        products = read_products()
        self.image_references = []
        for i, product in enumerate(products):
            row = i // 5
            col = i % 5
            box_frame = tk.Frame(scrollable_frame, width=250, height=500, bg='white', bd=2, relief=tk.GROOVE)
            box_frame.grid(row=row, column=col, padx=3, pady=3)
   
            # Load image from URL
            img=self.show_image(product[3],185,185)
            self.image_references.append(img)
            img_label = tk.Label(box_frame, image=img, bg='#f0f4f8')
            img_label.pack(pady=0)
            
            tk.Label(box_frame, text=f"Product {i+1}: {product[0]}", font=("Arial", 10),bg='white').pack(pady=0)
            tk.Label(box_frame, text=f"Price: {product[2]} INR", font=("Arial", 10),bg='white').pack(pady=0)
            tk.Label(box_frame, text=f"Quantity: {product[1]}", font=("Arial", 10),bg='white').pack(pady=0)
            tk.Label(box_frame, text=" ",bg='white').pack(pady=0)
   
        # Right Column for Buttons
        right_frame = tk.Frame(main_frame, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=30)
        
        tk.Label(right_frame, text="", bg='#f0f4f8', fg='#003366').pack(pady=3)
        tk.Label(right_frame, text="Admin Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)
        
        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Admin menu buttons
        button_width = 15
        
        # Add Product
        add_product = Image.open("add_stock.png")
        add_product = add_product.resize((40, 40))
        self.addpr_photo = ImageTk.PhotoImage(add_product)
        tk.Label(right_subleft_frame, image=self.addpr_photo, bg='#f0f4f8').grid(row=0, column=0, padx=20, pady=10)
        add_product_button = self.create_button(right_subleft_frame, "Add Product", self.add_product_admin_ui)
        add_product_button.config(width=button_width)
        add_product_button.grid(row=0, column=1, padx=20, pady=10)

        # View Products
        view_image = Image.open("display_stock.png")
        view_image = view_image.resize((40, 40))
        self.viewpr_photo = ImageTk.PhotoImage(view_image)
        tk.Label(right_subleft_frame, image=self.viewpr_photo, bg='#f0f4f8').grid(row=1, column=0, padx=20, pady=10)
        view_products_button = self.create_button(right_subleft_frame, "View Products", self.view_products_admin)
        view_products_button.config(width=button_width)
        view_products_button.grid(row=1, column=1, padx=20, pady=10)
        
        # Update Product
        update_product = Image.open("update_stock.png")
        update_product = update_product.resize((40, 40))
        self.updpr_photo = ImageTk.PhotoImage(update_product)
        tk.Label(right_subleft_frame, image=self.updpr_photo, bg='#f0f4f8').grid(row=2, column=0, padx=20, pady=10)
        update_product_button = self.create_button(right_subleft_frame, "Update Product", self.update_product_admin_ui)
        update_product_button.config(width=button_width)
        update_product_button.grid(row=2, column=1, padx=20, pady=10)
        
        # Delete Product
        del_product = Image.open("delete_stock.png")
        del_product = del_product.resize((40, 40))
        self.del_photo = ImageTk.PhotoImage(del_product)
        tk.Label(right_subleft_frame, image=self.del_photo, bg='#f0f4f8').grid(row=3, column=0, padx=20, pady=10)
        delete_product_button = self.create_button(right_subleft_frame, "Delete Product", self.delete_product_admin_ui)
        delete_product_button.config(width=button_width)
        delete_product_button.grid(row=3, column=1, padx=20, pady=10)
        
        # View Sales
        view_product = Image.open("view_sales.png")
        view_product = view_product.resize((40, 40))
        self.view_photo = ImageTk.PhotoImage(view_product)
        tk.Label(right_subleft_frame, image=self.view_photo, bg='#f0f4f8').grid(row=4, column=0, padx=20, pady=10)
        view_sales_button = self.create_button(right_subleft_frame, "View Sales", self.view_sales)
        view_sales_button.config(width=button_width)
        view_sales_button.grid(row=4, column=1, padx=20, pady=10)
        
        # Log Out
        logout = Image.open("logout.png")
        logout = logout.resize((40, 40))
        self.logout_photo = ImageTk.PhotoImage(logout)
        tk.Label(right_subleft_frame, image=self.logout_photo, bg='#f0f4f8').grid(row=5, column=0, padx=20, pady=10)
        logout_button = self.create_button(right_subleft_frame, "Log Out", self.logout_admin)
        logout_button.config(width=button_width)
        logout_button.grid(row=5, column=1, padx=20, pady=180)

    def logout_admin(self):
        self.is_admin_logged_in = False  # Reset the login state
        self.clear_window()
        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_product_admin_ui(self):
        self.clear_window()
        # Create a frame for the left column
        left_frame = tk.Frame(self.root, bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.Y, expand=False)

        # Create a frame for the right column
        right_frame = tk.Frame(self.root, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10, fill=tk.Y)

        # Create a separator
        separator = ttk.Separator(self.root, orient='vertical')
        separator.pack(side=tk.RIGHT, fill=tk.Y, padx=5)  
        
        # Right Column #
        tk.Label(right_frame, text="Admin Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=(30,30),padx=(15,10))

        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Admin menu buttons
        button_width = 15  

        # Add buttons to right_subleft_frame
        button_data = [
            ("add_stock.png", "Add Product", self.add_product_admin_ui),
            ("display_stock.png", "View Product", self.view_products_admin),
            ("update_stock.png", "Update Product", self.update_product_admin_ui),
            ("delete_stock.png", "Delete Product", self.delete_product_admin_ui),
            ("view_sales.png", "View Sales", self.view_sales)
        ]

        for index, (img_file, text, command) in enumerate(button_data):
            img = Image.open(img_file)
            img = img.resize((40, 40))
            photo = ImageTk.PhotoImage(img)

            tk.Label(right_subleft_frame, image=photo, bg='#f0f4f8').grid(row=index, column=0, padx=20, pady=10, sticky='n')
            button = self.create_button(right_subleft_frame, text, command)
            button.config(width=button_width)
            button.grid(row=index, column=1, padx=20, pady=20, sticky='n')

            # Keep a reference to the photo to prevent garbage collection
            button.photo = photo

        # Centering the content in right column
        for widget in right_subleft_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)
        
        # Log Out
        logout = Image.open("logout.png")
        logout = logout.resize((40, 40))
        self.logout_photo = ImageTk.PhotoImage(logout)
        tk.Label(right_subleft_frame, image=self.logout_photo, bg='#f0f4f8').grid(row=5, column=0, padx=20, pady=(100,180))
        logout_button = self.create_button(right_subleft_frame, "Log Out", self.logout_admin)
        logout_button.config(width=button_width)
        logout_button.grid(row=5, column=1, padx=20, pady=(100,180))
        
        tk.Label(self.root, text="Add Product", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)
   
        tk.Label(self.root, image=self.show_image('add_stock.png',100,100), bg='#f0f4f8').pack(pady=10)
        tk.Label(self.root, text="Product Name:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_product_name = tk.Entry(self.root)
        self.entry_product_name.pack(pady=5)
   
        tk.Label(self.root, text="Quantity:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_product_qty = tk.Entry(self.root)
        self.entry_product_qty.pack(pady=5)
   
        tk.Label(self.root, text="Price (INR):", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_product_price = tk.Entry(self.root)
        self.entry_product_price.pack(pady=5)
   
        tk.Label(self.root, text="Image URL:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_product_image_url = tk.Entry(self.root)
        self.entry_product_image_url.pack(pady=5)
   
        add_button = self.create_button(self.root, "Add Product", self.add_product)
        add_button.pack(pady=10)
   
        back_button = self.create_button(self.root, "Back to Admin Menu", self.show_admin_menu)
        back_button.pack(pady=5)

    def add_product(self):
        name = self.entry_product_name.get()
        qty = self.entry_product_qty.get()
        price = self.entry_product_price.get()
        image_url = self.entry_product_image_url.get()
   
        if name and qty.isdigit() and price.replace('.', '', 1).isdigit() and image_url:
            write_product(name, int(qty), float(price), image_url)
            messagebox.showinfo("Success", "Product added successfully")
            self.show_admin_menu()  # Go back to the admin menu after adding
        else:
            messagebox.showerror("Error", "Please enter valid product details")

    def view_products_admin(self):
        self.clear_window()
        
        left_frame = tk.Frame(self.root, bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.Y, expand=False)
    
        
        right_frame = tk.Frame(self.root, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10, fill=tk.Y)
    
        
        separator = ttk.Separator(self.root, orient='vertical')
        separator.pack(side=tk.RIGHT, fill=tk.Y, padx=5)  
        
        # Right Column #
        tk.Label(right_frame, text="Admin Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=(30,30),padx=(15,10))
    
        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        # Admin menu buttons
        button_width = 15  
    
        # Add buttons to right_subleft_frame
        button_data = [
            ("add_stock.png", "Add Product", self.add_product_admin_ui),
            ("display_stock.png", "View Product", self.view_products_admin),
            ("update_stock.png", "Update Product", self.update_product_admin_ui),
            ("delete_stock.png", "Delete Product", self.delete_product_admin_ui),
            ("view_sales.png", "View Sales", self.view_sales)
        ]
    
        for index, (img_file, text, command) in enumerate(button_data):
            img = Image.open(img_file)
            img = img.resize((40, 40))
            photo = ImageTk.PhotoImage(img)
    
            tk.Label(right_subleft_frame, image=photo, bg='#f0f4f8').grid(row=index, column=0, padx=20, pady=10, sticky='n')
            button = self.create_button(right_subleft_frame, text, command)
            button.config(width=button_width)
            button.grid(row=index, column=1, padx=20, pady=20, sticky='n')
    
            # Keep a reference to the photo to prevent garbage collection
            button.photo = photo
    
        # Centering the content in right column
        for widget in right_subleft_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)
        
        # Log Out
        logout = Image.open("logout.png")
        logout = logout.resize((40, 40))
        self.logout_photo = ImageTk.PhotoImage(logout)
        tk.Label(right_subleft_frame, image=self.logout_photo, bg='#f0f4f8').grid(row=5, column=0, padx=20, pady=(100,180))
        logout_button = self.create_button(right_subleft_frame, "Log Out", self.logout_admin)
        logout_button.config(width=button_width)
        logout_button.grid(row=5, column=1, padx=20, pady=(100,180))

        tk.Label(self.root, text="View Products", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)
        tk.Label(self.root, image=self.show_image('display_stock.png',100,100), bg='#f0f4f8').pack(pady=10)

        products = read_products()

        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a treeview for displaying products
        self.tree = ttk.Treeview(self.root, yscrollcommand=scrollbar.set, show="headings")
        self.tree.pack()

        scrollbar.config(command=self.tree.yview)

        self.tree["columns"] = ("Product No", "Name", "Quantity", "Price (INR)")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Product No", anchor=tk.CENTER, width=100)
        self.tree.column("Name", anchor=tk.CENTER, width=200)
        self.tree.column("Quantity", anchor=tk.CENTER, width=100)
        self.tree.column("Price (INR)", anchor=tk.CENTER, width=100)

        self.tree.heading("#0", text="", anchor=tk.CENTER)
        self.tree.heading("Product No", text="Product No", anchor=tk.CENTER)
        self.tree.heading("Name", text="Product Name", anchor=tk.CENTER)
        self.tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
        self.tree.heading("Price (INR)", text="Price (INR)", anchor=tk.CENTER)

        for index, product in enumerate(products, start=1):
            self.tree.insert("", "end", values=(index, product[0], product[1], product[2]))

        back_button = self.create_button(self.root, "Back to Admin Menu", self.show_admin_menu)
        back_button.pack(pady=10)

    def update_product_admin_ui(self):
        self.clear_window()
        
        left_frame = tk.Frame(self.root, bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.Y, expand=False)
    
        
        right_frame = tk.Frame(self.root, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10, fill=tk.Y)
    
        
        separator = ttk.Separator(self.root, orient='vertical')
        separator.pack(side=tk.RIGHT, fill=tk.Y, padx=5)  
        
        # Right Column 
        tk.Label(right_frame, text="Admin Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=(30,30),padx=(15,10))
    
        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        # Admin menu buttons
        button_width = 15  # Set a fixed width for buttons
    
        # Add buttons to right_subleft_frame
        button_data = [
            ("add_stock.png", "Add Product", self.add_product_admin_ui),
            ("display_stock.png", "View Product", self.view_products_admin),
            ("update_stock.png", "Update Product", self.update_product_admin_ui),
            ("delete_stock.png", "Delete Product", self.delete_product_admin_ui),
            ("view_sales.png", "View Sales", self.view_sales)
        ]
    
        for index, (img_file, text, command) in enumerate(button_data):
            img = Image.open(img_file)
            img = img.resize((40, 40))
            photo = ImageTk.PhotoImage(img)
    
            tk.Label(right_subleft_frame, image=photo, bg='#f0f4f8').grid(row=index, column=0, padx=20, pady=10, sticky='n')
            button = self.create_button(right_subleft_frame, text, command)
            button.config(width=button_width)
            button.grid(row=index, column=1, padx=20, pady=20, sticky='n')
    
            # Keep a reference to the photo to prevent garbage collection
            button.photo = photo
    
        # Centering the content in right column
        for widget in right_subleft_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)
        
        # Log Out
        logout = Image.open("logout.png")
        logout = logout.resize((40, 40))
        self.logout_photo = ImageTk.PhotoImage(logout)
        tk.Label(right_subleft_frame, image=self.logout_photo, bg='#f0f4f8').grid(row=5, column=0, padx=20, pady=(100,180))
        logout_button = self.create_button(right_subleft_frame, "Log Out", self.logout_admin)
        logout_button.config(width=button_width)
        logout_button.grid(row=5, column=1, padx=20, pady=(100,180))

        tk.Label(self.root, text="Update Product", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)

        tk.Label(self.root, image=self.show_image('update_stock.png',100,100), bg='#f0f4f8').pack(pady=10)
        
        tk.Label(self.root, text="Product Number:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_product_no = tk.Entry(self.root)
        self.entry_product_no.pack(pady=5)

        tk.Label(self.root, text="New Quantity:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_new_qty = tk.Entry(self.root)
        self.entry_new_qty.pack(pady=5)

        tk.Label(self.root, text="New Price (INR):", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_new_price = tk.Entry(self.root)
        self.entry_new_price.pack(pady=5)

        update_button = self.create_button(self.root, "Update Product", self.update_product)
        update_button.pack(pady=10)

        back_button = self.create_button(self.root, "Back to Admin Menu", self.show_admin_menu)
        back_button.pack(pady=5)

    def update_product(self):
        product_no = self.entry_product_no.get()
        new_qty = self.entry_new_qty.get()
        new_price = self.entry_new_price.get()

        if product_no.isdigit():
            product_no = int(product_no)
            success = update_product(product_no, int(new_qty) if new_qty.isdigit() else None, float(new_price) if new_price.replace('.', '', 1).isdigit() else None)
            if success:
                messagebox.showinfo("Success", "Product updated successfully")
                self.show_admin_menu()  # Go back to the admin menu after updating
            else:
                messagebox.showerror("Error", "Invalid product number")
        else:
            messagebox.showerror("Error", "Please enter a valid product number")

    def delete_product_admin_ui(self):
        self.clear_window()
        
        left_frame = tk.Frame(self.root, bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.Y, expand=False)
    
        
        right_frame = tk.Frame(self.root, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10, fill=tk.Y)
    
        
        separator = ttk.Separator(self.root, orient='vertical')
        separator.pack(side=tk.RIGHT, fill=tk.Y, padx=5)  
        
        # Right Column #
        tk.Label(right_frame, text="Admin Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=(30,30),padx=(15,10))
    
        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        # Admin menu buttons
        button_width = 15  
    
        # Add buttons to right_subleft_frame
        button_data = [
            ("add_stock.png", "Add Product", self.add_product_admin_ui),
            ("display_stock.png", "View Product", self.view_products_admin),
            ("update_stock.png", "Update Product", self.update_product_admin_ui),
            ("delete_stock.png", "Delete Product", self.delete_product_admin_ui),
            ("view_sales.png", "View Sales", self.view_sales)
        ]
    
        for index, (img_file, text, command) in enumerate(button_data):
            img = Image.open(img_file)
            img = img.resize((40, 40))
            photo = ImageTk.PhotoImage(img)
    
            tk.Label(right_subleft_frame, image=photo, bg='#f0f4f8').grid(row=index, column=0, padx=20, pady=10, sticky='n')
            button = self.create_button(right_subleft_frame, text, command)
            button.config(width=button_width)
            button.grid(row=index, column=1, padx=20, pady=20, sticky='n')
    
            # Keep a reference to the photo to prevent garbage collection
            button.photo = photo
    
        # Centering the content in right column
        for widget in right_subleft_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)
        
        # Log Out
        logout = Image.open("logout.png")
        logout = logout.resize((40, 40))
        self.logout_photo = ImageTk.PhotoImage(logout)
        tk.Label(right_subleft_frame, image=self.logout_photo, bg='#f0f4f8').grid(row=5, column=0, padx=20, pady=(100,180))
        logout_button = self.create_button(right_subleft_frame, "Log Out", self.logout_admin)
        logout_button.config(width=button_width)
        logout_button.grid(row=5, column=1, padx=20, pady=(100,180))

        tk.Label(self.root, text="Delete Product", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)

        tk.Label(self.root, image=self.show_image('delete_stock.png',100,100), bg='#f0f4f8').pack(pady=10)
        
        tk.Label(self.root, text="Product Number:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_delete_product_no = tk.Entry(self.root)
        self.entry_delete_product_no.pack(pady=5)

        delete_button = self.create_button(self.root, "Delete Product", self.delete_product)
        delete_button.pack(pady=10)

        back_button = self.create_button(self.root, "Back to Admin Menu", self.show_admin_menu)
        back_button.pack(pady=5)

    def delete_product(self):
        product_no = self.entry_delete_product_no.get()

        if product_no.isdigit():
            success = delete_product(int(product_no))
            if success:
                messagebox.showinfo("Success", "Product deleted successfully")
                self.show_admin_menu()  # Go back to the admin menu after deleting
            else:
                messagebox.showerror("Error", "Invalid product number")
        else:
            messagebox.showerror("Error", "Please enter a valid product number")

    # User Functions
    def show_user_menu(self):
        self.clear_window()

        tk.Label(self.root, text="User Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)

        tk.Label(self.root, image=self.show_image('customer_icon.png',150,120), bg='#f0f4f8').pack(pady=10)
        
        tk.Label(self.root, text="Enter Customer Name:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_customer_name = tk.Entry(self.root)
        self.entry_customer_name.pack(pady=5)

        proceed_button = self.create_button(self.root, "Proceed", self.proceed_to_shopping)
        proceed_button.pack(pady=10)

        back_button = self.create_button(self.root, "Back to Main Menu", self.show_login_screen)
        back_button.pack(pady=5)

    def proceed_to_shopping(self):
        self.customer_name = self.entry_customer_name.get()

        if self.customer_name:
            self.show_product_menu()  # Show the product menu
        else:
            messagebox.showerror("Error", "Please enter a valid customer name.")

    def show_product_menu(self):
        # Clear the window
        self.clear_window()
       
        main_frame = tk.Frame(self.root, bg='#f0f4f8')
        main_frame.pack(fill=tk.BOTH, expand=True)
   
        # Left Column for Images and Labels
        left_frame = tk.Frame(main_frame, bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
   
        # Scrollable area for the left column
        canvas = tk.Canvas(left_frame, bg='#f0f4f8')
        scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview, bg='#1f4b80')
   
        scrollable_frame = tk.Frame(canvas, bg='#f0f4f8')
   
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
   
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
   
        # Pack the canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
   
        #Grid of images
        products = read_products()
        self.image_references = []  # List to store image references
        for i, product in enumerate(products):
            row = i // 5
            col = i % 5
            box_frame = tk.Frame(scrollable_frame, width=250, height=500, bg='white', bd=2, relief=tk.GROOVE)
            box_frame.grid(row=row, column=col, padx=3, pady=3)
   
            img = self.show_image(product[3], 185, 185)
            self.image_references.append(img)  # Store the reference
            img_label = tk.Label(box_frame, image=img, bg='#f0f4f8')
            img_label.pack(pady=0)
           
            tk.Label(box_frame, text=f"Product {i + 1}: {product[0]}", font=("Arial", 10), bg='white').pack(pady=0)
            tk.Label(box_frame, text=f"Price: {product[2]} INR", font=("Arial", 10), bg='white').pack(pady=0)
            tk.Label(box_frame, text=f"Quantity: {product[1]}", font=("Arial", 10), bg='white').pack(pady=0)
            tk.Label(box_frame, text=" ", bg='white').pack(pady=0)

        # Right Column for Buttons
        right_frame = tk.Frame(main_frame, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=30)
        
        tk.Label(right_frame, text="", bg='#f0f4f8', fg='#003366').pack(pady=3)
        tk.Label(right_frame, text="User Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)
   
        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # User menu buttons
        button_width = 15  
        
        add_bill = Image.open("add_to_bill.png")
        add_bill = add_bill.resize((40, 40))
        self.addb_photo = ImageTk.PhotoImage(add_bill)
        tk.Label(right_subleft_frame, image=self.addb_photo, bg='#f0f4f8').grid(row=0, column=0, padx=20, pady=10)
        add_product_button = self.create_button(right_subleft_frame, "Add Product", self.add_product_ui)
        add_product_button.config(width=button_width)
        add_product_button.grid(row=0, column=1, padx=20, pady=10)
   
        update_bill = Image.open("update_bill.png")
        update_bill = update_bill.resize((40, 40))
        self.updb_photo = ImageTk.PhotoImage(update_bill)
        tk.Label(right_subleft_frame, image=self.updb_photo, bg='#f0f4f8').grid(row=1, column=0, padx=20, pady=10)
        update_product_button = self.create_button(right_subleft_frame, "Update Product", self.update_product_ui)
        update_product_button.config(width=button_width)
        update_product_button.grid(row=1, column=1, padx=20, pady=10)
   
        del_bill = Image.open("delete_from_bill.png")
        del_bill = del_bill.resize((40, 40))
        self.delb_photo = ImageTk.PhotoImage(del_bill)
        tk.Label(right_subleft_frame, image=self.delb_photo, bg='#f0f4f8').grid(row=2, column=0, padx=20, pady=10)
        delete_product_button = self.create_button(right_subleft_frame, "Delete Product", self.delete_product_ui)
        delete_product_button.config(width=button_width)
        delete_product_button.grid(row=2, column=1, padx=20, pady=10)
   
        disp_bill = Image.open("display_bill.png")
        disp_bill = disp_bill.resize((40, 40))
        self.disp_photo = ImageTk.PhotoImage(disp_bill)
        tk.Label(right_subleft_frame, image=self.disp_photo, bg='#f0f4f8').grid(row=3, column=0, padx=20, pady=10)
        view_sales_button = self.create_button(right_subleft_frame, "Display Bill", self.display_bill)
        view_sales_button.config(width=button_width)
        view_sales_button.grid(row=3, column=1, padx=20, pady=10)
   
        back_btn = Image.open("back_icon.png")
        back_btn = back_btn.resize((40, 40))
        self.back_photo = ImageTk.PhotoImage(back_btn)
        tk.Label(right_subleft_frame, image=self.back_photo, bg='#f0f4f8').grid(row=4, column=0, padx=20, pady=(270,10))#@
        back_to_user_button = self.create_button(right_subleft_frame, "Back to User Menu", self.show_user_menu)
        back_to_user_button.config(width=button_width)
        back_to_user_button.grid(row=4, column=1, padx=10, pady=(270,10))

    def add_product_ui(self):
        self.clear_window()
   
        left_frame = tk.Frame(self.root, bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.Y, expand=True)
   
        
        right_frame = tk.Frame(self.root, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10, fill=tk.Y)
   
        
        separator = ttk.Separator(self.root, orient='vertical')
        separator.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
   
        # Left Column
        tk.Label(left_frame, text="Add Product to Bill", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=(30, 10))
   
        tk.Label(left_frame, image=self.show_image('add_to_bill.png', 100, 100), bg='#f0f4f8').pack(pady=(0, 10))
   
        tk.Label(left_frame, text="Product Number:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack(pady=(0, 5))
        self.entry_product_no = tk.Entry(left_frame)
        self.entry_product_no.pack(pady=(0, 5))
   
        tk.Label(left_frame, text="Quantity:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack(pady=(0, 5))
        self.entry_product_qty = tk.Entry(left_frame)
        self.entry_product_qty.pack(pady=(0, 5))
   
        add_button = self.create_button(left_frame, "Add Product", self.add_product_to_bill)
        add_button.pack(pady=(10, 20))
        
        back_button = self.create_button(left_frame, "Back to Product Menu", self.show_product_menu)
        back_button.pack(pady=5)
   
        # Right Column
        tk.Label(right_frame, text="User  Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=(30,30))#@
   
        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')#@
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=(10,10),pady=(10,10))#@
   
        # User menu buttons
        button_width = 15  
   
        # Add buttons to right_subleft_frame
        button_data = [
            ("add_to_bill.png", "Add Product", self.add_product_ui),
            ("update_bill.png", "Update Product", self.update_product_ui),
            ("delete_from_bill.png", "Delete Product", self.delete_product_ui),
            ("display_bill.png", "Display Bill", self.display_bill),
        ]
   
        for index, (img_file, text, command) in enumerate(button_data):
            img = Image.open(img_file)
            img = img.resize((40, 40))
            photo = ImageTk.PhotoImage(img)
   
            tk.Label(right_subleft_frame, image=photo, bg='#f0f4f8').grid(row=index, column=0, padx=20, pady=10, sticky='n')
            button = self.create_button(right_subleft_frame, text, command)
            button.config(width=button_width)
            button.grid(row=index, column=1, padx=20, pady=20, sticky='n')#@
   
            # Keep a reference to the photo to prevent garbage collection
            button.photo = photo
   
        # Centering the content in right column
        for widget in right_subleft_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)
           
        back_btn = Image.open("back_icon.png")
        back_btn = back_btn.resize((40, 40))
        self.back_photo = ImageTk.PhotoImage(back_btn)
        tk.Label(right_subleft_frame, image=self.back_photo, bg='#f0f4f8').grid(row=4, column=0, padx=20, pady=(270,10))#@
        back_to_user_button = self.create_button(right_subleft_frame, "Back to User Menu", self.show_user_menu)
        back_to_user_button.config(width=button_width)
        back_to_user_button.grid(row=4, column=1, padx=10, pady=(270,10))

    def add_product_to_bill(self):
        product_no = self.entry_product_no.get()
        qty = self.entry_product_qty.get()
    
        if product_no.isdigit() and qty.isdigit():
            products = read_products()
            if int(product_no) <= len(products):
                product_name = products[int(product_no) - 1][0]
                available_qty = float(products[int(product_no) - 1][1])  # Assuming quantity is stored as a float
                product_price = float(products[int(product_no) - 1][2])
    
                if float(qty) > available_qty:
                    messagebox.showerror("Error", "Requested quantity exceeds available stock.")
                elif available_qty == 0:
                    messagebox.showerror("Error", "Product is out of stock.")
                else:
                    self.cart.append((product_no, product_name, qty, product_price))
                    messagebox.showinfo("Success", "Product added to bill!")
                    self.show_product_menu()
            else:
                messagebox.showerror("Error", "Product number not found.")
        else:
            messagebox.showerror("Error", "Please enter valid product number and quantity.")
        

    def update_product_ui(self):
        self.clear_window()

        left_frame = tk.Frame(self.root, bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.Y, expand=True)
   
        
        right_frame = tk.Frame(self.root, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10, fill=tk.Y)
   
        
        separator = ttk.Separator(self.root, orient='vertical')
        separator.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
       
        #left Frame
        tk.Label(left_frame, text="Update Product in Bill", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)

        tk.Label(left_frame, image=self.show_image('update_bill.png',100,100), bg='#f0f4f8').pack(pady=10)
       
        tk.Label(left_frame, text="Product Number:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_update_product_no = tk.Entry(left_frame)
        self.entry_update_product_no.pack(pady=5)

        tk.Label(left_frame, text="New Quantity:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_update_product_qty = tk.Entry(left_frame)
        self.entry_update_product_qty.pack(pady=5)

        update_button = self.create_button(left_frame, "Update Product", self.update_product_in_bill)
        update_button.pack(pady=10)

        back_button = self.create_button(left_frame, "Back to Product Menu", self.show_product_menu)
        back_button.pack(pady=5)
       
        #Right Column
        # Right Column
        tk.Label(right_frame, text="User  Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=(30,30))#@
   
        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')#@
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=(10,10),pady=(10,10))#@
   
        # User menu buttons
        button_width = 15  
   
        # Add buttons to right_subleft_frame
        button_data = [
            ("add_to_bill.png", "Add Product", self.add_product_ui),
            ("update_bill.png", "Update Product", self.update_product_ui),
            ("delete_from_bill.png", "Delete Product", self.delete_product_ui),
            ("display_bill.png", "Display Bill", self.display_bill),
        ]
   
        for index, (img_file, text, command) in enumerate(button_data):
            img = Image.open(img_file)
            img = img.resize((40, 40))
            photo = ImageTk.PhotoImage(img)
   
            tk.Label(right_subleft_frame, image=photo, bg='#f0f4f8').grid(row=index, column=0, padx=20, pady=10, sticky='n')
            button = self.create_button(right_subleft_frame, text, command)
            button.config(width=button_width)
            button.grid(row=index, column=1, padx=20, pady=20, sticky='n')#@
   
            # Keep a reference to the photo to prevent garbage collection
            button.photo = photo
   
        # Centering the content in right column
        for widget in right_subleft_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)

        back_btn = Image.open("back_icon.png")
        back_btn = back_btn.resize((40, 40))
        self.back_photo = ImageTk.PhotoImage(back_btn)
        tk.Label(right_subleft_frame, image=self.back_photo, bg='#f0f4f8').grid(row=4, column=0, padx=20, pady=(270,10))#@
        back_to_user_button = self.create_button(right_subleft_frame, "Back to User Menu", self.show_user_menu)
        back_to_user_button.config(width=button_width)
        back_to_user_button.grid(row=4, column=1, padx=10, pady=(270,10))

    def update_product_in_bill(self):
        product_no_to_update = self.entry_update_product_no.get()
        new_qty = self.entry_update_product_qty.get()

        if product_no_to_update.isdigit() and new_qty.isdigit():
            product_no_to_update = int(product_no_to_update)
            found = False

            for idx, item in enumerate(self.cart):
                product_no, product_name, qty, product_price = item
                if int(product_no) == product_no_to_update:
                    self.cart[idx] = (product_no, product_name, new_qty, product_price)
                    found = True
                    break

            if found:
                messagebox.showinfo("Success", "Product updated in bill!")
                self.show_product_menu()
            else:
                messagebox.showerror("Error", "Product number not found in bill.")
        else:
            messagebox.showerror("Error", "Please enter valid product number and quantity.")

    def delete_product_ui(self):
        self.clear_window()
        left_frame = tk.Frame(self.root, bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.Y, expand=True)
   
        
        right_frame = tk.Frame(self.root, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10, fill=tk.Y)
   
        
        separator = ttk.Separator(self.root, orient='vertical')
        separator.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        #Right Column
        # Right Column
        tk.Label(right_frame, text="User  Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=(30,30))#@
   
        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')#@
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=(10,10),pady=(10,10))#@
   
        # User menu buttons
        button_width = 15  
   
        # Add buttons to right_subleft_frame
        button_data = [
            ("add_to_bill.png", "Add Product", self.add_product_ui),
            ("update_bill.png", "Update Product", self.update_product_ui),
            ("delete_from_bill.png", "Delete Product", self.delete_product_ui),
            ("display_bill.png", "Display Bill", self.display_bill),
        ]
   
        for index, (img_file, text, command) in enumerate(button_data):
            img = Image.open(img_file)
            img = img.resize((40, 40))
            photo = ImageTk.PhotoImage(img)
   
            tk.Label(right_subleft_frame, image=photo, bg='#f0f4f8').grid(row=index, column=0, padx=20, pady=10, sticky='n')
            button = self.create_button(right_subleft_frame, text, command)
            button.config(width=button_width)
            button.grid(row=index, column=1, padx=20, pady=20, sticky='n')#@
   
            # Keep a reference to the photo to prevent garbage collection
            button.photo = photo
   
        # Centering the content in right column
        for widget in right_subleft_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)

        back_btn = Image.open("back_icon.png")
        back_btn = back_btn.resize((40, 40))
        self.back_photo = ImageTk.PhotoImage(back_btn)
        tk.Label(right_subleft_frame, image=self.back_photo, bg='#f0f4f8').grid(row=4, column=0, padx=20, pady=(270,10))#@
        back_to_user_button = self.create_button(right_subleft_frame, "Back to User Menu", self.show_user_menu)
        back_to_user_button.config(width=button_width)
        back_to_user_button.grid(row=4, column=1, padx=10, pady=(270,10))
        
        #Left Frame
        tk.Label(left_frame, text="Delete Product from Bill", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=20)

        tk.Label(left_frame, image=self.show_image('delete_from_bill.png',100,100), bg='#f0f4f8').pack(pady=10)
        tk.Label(left_frame, text="Product Number:", font=("Arial", 12), bg='#f0f4f8', fg='#003366').pack()
        self.entry_delete_product_no = tk.Entry(left_frame)
        self.entry_delete_product_no.pack(pady=5)

        delete_button = self.create_button(left_frame, "Delete Product", self.delete_product_from_bill)
        delete_button.pack(pady=10)

        back_button = self.create_button(left_frame, "Back to Product Menu", self.show_product_menu)
        back_button.pack(pady=5)

    def delete_product_from_bill(self):
        product_no = self.entry_delete_product_no.get()
        if product_no.isdigit():
            if int(product_no) <= len(self.cart):
                del self.cart[int(product_no) - 1]
                messagebox.showinfo("Success", "Product deleted from bill!")
                self.show_product_menu()
            else:
                messagebox.showerror("Error", "Product number not found in bill.")
        else:
            messagebox.showerror("Error", "Please enter a valid product number.")

    def update_products_after_purchase(self):
        print("Cart contents:", self.cart)  # Debugging line
        products = read_products()
        
        for item in self.cart:
            print("Processing item:", item)  # Debugging line
            product_no,product_name, qty, *rest = item
            print(f"Product: {product_name}, Quantity to reduce: {qty}")  # Debugging
            
            for product in products:
                if product[0].strip().lower() == product_name.strip().lower():  # Match ignoring case and whitespace
                    new_qty = int(product[1]) - int(qty)  # Subtract purchased quantity
                    print(f"Updating {product_name}: Old quantity: {product[1]}, New quantity: {new_qty}")  # Debugging
                    
        with open("supermarket.txt", "w") as file:
            for product in products:
                file.write(",".join(product) + "\n")
            print("File updated successfully.")
        self.show_product_menu()
        
    def display_bill(self):
        self.clear_window()
        left_frame = tk.Frame(self.root, bg='#f0f4f8')
        left_frame.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.Y, expand=True)
   
        
        right_frame = tk.Frame(self.root, bg='#f0f4f8')
        right_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10, fill=tk.Y)
   
        
        separator = ttk.Separator(self.root, orient='vertical')
        separator.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        #Right Column
        # Right Column
        tk.Label(right_frame, text="User  Menu", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=(30,30))#@
   
        right_subleft_frame = tk.Frame(right_frame, bg='#f0f4f8')#@
        right_subleft_frame.pack(fill=tk.BOTH, expand=True, padx=(10,10),pady=(10,10))#@
   
        # User menu buttons
        button_width = 15  
   
        # Add buttons to right_subleft_frame
        button_data = [
            ("add_to_bill.png", "Add Product", self.add_product_ui),
            ("update_bill.png", "Update Product", self.update_product_ui),
            ("delete_from_bill.png", "Delete Product", self.delete_product_ui),
            ("display_bill.png", "Display Bill", self.display_bill),
        ]
   
        for index, (img_file, text, command) in enumerate(button_data):
            img = Image.open(img_file)
            img = img.resize((40, 40))
            photo = ImageTk.PhotoImage(img)
   
            tk.Label(right_subleft_frame, image=photo, bg='#f0f4f8').grid(row=index, column=0, padx=20, pady=10, sticky='n')
            button = self.create_button(right_subleft_frame, text, command)
            button.config(width=button_width)
            button.grid(row=index, column=1, padx=20, pady=20, sticky='n')#@
   
            # Keep a reference to the photo to prevent garbage collection
            button.photo = photo
   
        # Centering the content in right column
        for widget in right_subleft_frame.winfo_children():
            widget.grid_configure(padx=10, pady=10)

        back_btn = Image.open("back_icon.png")
        back_btn = back_btn.resize((40, 40))
        self.back_photo = ImageTk.PhotoImage(back_btn)
        tk.Label(right_subleft_frame, image=self.back_photo, bg='#f0f4f8').grid(row=4, column=0, padx=20, pady=(270,10))#@
        back_to_user_button = self.create_button(right_subleft_frame, "Back to User Menu", self.show_user_menu)
        back_to_user_button.config(width=button_width)
        back_to_user_button.grid(row=4, column=1, padx=10, pady=(270,10))
        
        #left Frame
        # Show bill heading and customer name
        tk.Label(left_frame, text="Bill", font=("Arial", 20), bg='#f0f4f8', fg='#003366').pack(pady=5)
        tk.Label(left_frame, image=self.show_image('display_bill.png',100,100), bg='#f0f4f8').pack(pady=10)
        tk.Label(left_frame, text=self.customer_name, font=("Arial", 16), bg='#f0f4f8', fg='#003366').pack(pady=5)
   
        bill_frame = tk.Frame(left_frame)
        bill_frame.pack(pady=10)
       
        # Create a treeview for displaying the bill
        self.bill_tree = ttk.Treeview(bill_frame, show="headings")
        self.bill_tree.pack()
       
        # Define the columns including Product No
        self.bill_tree["columns"] = ("Product No", "Product Name", "Quantity", "Price (INR)", "Total (INR)")
        self.bill_tree.column("#0", width=0, stretch=tk.NO)
        self.bill_tree.column("Product No", anchor=tk.CENTER, width=100)
        self.bill_tree.column("Product Name", anchor=tk.CENTER, width=200)
        self.bill_tree.column("Quantity", anchor=tk.CENTER, width=100)
        self.bill_tree.column("Price (INR)", anchor=tk.CENTER, width=100)
        self.bill_tree.column("Total (INR)", anchor=tk.CENTER, width=100)
       
        self.bill_tree.heading("#0", text="", anchor=tk.CENTER)
        self.bill_tree.heading("Product No", text="Product No", anchor=tk.CENTER)
        self.bill_tree.heading("Product Name", text="Product Name", anchor=tk.CENTER)
        self.bill_tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
        self.bill_tree.heading("Price (INR)", text="Price (INR)", anchor=tk.CENTER)
        self.bill_tree.heading("Total (INR)", text="Total (INR)", anchor=tk.CENTER)
    
        # Dictionary to store aggregated items with updated quantities
        aggregated_cart = {}
        for item in self.cart:
            product_no, product_name, qty, price = item
            if product_no in aggregated_cart:
                # Update the quantity and recalculate the total
                aggregated_cart[product_no]['qty'] += int(qty)
            else:
                # Add new item to the aggregated cart
                aggregated_cart[product_no] = {
                    'product_name': product_name,
                    'qty': int(qty),
                    'price': float(price)
                }
        
        total_amount = 0
        
        for product_no, details in aggregated_cart.items():
            product_name = details['product_name']
            qty = details['qty']
            price = details['price']
            total_price = qty * price
            total_amount += total_price
            
            self.bill_tree.insert("", "end", values=(product_no, product_name, qty, price, total_price))
       
        tk.Label(left_frame, text=f"Total Amount: INR {total_amount}", font=("Arial", 16)).pack(pady=10)
    
        self.bill_data = (self.customer_name, self.cart.copy(), total_amount)
    
        self.create_button(left_frame,"Buy Now", self.verify_and_print_bill).pack(pady=10)
        self.create_button(left_frame,"Back to Product Menu", self.show_product_menu).pack(pady=5)

    def check_verification_code(self):
        code = self.entry_verification_code.get()
        if code == "0101":  # Static verification code
            self.save_bill()  # Save the bill data to sales.csv
            self.update_products_after_purchase()  # Update product quantities after purchase
            self.show_thank_you_page() #Succesfull payment
            self.cart.clear()  # Clear the cart after payment
            #self.show_user_menu()  # Redirect to user menu
        else:
            messagebox.showerror("Error", "Invalid verification code")
            self.verify_and_print_bill()

    def verify_and_print_bill(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Verification Code", font=("Arial", 20),bg='#f0f4f8', fg='#003366').pack(pady=10)
        self.entry_verification_code = tk.Entry(self.root, show="*")
        self.entry_verification_code.pack(pady=10)

        self.create_button(self.root,"Submit", self.check_verification_code).pack(pady=10)
    
    def show_thank_you_page(self):
        self.clear_window()  # Clear the current window
        tk.Label(self.root, text="Payment successful.", font=("Times New Roman", 15),bg='#f0f4f8', fg='#003366').pack(pady=20)
        tk.Label(self.root, text="Thank You for Visiting!", font=("Arial", 24),bg='#f0f4f8', fg='#003366').pack(pady=20)
       
   
        self.create_button(self.root,"Return to User Menu", self.show_user_menu).pack(pady=20)
    
    def save_bill(self):
        customer_name, cart, total_amount = self.bill_data
        items_purchased = '; '.join([f"{item[0]} x{item[1]}" for item in cart])
        # Get current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Open the csv file in append mode and write the data along with the timestamp
        with open('sales.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([customer_name, items_purchased, total_amount, timestamp])

    # Sales data in admin panel
    def view_sales(self):
        self.clear_window()
        tk.Label(self.root, text="Sales Data", font=("Arial", 20),bg='#f0f4f8', fg='#003366').pack(pady=20)
   
        tk.Label(self.root, image=self.show_image('view_sales.png',100,100), bg='#f0f4f8').pack(pady=10)
        # Read sales data from 'sales.csv'
        try:
            with open('sales.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                sales_data = list(reader)
        except FileNotFoundError:
            sales_data = []
   
        # Create a scrollbar
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
   
        # Create a treeview for displaying sales data
        self.sales_tree = ttk.Treeview(self.root, yscrollcommand=scrollbar.set, show="headings")
        self.sales_tree.pack()
   
        scrollbar.config(command=self.sales_tree.yview)
   
        # Add "Timestamp" column to the treeview
        self.sales_tree["columns"] = ("Customer Name", "Items Purchased", "Total Amount (INR)", "Timestamp")
        self.sales_tree.column("#0", width=0, stretch=tk.NO)
        self.sales_tree.column("Customer Name", anchor=tk.CENTER, width=150)
        self.sales_tree.column("Items Purchased", anchor=tk.CENTER, width=300)  # Left-aligned for better readability
        self.sales_tree.column("Total Amount (INR)", anchor=tk.CENTER, width=150)
        self.sales_tree.column("Timestamp", anchor=tk.CENTER, width=180)
   
        self.sales_tree.heading("Customer Name", text="Customer Name", anchor=tk.CENTER)
        self.sales_tree.heading("Items Purchased", text="Items Purchased", anchor=tk.CENTER)
        self.sales_tree.heading("Total Amount (INR)", text="Total Amount (INR)", anchor=tk.CENTER)
        self.sales_tree.heading("Timestamp", text="Timestamp", anchor=tk.CENTER)
   
        total_sales = 0
        for sale in sales_data:
            customer_name, items_purchased, total_amount, timestamp = sale

            # Insert sales data into the treeview
            self.sales_tree.insert("", "end", values=(customer_name, items_purchased, total_amount, timestamp))
   
            total_sales += float(total_amount)
   
        # Display total sales
        tk.Label(self.root, text=f"Total Sales: INR {total_sales}", font=("Arial", 16)).pack(pady=10)
        self.create_button(self.root,"Back to Admin Menu",self.show_admin_menu).pack(pady=10)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = SupermarketApp(root)
    root.mainloop()