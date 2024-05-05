import tkinter as tk
from tkinter import END, NO, RIGHT, W, Y, messagebox,LabelFrame,Label,Entry,Scrollbar,Frame,Button
from logic import inventory_items_crud  
from tkinter import ttk

class ItemsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Inventory Details")
        self.geometry("1200x500")

        # Configure Treeview style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#EAEAF4",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#EAEAF4",
                        show="headings"
                        )
        style.map('Treeview', background=[('selected', '#347083')])

        # Treeview frame and scrollbar
        tree_frame = Frame(self)
        tree_frame.pack(pady=10)
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview with columns
        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.my_tree.pack()

        self.my_tree['columns'] = ("Item ID", "Name", "Description", "Category", "Price", "Quantity", "Supplier Name")

        # Configure columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Item ID", anchor=W, width=120)
        self.my_tree.column("Name", anchor=W, width=200)
        self.my_tree.column("Description", anchor=W, width=250)
        self.my_tree.column("Category", anchor=W, width=120)
        self.my_tree.column("Price", anchor=W, width=100)
        self.my_tree.column("Quantity", anchor=W, width=100)
        self.my_tree.column("Supplier Name", anchor=W, width=200)

        # Create headings for columns
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("Item ID", text="Item ID", anchor=W)
        self.my_tree.heading("Name", text="Name", anchor=W)
        self.my_tree.heading("Description", text="Description", anchor=W)
        self.my_tree.heading("Category", text="Category", anchor=W)
        self.my_tree.heading("Price", text="Price", anchor=W)
        self.my_tree.heading("Quantity", text="Quantity", anchor=W)
        self.my_tree.heading("Supplier Name", text="Supplier Name", anchor=W)

        # Striped row tags (optional)
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="lightblue")

        # Function to load inventory data with supplier information
        def load_inventory(self):
            records = inventory_items_crud.get_inventory_items()
            count = 0
            for record in records:
                if count % 2 == 0:
                    self.my_tree.insert(parent='', index='end', iid=count, text="",
                                         values=record, tags=('evenrow',))
                else:
                    self.my_tree.insert(parent='', index='end', iid=count, text="",
                                         values=record, tags=('oddrow',))
                count += 1

            # Configure scrollbar
            tree_scroll.config(command=self.my_tree.yview)

      
        data_frame =LabelFrame(self,text="Record")
        data_frame.pack(fill="x",expand="yes",padx=20)

        in_label =Label(data_frame,text="Item ID")
        in_label.grid(row=0,column=0,padx=10 ,pady=10)
        in_entry =Entry(data_frame)
        in_entry.grid(row=0,column=1,padx=10 ,pady=10)

        ln_label =Label(data_frame,text="Name")
        ln_label.grid(row=0,column=2,padx=10 ,pady=10)
        ln_entry =Entry(data_frame)
        ln_entry.grid(row=0,column=3,padx=10 ,pady=10)

        dd_label =Label(data_frame,text="Description")
        dd_label.grid(row=0,column=4,padx=10 ,pady=10)
        dd_entry =Entry(data_frame)
        dd_entry.grid(row=0,column=5,padx=10 ,pady=10)

        cn_label =Label(data_frame,text="Category")
        cn_label.grid(row=1,column=0,padx=10 ,pady=10)
        cn_entry =Entry(data_frame)
        cn_entry.grid(row=1,column=1,padx=10 ,pady=10)

        price_label =Label(data_frame,text="Price")
        price_label.grid(row=1,column=2,padx=10 ,pady=10)
        price_entry =Entry(data_frame)
        price_entry.grid(row=1,column=3,padx=10 ,pady=10)

        quantity_label =Label(data_frame,text="Quantity")
        quantity_label.grid(row=1,column=4,padx=10 ,pady=10)
        quantity_entry =Entry(data_frame)
        quantity_entry.grid(row=1,column=5,padx=10 ,pady=10)

        sn_label =Label(data_frame,text="Supplier Name")
        sn_label.grid(row=2,column=0,padx=10 ,pady=10)
        sn_entry =Entry(data_frame)
        sn_entry.grid(row=2,column=1,padx=10 ,pady=10)

        #move row up 
        def up():
            rows =self.my_tree.selection()
            for row in rows : 
                self.my_tree.move(row,self.my_tree.parent(row),self.my_tree.index(row)-1) 

        #move row down
        def down():
            rows =self.my_tree.selection()
            for row in reversed(rows) : 
                self.my_tree.move(row,self.my_tree.parent(row),self.my_tree.index(row)+1) 

        #remove record
        def remove_one():
            selected = self.my_tree.selection()
            if selected:  
                item_id = self.my_tree.item(selected[0])["values"][0]  
                deleted=inventory_items_crud.delete_inventory_item(item_id)
                if deleted :self.my_tree.delete(selected[0])
                clear_entries()
            else:
                messagebox.showerror("Error", "Please select a customer to remove")

        #remove many record 
        def remove_many():
            x=self.my_tree.selection()
            for record in x : 
                self.my_tree.delete(record)

        #remove all records 
        def remove_all():
            for record in self.my_tree.get_children():
                self.my_tree.delete(record)

        def clear_entries():
            
            in_entry.delete(0,END)
            ln_entry.delete(0,END)
            dd_entry.delete(0,END)
            cn_entry.delete(0,END)
            price_entry.delete(0,END)
            quantity_entry.delete(0,END)
            sn_entry.delete(0,END)

        #select record 
        def select_record(e) : 
            #clear entry boxes
           
            in_entry.delete(0,END)
            ln_entry.delete(0,END)
            dd_entry.delete(0,END)
            cn_entry.delete(0,END)
            price_entry.delete(0,END)
            quantity_entry.delete(0,END)
            sn_entry.delete(0,END)


            #grab record number
            selected = self.my_tree.focus()
            #grab record values 
            values=self.my_tree.item(selected,'values')

            #output entry boxes 
           
            in_entry.insert(0,values[0])
            ln_entry.insert(0,values[1])
            dd_entry.insert(0,values[2])
            cn_entry.insert(0,values[3])
            price_entry.insert(0,values[4])
            quantity_entry.insert(0,values[5])
            sn_entry.insert(0,values[6])

        def create_inventory_item(): 
            item_id = in_entry.get()
            name = ln_entry.get()
            description= dd_entry.get()
            category = cn_entry.get()
            price = price_entry.get()
            quantity = quantity_entry.get()
            supplier_name = sn_entry.get()
            inventory_items_crud.create_inventory_item(name, description, category, price, quantity, supplier_name)
            in_entry.delete(0,END)
            ln_entry.delete(0,END)
            dd_entry.delete(0,END)
            cn_entry.delete(0,END)
            price_entry.delete(0,END)
            quantity_entry.delete(0,END)
            sn_entry.delete(0,END)
        
             # Clear The Treeview Table
            self.my_tree.delete(*self.my_tree.get_children())
            load_inventory(self)

    

        #update record 
        def update_record():
            selected =self.my_tree.focus()
            item_id = self.my_tree.item(selected)["values"][0]  
            # Get other values from entry boxes
            
            name = ln_entry.get()
            description = dd_entry.get()
            category = cn_entry.get()
            price = price_entry.get()
            quantity = quantity_entry.get()
            supplier_name = sn_entry.get()

            # Call the logic function to update the database
            inventory_items_crud.update_inventory_item(item_id,name,description, category, price,  quantity, supplier_name)
           
            in_entry.delete(0,END)
            ln_entry.delete(0,END)
            dd_entry.delete(0,END)
            cn_entry.delete(0,END)
            price_entry.delete(0,END)
            quantity_entry.delete(0,END)
            sn_entry.delete(0,END)

        #add buttons 
        button_frame = LabelFrame(self,text="Commands")
        button_frame.pack(fill="x" ,expand="yes" ,padx=20)

        update_button = Button(button_frame,text="update inventory item",command=update_record)
        update_button.grid(row=0 , column=0 ,padx=10,pady=10)

        add_button = Button(button_frame,text="add item",command=create_inventory_item)
        add_button.grid(row=0 , column=1 ,padx=10,pady=10)

        remove_all_button = Button(button_frame,text="remove all items",command=remove_all)
        remove_all_button.grid(row=0 , column=2 ,padx=10,pady=10)

        remove_one_button = Button(button_frame,text="remove selected item",command=remove_one)
        remove_one_button.grid(row=0 , column=3 ,padx=10,pady=10)

        remove_many_button = Button(button_frame,text="remove many selected",command=remove_many)
        remove_many_button.grid(row=0 , column=4 ,padx=10,pady=10)

        move_up_button = Button(button_frame,text="move up",command=up)
        move_up_button.grid(row=0 , column=5 ,padx=10,pady=10)

        move_down_button = Button(button_frame,text="move down",command=down)
        move_down_button.grid(row=0 , column=6 ,padx=10,pady=10)

        select_record_button = Button(button_frame,text="clear",command=clear_entries)
        select_record_button.grid(row=0 , column=7 ,padx=10,pady=10)


        #bind the tree view 
        self.my_tree.bind("<ButtonRelease-1>",select_record)

        #run to pull data from database on start
        load_inventory(self)