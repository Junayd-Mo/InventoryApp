from tkinter import *
import tkinter as tk
from tkinter.messagebox import * #importing all moduels and libraries 
import sqlite3
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd
#=====================GUI MASTER===================#
main_app = tk.Tk()
main_app.configure(bg='#89CFF0')
main_app.title('Main Menu')
main_app.geometry("1200x800")
main_app.resizable(0,0) 
main_app.attributes('-fullscreen', True) 
main_title = tk.Label(main_app,bg='#89CFF0',text='Main Menu',font=('Arial',50),fg='Black')
main_title.pack()
#  creating the master window defining its name, size and colour.

conn = sqlite3.connect("products.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS items (name text,
price real, quantity integer, cost real,sales integer)''')
#Creating a database if one called products doesnt exist 
sql_query = """SELECT * FROM items"""
c.execute(sql_query)
data = c.fetchall()
#storing all the data in the database in a variable


#Import the image using PhotoImage function
click_btn= PhotoImage(file='close.png')

#makes only the main menu window visible    
def erase_window(window):
    main_app.deiconify()
    window.destroy()



#============================FUNCTIONS FOR BUTTONS===============================================#
def Quit():
    answer = askyesno(title='Confirmation', message='Are you sure that you want to quit?')
    if answer == True:
        main_app.withdraw()
        quit()
    else:
        None
    
#Quit function closes the app

#============================ANALYSIS WINDOW===============================================#
def Analysis(click_btn):
    main_app.withdraw()
    #creating the window    
    analysis_window = Toplevel(main_app,bg ='#89CFF0')
    analysis_window.title('Analysis Page')
    analysis_window.geometry("1200x800")
    analysis_window.attributes('-fullscreen', True)
    analysis_title = tk.Label(analysis_window,bg='#89CFF0', text='Analysis',
                              font=('Arial',50),fg='Black')
    analysis_title.pack()

    #connecting to the database
    connection = sqlite3.connect('products.db')
    cursor = connection.cursor()
    
    sql_query = """SELECT * FROM items"""

    cursor.execute(sql_query)
    data = cursor.fetchall()

    #creating the graph based on user selection
    def graph(data,products):
        selected_products = []
        selected_sales = []  
        for i in products.curselection():
            selected_sales.append(pd_data.at[i,'product_sales'])
            selected_products.append(products.get(i))
        plt.bar(selected_products,selected_sales,color="#32a852",edgecolor="#03ff47")
        plt.show()
        

    #Importing all required libraries
    sql_query = """SELECT * FROM items"""
    cursor.execute(sql_query)
    #creating a dataframe with all database data inside     
    pd_data =cursor.fetchall()
    column_names = ["product","sale_price","quantity","product_price", "product_sales"]
    pd_data = pd.DataFrame(data,columns=column_names)
    products_list = []

    #creating an array with all the names of the products 
    for i in range (len(pd_data.index)):
        products_list.append(pd_data.at[i,'product'])

    prompt_title = Label(analysis_window,text='Select the items you would like to graph'
                                     ,bg='#89CFF0',font=('Arial',20),fg='Black')
    prompt_title.pack()


    products = Listbox(analysis_window,selectmode="multiple",font=('Arial',20))
    products.pack(expand=NO,fill="both")

    for i in products_list:
        products.insert(END,i)#inserting data that i want to display into the listbox

        
    graph_button = Button(analysis_window,text='display graph',command=(lambda:(graph(pd_data,products))))
    graph_button.pack()

    #Let us create a dummy button and pass the image
    image_button= Button(analysis_window,activebackground='#89CFF0',image=click_btn,command= lambda:(erase_window(analysis_window)),
    borderwidth=0,text='Button')


    
    image_button.place(x=0, y=0)
#============================PRODUCT OVERVIEW WINDOW===============================================#
def Product_overview(click_btn,data):
    main_app.withdraw()
    Product_overview_window = Toplevel(main_app,bg ='#89CFF0')
    Product_overview_window.title('Product Overview Page')
    Product_overview_window.geometry("1200x800")
    Product_overview_window.attributes('-fullscreen', True)
    Product_title = tk.Label(Product_overview_window,bg='#89CFF0', text='Product Overview',
                              font=('Arial',50),fg='Black')
    Product_title.grid(column=3,row=0)

    # define columns
    columns = ('product_name', 'product_price', 'products_quantity','product_cost')
    container = Frame(Product_overview_window)
    container.place(y=100,x=100)
    tree = ttk.Treeview(container, columns=columns, show='headings', height=15)
    
    # define headings
    tree.heading('product_name', text='Product Name')
    tree.heading('product_price', text='Price')
    tree.heading('products_quantity', text='Quantity')
    tree.heading('product_cost', text='Cost')

    #connecting to database
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    sql_query = """SELECT * FROM items"""

    c.execute(sql_query)
    data = c.fetchall()
    
    # add data to the treeview
    for product in data:
        tree.insert('', tk.END, values=product)


    tree.grid(row=0, column=0, sticky='nsew')

    # add a scrollbar
    scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0,column=1,sticky='ns')

    #Let us create a dummy button and pass the image
    image_button= Button(Product_overview_window, image=click_btn,command= lambda:(erase_window(Product_overview_window)),
    borderwidth=0,text='Button')

    image_button.grid(column=0,row=0)
#=================================== ADD STOCK ===============================================#
def Add_stock(click_btn):
    #making the main app not visible 
    main_app.withdraw()
    #creating and customising new window
    add_stock_window = Toplevel(main_app,bg ='#89CFF0')
    add_stock_window.title('Add Products Page')
    add_stock_window.geometry("1200x800")
    add_stock_window.attributes('-fullscreen', True)
    add_title = tk.Label(add_stock_window,bg='#89CFF0', text='Add Products',
                              font=('Arial',50),fg='Black')
    add_title.grid(column=10, row=0)

    def add_products():
        #getting all the data from the entry boxes
        product_name = entry_product_name.get()
        product_price = entry_product_price.get()
        product_quantity = entry_product_quantity.get()
        product_cost = entry_product_cost.get()
        product_sales = 0
        added_data = (product_name, product_price, product_quantity, product_cost,product_sales)

        #connecting or creating a database if it does not exist 
        conn = sqlite3.connect("products.db")
        c = conn.cursor()
        sql_query = """SELECT * FROM items"""
        c.execute(sql_query)
        data = c.fetchall()
        #error handling 
        try:
            #forcefully makes all the entries the right data type
            product_name = str(product_name)
            product_price = float(product_price)
            product_quantity = int(product_quantity)
            prodct_cost = float(product_cost)
            
        #if an error occurs then the except block of code will execute
        except ValueError:
            #checks if the user has left any entry boxes blank
            if product_name == "" or product_price == "" or product_quantity == "" or product_cost == "":
                        tk.messagebox.showerror("Error", "Please fill in all fields.")

            else:
                #only other ValueError that can occur is an invalid input 
                tk.messagebox.showerror("Error", "Invalid input for price, quantity or cost.")
            clear_entries()
            
        else:
            in_data = False
            for i in range (len(data)):
                if product_name == data[i][0]: #checks if the name inputted is in the database
                    in_data = True
            #if it is not in the database then it should add all entry boxes to the database 
            if in_data == False:
                c.execute("INSERT INTO items (name, price, quantity, cost,sales) VALUES (?, ?, ?, ?,?)",added_data)
                conn.commit()
                conn.close()
                tk.messagebox.showinfo("Success", "Product successfuly added.")
                clear_entries()
            else:
                tk.messagebox.showerror("Error", "This product is already saved.")
                clear_entries()

    #clearns the entryboxes 
    def clear_entries():
        entry_product_name.delete(0, tk.END)
        entry_product_price.delete(0, tk.END)
        entry_product_quantity.delete(0, tk.END)
        entry_product_cost.delete(0, tk.END)

    #lables and entry boxes being created and displayed
    label_product_name = tk.Label(add_stock_window, text="Product Name:", font=('Arial',25),fg='Black')
    label_product_name.grid(column=0,row=1,pady=100,padx=0)

    entry_product_name = tk.Entry(add_stock_window,font=('Arial',25))
    entry_product_name.grid(column=1,row=1)

    label_product_price = tk.Label(add_stock_window, text="Product Price:", font=('Arial',25),fg='Black')
    label_product_price.grid(column=0,row=2,padx=0)

    entry_product_price = tk.Entry(add_stock_window,font=('Arial',25))
    entry_product_price.grid(column=1,row=2)

    label_product_quantity = tk.Label(add_stock_window, text="Product Quantity:", font=('Arial',25),fg='Black')
    label_product_quantity.grid(column=0,row=3,pady=100,padx=0)

    entry_product_quantity = tk.Entry(add_stock_window,font=('Arial',25))
    entry_product_quantity.grid(column=1,row=3)

    entry_product_cost = tk.Entry(add_stock_window,font=('Arial',25))
    entry_product_cost.grid(column=1,row=4)

    label_product_cost = tk.Label(add_stock_window, text='Product Cost:', font=('Arial',25),fg='Black')
    label_product_cost.grid(column=0,row=4,padx=10)

    add_product = tk.Button(add_stock_window, text='add product', command=add_products,font=('Arial',18))
    add_product.grid(column=10,row=3)


    #creating a dummy button and passing the image into it  
    image_button= Button(add_stock_window, image=click_btn,command= lambda:(erase_window(add_stock_window)),
    borderwidth=0,text='Button')
    
    image_button.place(x=0, y=0)


#=====================================EDIT_PRODUCTS================================================#

def Edit_products(click_btn):
    main_app.withdraw()

    Edit_products_window = Toplevel(main_app,bg ='#89CFF0')
    Edit_products_window.title('Edit products Page')
    Edit_products_window.geometry("1200x800")
    Edit_products_window.attributes('-fullscreen', True)
    Edit_title = tk.Label(Edit_products_window,bg='#89CFF0', text='Edit products',
                              font=('Arial',50),fg='Black')
    Edit_title.pack()




    #creating a dummy button and passing the image into it  
    image_button= Button(Edit_products_window, image=click_btn,command= lambda:(erase_window(Edit_products_window)),
    borderwidth=0,text='Button')
    
    image_button.place(x=0, y=0)


    connection = sqlite3.connect('products.db')
    sql_query = """SELECT * FROM items"""
    cursor = connection.cursor()
    cursor.execute(sql_query)
    #storing all contents from the database table into a variable

    data = cursor.fetchall()
    #creating a function to display the selected items data 
    def selection(data):
        selected_data = []
        for i in range (len(data)):
            if data[i][0] == clicked_edit.get() :
                selected_data = data[i] #storing the selected item into a variable

        #checks if the user has selected an item
        if clicked_edit.get() == 'products':
            tk.messagebox.showwarning('Warning', 'You must select an item before clicking select')

        else:
            #displaying all the entry boxes with the selected items data inside     
            display_frame = Frame(Edit_products_window,width=1000, border=False, height=10,bg='#89CFF0')
            display_frame.place(x=0,y=200)

            display_name = Entry(display_frame,font=('Arial',22),width=24)
            display_name.insert(END,selected_data[0])
            display_name.grid(column=2,row=2)

            display_price = Entry(display_frame,font=('Arial',22),width=24)
            display_price.insert(END,selected_data[1])
            display_price.grid(column=3,row=2)
            
            display_quantity = Entry(display_frame,font=('Arial',22),width=24)
            display_quantity.insert(END,selected_data[2])
            display_quantity.grid(column=4,row=2)
            
            display_cost = Entry(display_frame,font=('Arial',22),width=24)
            display_cost.insert(END,selected_data[3])
            display_cost.grid(column=5,row=2)



        #making the table titles
            price_title= Label(Edit_products_window,text='Price',font=('Arial',30)
                               ,fg='black',bg='#89CFF0')
            price_title.place(x=390,y=145)

            name_title= Label(Edit_products_window,text='Name',font=('Arial',30),fg='black',bg='#89CFF0')
            name_title.place(x=0,y=145)

            quantity_title= Label(Edit_products_window,text='Quantitiy',font=('Arial',30),fg='black',bg='#89CFF0')
            quantity_title.place(x=780,y=145)

            cost_title= Label(Edit_products_window,text='Cost',font=('Arial',30),fg='black',bg='#89CFF0')
            cost_title.place(x=1170,y=145)

        #Creating the save button 
            save_button = Button(display_frame, text='Save', command=lambda:(save_changes(display_cost,display_name,display_price,display_quantity,selected_data)), width=7, height=3)
            save_button.grid(column=3,row=5)

        #Creating the delete button
            delete_button = Button(display_frame, text='Delete',
                                 width=7, height=3, command=delete_item)
            delete_button.grid(column=4,row=5)
        #Creating a function to delete selected item from the database 
    def delete_item():
        for i in range (len(data)):
            if data[i][0] == clicked_edit.get() :
                product = data[i][0]
        #allowing user to confirm their choice
        if tk.messagebox.askyesno('Confirm Choice', 'Are you sure you want to delete?') == True:
            cursor.execute("DELETE FROM items \n WHERE name = (?)",(product,))
            connection.commit()
            Edit_products_window.destroy()
            Edit_products(click_btn)
    #Creating a function to save changes made
    def save_changes(cost,name,price,quantity,selected_data):
        try:
            cost = float(cost.get())
            price = float(price.get())
            name = str(name.get())
            quantity = int(quantity.get())

        except:
            tk.messagebox.showerror('Warning', 'invalid input(s)')
            selection(data) #bringing the window back to defult
            
        else:
            #updating the database with correct user inputs
            connection = sqlite3.connect('products.db')
            cursor = connection.cursor()

            Name = (name,selected_data[0])
            cursor.execute("""UPDATE items SET name = ? WHERE name = ?""",(Name),)
            
            Price = (price,selected_data[1])
            cursor.execute("""UPDATE items SET price = ? WHERE price = ?""",(Price),)
            
            Quantity = (quantity,selected_data[2])
            cursor.execute("""UPDATE items SET quantity = ? WHERE quantity = ?""",(Quantity),)
            
            Cost = (cost,selected_data[3])
            cursor.execute("""UPDATE items SET cost = ? WHERE cost = ?""",(Cost),)

            connection.commit()


            #showing the user their changes was made successfully 
            if name != selected_data[0] or float(price) != float(selected_data[1]) or int(quantity) != int(selected_data[2] or float(cost) != float(selected_data[3])):
                tk.messagebox.showinfo("Success", "Your changes have been saved.")
                Edit_products_window.destroy()
                Edit_products(click_btn)
            #telling the user to make changes before clciking save
            else:
                tk.messagebox.showerror("Error", "Please make a change before saving.")
      

            
    clicked_edit = StringVar(main_app)
    clicked_edit.set('products') #setting a defult value for the dropdown list

    options_edit = []

    for i in range(len(data)):
        options_edit.append(data[i][0])

    #creating the dropdown list
    drop_edit = OptionMenu(Edit_products_window,clicked_edit, *options_edit,)
    drop_edit.config(width=10,font=('Arial',22),height=1)
    drop_edit.pack()

    #creating the select button
    select_button_edit = Button(Edit_products_window, text='select', command=lambda:(selection(data)),width=5,height=2)
    select_button_edit.place(x=871,y=85)



    
    
#============================DELETE PRODUCTS===============================================#
def Sales_Update(click_btn):
    main_app.withdraw()

    Sales_Update_window = Toplevel(main_app,bg ='#89CFF0' )
    Sales_Update_window.title('Sales Update Page')
    Sales_Update_window.geometry("1200x700")
    Sales_Update_window.attributes('-fullscreen', True)
    Sales_Update_title = tk.Label(Sales_Update_window,bg='#89CFF0', text='Sales Update',
                            font=('Arial',50),fg='Black')
    Sales_Update_title.pack()





    #Let us create a dummy button and pass the image
    image_button= Button(Sales_Update_window, image=click_btn,command=lambda:(erase_window(Sales_Update_window)),
    borderwidth=0,text='Button')
    image_button.place(x=0, y=0)

    clicked_update = StringVar(main_app)
    clicked_update.set('products')

    options_update = []
    connection = sqlite3.connect('products.db')
    sql_query = """SELECT * FROM items"""
    cursor = connection.cursor()
    cursor.execute(sql_query)
    data = cursor.fetchall()

    for i in range(len(data)):
        options_update.append(data[i][0])#storing all the product names into an array
    clicked_update = StringVar(main_app)
    clicked_update.set('products')

    drop_update = OptionMenu(Sales_Update_window,clicked_update, *options_update,)
    drop_update.config(width=10,font=('Arial',22),height=1)
    drop_update.pack()


    def selection():
        selected = clicked_update.get()
        if selected == 'products':
            tk.messagebox.showwarning('WARNING', 'Please select an item from the dropdown menu')

        else:
            container = Frame(Sales_Update_window, bg='#89CFF0', width=200,height=200)
            container.pack(side=TOP)
            
            update_entry = Entry(container,font=('Arial',22),width=24)
            update_entry.grid(column=1,row=0)

            promt = Label(container,font=('Arial',15), fg='Black', bg='#89CFF0',
                          text='Enter number of sales made for selected product: ')
            promt.grid(column=0,row=0)

            def Update(update_entry,clicked_update):
                update = update_entry.get()

                try:    
                    if isinstance(int(update),int) == True:#checks if the user inputted an integer 
                        for i in range (len(data)):
                            if data[i][0] == clicked_update.get():#finds the user selection
                                chosen_item = data[i][0]          #and stores it for later use
                                
                                if data[i][2] >= int(update): #checks if the user input is smaller or
                                                              #equal to the quantity of the product
                                    
                                    quantity = data[i][2] - int(update) #subtracts the user qunatity by
                                                                        #the user input saves it to update database
                                    tk.messagebox.showinfo('Success', 'Your changes have been saved')
                                    Sales_Update_window.destroy()
                                    Sales_Update(click_btn) #resets the window 
                                    cursor.execute("""UPDATE items SET quantity = ? WHERE name = ?""",(quantity,chosen_item))#updating the database  
                                    connection.commit()                                                                     #with new quantity
                                elif data[i][2] < int(update):
                                    tk.messagebox.showerror('Error', 'Number is too large.')
                                    update_entry.delete(0, tk.END)

                    sales_record = 0
                    for i in range(len(data)):
                        if data[i][0] == clicked_update.get():
                            sales_record = int(data[i][-1]) + int(update)#updates the sales record in database
                    cursor.execute("""UPDATE items SET sales = ? WHERE name = ? """,(sales_record,chosen_item))
                    connection.commit()
                        
                
                except:
                    if update == "" :
                        tk.messagebox.showerror("Error", "Please fill in field.")
                    else:
                        tk.messagebox.showerror("Error", "Invalid input.")
                        update_entry.delete(0, tk.END)
                    

                
            save_button_update = Button(Sales_Update_window,text='Update', command=lambda:(Update(update_entry,clicked_update)),width=10,height=4)
            save_button_update.pack()

    
    select_button_update = Button(Sales_Update_window, text='Select', command=selection,width=5,height=2)
    select_button_update.place(x=871,y=85) 

#===================================================================================================#
def Menu_buutons():
#=================================SIDE MENU FRAME MASTER==========================================================#
    side_menu = tk.Frame(main_app, width=200,height=1000,border=True,bg='#89CFF0')
    side_menu.place(x=0,y=0) #creates a frame for the side menu buttons
#================================BUTTONS===================================================================#
    #creating and adding the buttons to the previously created frame 
    analysis_button = tk.Button(side_menu,font=('Arial',18), height=4,bg='#FFE5B4',
                                text="Analysis", width=14,command=lambda:(Analysis(click_btn)))
    analysis_button.grid(column=0,row=0)

    product_overview_button = tk.Button(side_menu,bg='#FFE5B4', text='Product Overview',
                                        font=('Arial',18), height=4, width=14,
                                        command=lambda:(Product_overview(click_btn,data)))
    product_overview_button.grid(column=0,row=1)


    Add_stock_button = tk.Button(side_menu,font=('Arial',18), height=4,bg='#FFE5B4',
                                text="Add Stock", width=14,command=lambda:(Add_stock(click_btn)))
    Add_stock_button.grid(column=0,row=2)


    edit_products_button = tk.Button(side_menu,font=('Arial',18), height=4,bg='#FFE5B4',
                                text="Edit Products", width=14,command=lambda:(Edit_products(click_btn)))
    edit_products_button.grid(column=0,row=3)


    sales_update_button = tk.Button(side_menu,font=('Arial',18), height=4,bg='#FFE5B4',
                                text="Sales Update", width=14,command=lambda:(Sales_Update(click_btn)))
    sales_update_button.grid(column=0,row=4)


    Quit_button = tk.Button(side_menu,font=('Arial',18), height=4,bg='#FFE5B4',
                                text="Quit", width=14,command=Quit)
    Quit_button.grid(column=0,row=5)

Menu_buutons()

#========================MENU CONTENTS===============================================================#
menu_frame = tk.Frame(main_app, width=1320,height=700,border=True,bd=0,bg='#89CFF0')
menu_frame.place(x=209,y=75)
main_app.mainloop()

    
