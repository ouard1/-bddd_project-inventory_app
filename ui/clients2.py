from tkinter import * 
from tkinter import ttk 
import sys
sys.path.append('../.')

from logic import customers_crud

root =Tk()
root.title("Clients details") 
#root.iconbitmap('')
root.geometry("1000x500") 

style =ttk.Style()
#Theme 
style.theme_use("default")
#configuring the treeview 
style.configure("Treeview",
                backgroung="#D3D3D3D",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3"
                )
#changing selected color
style.map('Treeview'  , 
          background=[('selected','#347083')])

#create a Treeview frame 
def load_customers(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Get customers from the database
        records= customers_crud.get_customers()
        global count 
        count=0
        for record in records :
            if count % 2 ==0 :
                my_tree.insert(parent='',index='end' , iid=count,text="",values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('evenrow',))
            else :
                my_tree.insert(parent='',index='end' ,iid=count,text="",values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7]), tags=('oddrow',))
                count += 1
tree_frame = Frame(root)
tree_frame.pack(pady=10)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT,fill=Y)

#create the Treeview 
my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended")

my_tree.pack()

#configure the scrollbar

tree_scroll.config(command=my_tree.yview)

#define our columns
my_tree['columns'] = ( "First Name", "Last Name", "Email", "Contact Number", "Address", "City", "Country")
#format our columns 
my_tree.column("#0" , width=0 , stretch =NO)
my_tree.column("First Name" , anchor=W , width=140 )
my_tree.column("Last Name" , anchor=W , width=140 )
my_tree.column("Email" , anchor=W , width=140 )
my_tree.column("Contact Number" , anchor=W , width=140 )
my_tree.column("Address" , anchor=W , width=140 )
my_tree.column("City" , anchor=W , width=140 )
my_tree.column("Country" , anchor=W , width=140 )

#create headings 

my_tree.heading("#0",text="" , anchor=W)
my_tree.heading("First Name",text="" , anchor=W)
my_tree.heading("Last Name",text="" , anchor=W)
my_tree.heading("Email" ,text="" , anchor=W)
my_tree.heading("Contact Number",text="" , anchor=W)
my_tree.heading("Address" ,text="" , anchor=W)
my_tree.heading("Country" ,text="" , anchor=W)

#create striped row tags 

my_tree.tag_configure("oddrow",background="white")

my_tree.tag_configure("evenrow",background="lightblue")
#add record entry boxes 

data_frame =LabelFrame(root,text="Record")
data_frame.pack(fill="x",expand="yes",padx=20)

fn_label =Label(data_frame,text="First Name")
fn_label.grid(row=0,column=0,padx=10 ,pady=10)
fn_entry =Entry(data_frame)
fn_entry.grid(row=0,column=1,padx=10 ,pady=10)

ln_label =Label(data_frame,text="Last Name")
ln_label.grid(row=0,column=2,padx=10 ,pady=10)
ln_entry =Entry(data_frame)
ln_entry.grid(row=0,column=3,padx=10 ,pady=10)

id_label =Label(data_frame,text="Email")
id_label.grid(row=0,column=4,padx=10 ,pady=10)
id_entry =Entry(data_frame)
id_entry.grid(row=0,column=5,padx=10 ,pady=10)

cn_label =Label(data_frame,text="Contact Number")
cn_label.grid(row=1,column=0,padx=10 ,pady=10)
cn_entry =Entry(data_frame)
cn_entry.grid(row=1,column=1,padx=10 ,pady=10)

address_label =Label(data_frame,text="Address")
address_label.grid(row=1,column=2,padx=10 ,pady=10)
address_entry =Entry(data_frame)
address_entry.grid(row=1,column=3,padx=10 ,pady=10)

country_label =Label(data_frame,text="Country")
country_label.grid(row=1,column=4,padx=10 ,pady=10)
country_entry =Entry(data_frame)
country_entry.grid(row=1,column=5,padx=10 ,pady=10)
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
    x=my_tree.selection()[0]
    my_tree.delete(x)
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
    fn_entry.delete(0,END)
    ln_label.delete(0,END)
    id_label.delete(0,END)
    cn_label.delete(0,END)
    address_label.delete(0,END)
    country_label.delete(0,END)

#select record 
def select_record(e) : 
    #clear entry boxes
    fn_entry.delete(0,END)
    ln_entry.delete(0,END)
    id_entry.delete(0,END)
    cn_entry.delete(0,END)
    address_entry.delete(0,END)
    country_entry.delete(0,END)


    #grab record number
    selected = my_tree.focus()
    #grab record values 
    values=my_tree.item(selected,values)

    #output entry boxes 
    fn_entry.insert(0,values[0])
    ln_entry.insert(0,values[1])
    id_entry.insert(0,values[2])
    cn_entry.insert(0,values[3])
    address_entry.insert(0,values[4])
    country_entry.insert(0,values[5])
  

#update record 
def update_record():
    selected =my_tree.focus()
    my_tree.item(selected ,text="",values=(fn_entry.get(),ln_entry.get(),id_entry.get(),cn_entry.get(),address_entry.get))
    fn_entry.delete(0,END)
    ln_entry.delete(0,END)
    id_entry.delete(0,END)
    cn_entry.delete(0,END)
    address_entry.delete(0,END)
    country_entry.delete(0,END)

#add buttons 
button_frame = LabelFrame(root,text="Commands")
button_frame.pack(fill="x" ,expand="yes" ,padx=20)

update_button = Button(button_frame,text="update client",command=update_record)
update_button.grid(row=0 , column=0 ,padx=10,pady=10)

add_button = Button(button_frame,text="add client")
add_button.grid(row=0 , column=1 ,padx=10,pady=10)

remove_all_button = Button(button_frame,text="remove all clients",command=remove_all)
remove_all_button.grid(row=0 , column=2 ,padx=10,pady=10)

remove_one_button = Button(button_frame,text="remove selected client",command=remove_one)
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

#run to pull data from database on start
load_customers()
root.mainloop()