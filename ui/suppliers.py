import tkinter as tk
from tkinter import ttk, messagebox
from logic import suppliers_crud
from tkinter import * 
import tkintermapview

class   SuppliersWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Suppliers details") 
        #self.iconbitmap('')
        self.geometry("1000x500") 

        style =ttk.Style()
        #Theme 
        style.theme_use("default")
        #configuring the treeview 
        style.configure("Treeview",
                        backgroung="#D3D3D3D",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3",
                        show="headings"
                        )
        #changing selected color
        style.map('Treeview'  , 
                background=[('selected','#347083')])

       
        tree_frame = Frame(self)
        tree_frame.pack(pady=10)
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT,fill=Y)

        #create the Treeview 
        my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended")

        my_tree.pack()
         #create a Treeview frame 
        def load_suppliers(self):
                # Get customers from the database
                records= suppliers_crud.get_suppliers()
                global count 
                count=0
                for record in records :
                    if count % 2 == 0 :                                             
                        my_tree.insert(parent='',index='end' , iid=count,text="",values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('evenrow',))
                    else :
                        my_tree.insert(parent='',index='end' ,iid=count,text="",values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('oddrow',))
                    count += 1
        #configure the scrollbar

        tree_scroll.config(command=my_tree.yview)

        #define our columns      
        my_tree['columns'] = ("Supplier id","Full name", "Contact person", "Contact number", "Email", "Address", "City", "Country")

        #format our columns 
        my_tree.column("#0" , width=0 , stretch =NO)
        my_tree.column("Supplier id" , anchor=W , width=140 )
        my_tree.column("Full name" , anchor=W , width=140 )
        my_tree.column("Contact person" , anchor=W , width=140 )
        my_tree.column("Contact number" , anchor=W , width=140 )
        my_tree.column("Email" , anchor=W , width=140 )
        my_tree.column("Address" , anchor=W , width=140 )
        my_tree.column("City" , anchor=W , width=140 )
        my_tree.column("Country" , anchor=W , width=140 )

        #create headings 

        my_tree.heading("#0",text="" , anchor=W)
        my_tree.heading("Supplier id" , text="Supplier id" ,anchor=W )
        my_tree.heading("Full name",text="Full name", anchor=W)
        my_tree.heading("Contact person",text="Contact person" , anchor=W)
        my_tree.heading("Contact number" ,text="Contact number" , anchor=W)
        my_tree.heading("Email",text="Email" , anchor=W)
        my_tree.heading("Address" ,text="Address" , anchor=W)
        my_tree.heading("City" ,text="City", anchor=W)
        my_tree.heading("Country" ,text="Country" , anchor=W)

        #create striped row tags 

        my_tree.tag_configure("oddrow",background="white")

        my_tree.tag_configure("evenrow",background="lightblue")
        #add record entry boxes 

        data_frame =LabelFrame(self,text="Record")
        data_frame.pack(fill="x",expand="yes",padx=20)

        fn_label =Label(data_frame,text="Full name")
        fn_label.grid(row=0,column=0,padx=10 ,pady=10)
        fn_entry =Entry(data_frame)
        fn_entry.grid(row=0,column=1,padx=10 ,pady=10)

        ln_label =Label(data_frame,text="Contact person")
        ln_label.grid(row=0,column=2,padx=10 ,pady=10)
        ln_entry =Entry(data_frame)
        ln_entry.grid(row=0,column=3,padx=10 ,pady=10)

        id_label =Label(data_frame,text="Contact number")
        id_label.grid(row=0,column=4,padx=10 ,pady=10)
        id_entry =Entry(data_frame)
        id_entry.grid(row=0,column=5,padx=10 ,pady=10)

        cn_label =Label(data_frame,text= "Email")
        cn_label.grid(row=1,column=0,padx=10 ,pady=10)
        cn_entry =Entry(data_frame)
        cn_entry.grid(row=1,column=1,padx=10 ,pady=10)

        address_label =Label(data_frame,text="Address")
        address_label.grid(row=1,column=2,padx=10 ,pady=10)
        address_entry =Entry(data_frame)
        address_entry.grid(row=1,column=3,padx=10 ,pady=10)
        def select_location(self):
            # Open a map window to select location
            map_window = tk.Toplevel(self)
            map_window.title("Select Location")
            map_window.geometry("500x300")

            # Create a map widget
            map_widget = tkintermapview.TkinterMapView(map_window, width=700, height=700, corner_radius=0)
            map_widget.set_address("bejaia")
            map_widget.set_zoom(15)
            map_widget.pack()

            # Function to handle location selection
            def set_address(coords):
                # Update address entry in SuppliersWindow
                adr = tkintermapview.convert_coordinates_to_address(coords[0],coords[1])
                clean_address = adr.address +" coordinates : "+str(coords)
                print(clean_address)
                address_entry.delete(0, END)
                address_entry.insert(0, clean_address)

                # Close the map window
                map_window.destroy()


            map_widget.add_right_click_menu_command(label="get location",
                                        command=set_address,
                                        pass_coords=True)
        select_location_button = Button(data_frame, text="Map Location", command=lambda: select_location(self))
        select_location_button.grid(row=1, column=4, padx=10, pady=10)

        city_label =Label(data_frame,text="City")
        city_label.grid(row=1,column=4,padx=10 ,pady=10)
        city_entry =Entry(data_frame)
        city_entry.grid(row=1,column=5,padx=10 ,pady=10)

        country_label =Label(data_frame,text="Country")
        country_label.grid(row=2,column=0,padx=10 ,pady=10)
        country_entry =Entry(data_frame)
        country_entry.grid(row=2,column=1,padx=10 ,pady=10)
      

        supplier_id_label = Label(data_frame, text="Supplier id")
        supplier_id_label.grid(row=2, column=2, padx=10, pady=10)
        supplier_id_entry = Entry(data_frame)
        supplier_id_entry.grid(row=2, column=3, padx=10, pady=10)
        #move row up 
        def up():
            rows =my_tree.selection()
            for row in rows : 
                my_tree.move(row,my_tree.parent(row),my_tree.index(row)-1) 

        #move row down
        def down():
            rows =my_tree.selection()
            for row in reversed(rows) : 
                my_tree.move(row,my_tree.parent(row),my_tree.index(row)+1) 

        #remove record
        def remove_one():
            selected = my_tree.selection()
            if selected:  
                supplier_id = my_tree.item(selected[0])["values"][0]  
                deleted=suppliers_crud.delete_supplier(supplier_id)
                if deleted :my_tree.delete(selected[0])
                clear_entries()
            else:
                messagebox.showerror("Error", "Please select a supplier to remove")

        #remove many record 
        def remove_many():
            x=my_tree.selection()
            for record in x : 
                my_tree.delete(record)

        #remove all records 
        def remove_all():
            for record in my_tree.get_children():
                my_tree.delete(record)

        def clear_entries():
            supplier_id_entry.delete(0,END)
            fn_entry.delete(0,END)
            ln_entry.delete(0,END)
            id_entry.delete(0,END)
            cn_entry.delete(0,END)
            address_entry.delete(0,END)
            city_entry.delete(0,END)
            country_entry.delete(0,END)

        #select record 
        def select_record(e) : 
            #clear entry boxes
            supplier_id_entry.delete(0,END)
            fn_entry.delete(0,END)
            ln_entry.delete(0,END)
            id_entry.delete(0,END)
            cn_entry.delete(0,END)
            address_entry.delete(0,END)
            city_entry.delete(0,END)
            country_entry.delete(0,END)
           

            #grab record number
            selected = my_tree.focus()
            #grab record values 
            values=my_tree.item(selected,'values')

            #output entry boxes 
            supplier_id_entry.insert(0,values[0])
            fn_entry.insert(0,values[1])
            ln_entry.insert(0,values[2])
            id_entry.insert(0,values[3])
            cn_entry.insert(0,values[4])
            address_entry.insert(0,values[5])
            city_entry.insert(0,values[6])
            country_entry.insert(0,values[7])
        

        def create_supplier(): 
            first_name = fn_entry.get()
            last_name = ln_entry.get()
            email = id_entry.get()
            contact_number = cn_entry.get()
            address = address_entry.get()
            city = city_entry.get()
            country = country_entry.get()
              
            suppliers_crud.create_supplier(first_name, last_name, email, contact_number, address, city, country)
            fn_entry.delete(0,END)
            ln_entry.delete(0,END)
            id_entry.delete(0,END)
            cn_entry.delete(0,END)
            address_entry.delete(0,END)
            city_entry.delete(0,END)
            country_entry.delete(0,END)
        
             # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())
            load_suppliers(self)

    

        #update record 
        def update_record():
            selected =my_tree.focus()
            supplier_id = my_tree.item(selected)["values"][0]  
            # Get other values from entry boxes
            first_name = fn_entry.get()
            last_name = ln_entry.get()
            email = id_entry.get()
            contact_number = cn_entry.get()
            address = address_entry.get()
            city = city_entry.get()
            country = country_entry.get()

            # Call the logic function to update the database
            suppliers_crud.update_supplier(supplier_id, first_name, last_name, email, contact_number, address, city, country)
            supplier_id_entry.delete(0,END)
            fn_entry.delete(0,END)
            ln_entry.delete(0,END)
            id_entry.delete(0,END)
            cn_entry.delete(0,END)
            address_entry.delete(0,END)
            city_entry.delete(0,END)
            country_entry.delete(0,END)

            my_tree.delete(*my_tree.get_children())
            load_suppliers(self)
        

     
   
        #add buttons 
        button_frame = LabelFrame(self,text="Commands")
        button_frame.pack(fill="x" ,expand="yes" ,padx=20)

        

        update_button = Button(button_frame,text="update supplier",command=update_record)
        update_button.grid(row=0 , column=0 ,padx=10,pady=10)

        add_button = Button(button_frame,text="add supplier",command=create_supplier)
        add_button.grid(row=0 , column=1 ,padx=10,pady=10)

        remove_all_button = Button(button_frame,text="remove all suppliers",command=remove_all)
        remove_all_button.grid(row=0 , column=2 ,padx=10,pady=10)

        remove_one_button = Button(button_frame,text="remove selected supplier",command=remove_one)
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
        my_tree.bind("<ButtonRelease-1>",select_record)
        
        load_suppliers(self)