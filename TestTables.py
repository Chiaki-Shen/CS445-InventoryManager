import uuid
from functools import partial
from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3
from datetime import date
from tkinter import messagebox
import webbrowser
'''from shopify_scraper import get_bestware_products'''

def MainScreen(tab,root):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (1400 / 2)
    y = (hs / 2) - (1000 / 2)
    conn = sqlite3.connect('Hiccups.db')  # create a DB if there is not one
    c = conn.cursor()

    # c.execute("Delete from products where prodCode = 'Potato' ")
    '''
    c.execute("SELECT * FROM products")
    display1 = c.fetchall()
    print(display1)
    '''
    global currentSelectedTable
    # main option frame declare
    mainOptionFrame = Frame(tab)
    mainOptionFrame.grid(row=0, column=1, padx=20, pady=(10, 0))

    # Main screen Tables Combo Drop down
    mainList = ["Products", "Vendors", "Orders", "Vendor Price"]
    mainComboDropdown = ttk.Combobox(mainOptionFrame, value=mainList)
    mainComboDropdown.current(0)
    mainComboDropdown.bind("<<ComboboxSelected>>")
    # print(mainComboDropdown.get())
    mainComboDropdown.grid(row=1, column=1, pady=1, padx=1)

    # Main Screen sort-By Combo drop down
    mainSortList = ["Price: Low to High", "Price: High to Low", "Alphabetical", "Newest"]
    mainSortComboDropdown = ttk.Combobox(mainOptionFrame, value=mainSortList)
    mainSortComboDropdown.current(0)
    mainSortComboDropdown.bind("<<ComboboxSelected>>")
    # print(mainComboDropdown.get())
    mainSortComboDropdown.grid(row=7, column=1, pady=1, padx=1)


    class treeCurrentdisplay:
        def __init__(self, currenttable, index):
            self.currentTable = currenttable
            self.index = index
    class summaryDCFlag:
        def __init__(self, flag):
            self.flag = flag
    # addDataComandList in main Screen
    def addCommand():
        currentSelectedTable=mainComboDropdown.get()
        print("In ADD table " + currentSelectedTable)
        if(currentSelectedTable == "Products"):  # if dropdown selected table then
            print("Yes Products Add is selected")
            productsAddWindowPopup()
        elif(currentSelectedTable == "Vendors"):
            print("Yes Vendors Add is selected")
            vendorsAddWindowPopup()
        elif (currentSelectedTable == "Orders"):
            print("Yes Orders Add is selected")
            ordersAddWindowPopup()
        elif (currentSelectedTable == "Vendor Price"):
            print("Yes Vendor Price Add is selected")
            vendorPricesAddWindowPopup()
    def SummaryTreeRemove():
        # if (tableOndisplay.currentTable == "Product on Market"):
            # mainPageQuery_ContentTree.destroy()
        try:
            mainPageQuery_ContentTree.destroy()
            print("Summary REMOVED !!")
        except:
            print("Summary tree not defined")
    def treeRemove():
        currentSelectedTable = mainComboDropdown.get()
        if (currentSelectedTable !="Products"):
            try:
                display_Products_ContentTree.destroy()
                print("ProductTree Gone")
            except:
                print("Tree not defined")
        if (currentSelectedTable !="Orders"):
            try:
                display_Orders_ContentTree.destroy()
                print("OrderTree Gone")
            except:
                print("Tree not defined")
        if (currentSelectedTable !="Vendor Price"):
            try:
                display_VendorPrices_ContentTree.destroy()
                print("VendorPriceTree Gone")
            except:
                print("Tree not defined")

        if (currentSelectedTable !="Vendors"):
            try:
                display_Vendors_ContentTree.destroy()
                print("vendorTree Gone")
            except:
                print("Tree not defined")


    # this called after user click a column and click edit in Main screen
    def editCommand():
        # Check if anycolumn is selected by user
        # when current table on display is Products
        if (tableOndisplay.currentTable == "products"):
            selectColumn = display_Products_ContentTree.focus()
            if (selectColumn == ""):
                return 0
            print("In Edit table products")
            productEditWindowPopup()
        # when current table on display is Products
        elif(tableOndisplay.currentTable == "vendors"):
            selectColumn = display_Vendors_ContentTree.focus()
            if (selectColumn == ""):
                return 0
            print("In Edit table vendors")
            vendorsEditWindowPopup()
        elif (tableOndisplay.currentTable == "orders"):
            selectColumn = display_Orders_ContentTree.focus()
            if (selectColumn == ""):
                return 0
            print("In Edit table orders")
            ordersEditWindowPopup()


    # This def called after user confirm the changes
    def submitEditCommand():
        if (tableOndisplay.currentTable == "products"):
            submitEditProduct()
        elif (tableOndisplay.currentTable == "vendors"):
            submitEditVendor()
        elif (tableOndisplay.currentTable == "orders"):
            submitEditOrders()

    def askQuantityPopUp():

        global quantityAdd
        quantityAdd = Tk()
        quantityAdd.title("Adding to Cart")
        quantityAdd.geometry('%dx%d+%d+%d' % (250, 150, x*1.5, y*1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        global quantitybox1
        quantitybox1 = Entry(quantityAdd, width=30)  # product Code
        quantitybox1.grid(row=3, column=0, padx=20, pady=(10, 0))
        box = Label(quantityAdd, text="How many you want to buy?")
        box.grid(row=2, column=0, padx=20, pady=(10, 0))

        option_Add_btn = Button(quantityAdd, text="Add", command=submitAddCart)
        option_Add_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=20, ipadx=50)

        conn.commit()
        conn.close()

    def askQuantityPopUp2():

        global quantityAdd
        quantityAdd = Tk()
        quantityAdd.title("Adding to Cart")
        quantityAdd.geometry('%dx%d+%d+%d' % (250, 150, x*1.5, y*1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        global quantitybox1
        quantitybox1 = Entry(quantityAdd, width=30)  # product Code
        quantitybox1.grid(row=3, column=0, padx=20, pady=(10, 0))
        box = Label(quantityAdd, text="How many you want to buy?")
        box.grid(row=2, column=0, padx=20, pady=(10, 0))

        option_Add_btn = Button(quantityAdd, text="Add", command=submitAddCartFromSummaryTable)
        option_Add_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=20, ipadx=50)

        conn.commit()
        conn.close()



    def submitAddCart():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()


        selectColumn = display_Products_ContentTree.focus()
        valuesInColumn = display_Products_ContentTree.item(selectColumn, "values")


        mycart = []
        mycart.append(valuesInColumn[0])
        mycart.append(valuesInColumn[1])
        mycart.append(valuesInColumn[2])
        mycart.append(valuesInColumn[6])

        c.execute("SELECT unitListPrice FROM products p INNER JOIN vendorPrices vP on p.SKU = vP.SKU WHERE p.SKU = ?", (mycart[0],))
        unitPrice = c.fetchone()
        mycart.append(unitPrice[0])
        mycart.append(quantitybox1.get())



        try:
            c.execute("INSERT INTO cart VALUES (:SKU, :prodDesc, :productURL, :unitsInStock, :Quantity, :unitPrice, :totalPrice )",
                      {
                          'SKU': mycart[0],
                          'prodDesc': mycart[1],
                          'productURL': mycart[2],
                          'unitsInStock': mycart[3],
                          'Quantity': mycart[5],
                          'unitPrice': mycart[4],
                          'totalPrice': float(mycart[4]) * float(mycart[5])
                      })
            quantitybox1.delete(0,END)
        except:
            messagebox.showwarning('Failed adding', 'You have already add this one to the cart.')


        conn.commit()
        conn.close()
        quantityAdd.destroy()

    def submitAddCartFromSummaryTable():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()


        selectColumn = mainPageQuery_ContentTree.focus()
        valuesInColumn = mainPageQuery_ContentTree.item(selectColumn, "values")


        mycart = []
        mycart.append(valuesInColumn[1])
        mycart.append(valuesInColumn[2])
        c.execute("SELECT productURL FROM products WHERE SKU = ?",(mycart[0],))
        url = c.fetchone()
        c.execute("SELECT unitsInStock FROM products WHERE SKU = ?",(mycart[0],))
        stock = c.fetchone()
        c.execute("SELECT unitListPrice FROM products p INNER JOIN vendorPrices vP on p.SKU = vP.SKU WHERE p.SKU = ?", (mycart[0],))
        unitPrice = c.fetchone()
        mycart.append(url[0])
        mycart.append(stock[0])
        mycart.append(unitPrice[0])
        mycart.append(quantitybox1.get())

        try:
            c.execute("INSERT INTO cart VALUES (:SKU, :prodDesc, :productURL, :unitsInStock, :Quantity, :unitPrice, :totalPrice)",
                      {
                          'SKU': mycart[0],
                          'prodDesc': mycart[1],
                          'productURL': mycart[2],
                          'unitsInStock': mycart[3],
                          'Quantity': mycart[5],
                          'unitPrice':mycart[4],
                          'totalPrice':float(mycart[4]) * float(mycart[5])

                      })
            quantitybox1.delete(0,END)
        except:
            messagebox.showwarning('Failed adding', 'You have already add this one to the cart.')


        conn.commit()
        conn.close()
        quantityAdd.destroy()


    def addCart():
        if (tableOndisplay.currentTable == "products"):
            selectColumn = display_Products_ContentTree.focus()
            if (selectColumn == ""):
                return 0
            print("Adding products")
            askQuantityPopUp()
        elif(tableOndisplay.currentTable == "Product on Market"):
            selectColumn = mainPageQuery_ContentTree.focus()
            if (selectColumn == ""):
                return 0
            print("Adding products")
            askQuantityPopUp2()
        else:
            messagebox.showwarning('Failed', 'You have to switch to product table before adding')


    def showCart():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        # Query DB
        c.execute("SELECT * FROM cart")
        records = c.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        for row in records:
            print(row)
            tree.insert("", tk.END, values=row)

        conn.commit()
        conn.close()
        tree.bind('<Double-1>', doubleClicked)


    def DisplayCartWindowPopUp():
        global cart
        cart = Toplevel()
        message = "Cart"
        Label(cart, text=message).pack()
        new_element_header = ["SKU", "Prod Description", "Product URL", "Units In Stock", "Quantity", "unitPrice", "Total"]
        treeScroll = ttk.Scrollbar(cart)
        treeScroll.pack(side=RIGHT, fill=Y)
        global tree
        cart.geometry('%dx%d+%d+%d' % (1000, 600, x*1.5, y*1.5))
        tree = ttk.Treeview(cart, columns=new_element_header, show="headings", yscrollcommand=treeScroll)
        tree.column("SKU", width=120, minwidth=100, anchor=tk.CENTER)
        tree.heading("SKU", text="SKU")

        tree.column("Prod Description", width=250, minwidth=100, anchor=tk.CENTER)
        tree.heading("Prod Description", text="Prod Description")

        tree.column("Product URL", width=250, minwidth=100, anchor=tk.CENTER)
        tree.heading("Product URL", text="Product URL")

        tree.column("Quantity", width=100, minwidth=100, anchor=tk.CENTER)
        tree.heading("Quantity", text="Quantity")

        tree.column("Total", width=100, minwidth=100, anchor=tk.CENTER)
        tree.heading("Total", text="Total")

        tree.column("unitPrice", width=75, minwidth=75, anchor=tk.CENTER)
        tree.heading("unitPrice", text="unitPrice")

        tree.column("Units In Stock", width=75, minwidth=75, anchor=tk.CENTER)
        tree.heading("Units In Stock", text="Stock")
        tree.pack(side=LEFT, fill=BOTH)
        treeScroll.config(command=tree.yview)
        showCart()



    def newCart():

        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        c.execute("DROP TABLE IF EXISTS cart;")
        c.execute('''CREATE TABLE cart(
                          SKU VARCHAR (25) NOT NULL,
                          prodDesc VARCHAR NOT NULL,
                          productURL VARCHAR,
                          unitsInStock double DEFAULT 0,
                          Quantity double DEFAULT 1,
                          unitPrice double,
                          totalPrice double,
                          CONSTRAINT products_pk PRIMARY KEY (SKU)
                    );''')
        messagebox.showinfo("Success", "Your cart is now empty!")

        conn.commit()
        conn.close()

    def PlaceOrder():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        # Query DB

        c.execute("SELECT COUNT(SKU) FROM cart;")
        count = c.fetchone()
        num = count[0]
        if num == 0:
            messagebox.showerror('Failed', "You don't have anything in cart")
            return NONE

        c.execute("SELECT SKU FROM cart")
        SKUs = c.fetchall()
        listoutput = [i[0] for i in SKUs]



        c.execute("SELECT quantity FROM cart")
        Quantities = c.fetchall()
        listoutput2 = [i[0] for i in Quantities]





        uid_str = uuid.uuid4().urn
        orderId = uid_str[9:]

        c.execute("INSERT INTO orders VALUES (:id, :date,:orderStatus)",
                  {
                      'id': orderId,
                      'date': date.today(),
                      'orderStatus': 'Processing'
                  })

        for i in range (0, int(num)):
            c.execute("INSERT INTO orderLines VALUES (:id, :SKU,:itemQuantity)",
                            {
                                  'id': orderId,
                                  'SKU': listoutput[i],
                                  'itemQuantity': listoutput2[i]
                              })
            c.execute('''UPDATE products
                              SET
                                  unitsInStock = :stock + unitsInStock
                                WHERE SKU = :sku''',
                                {
                                    'stock': listoutput2[i],
                                    'sku':listoutput[i]
                                })
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Your order has been placed. (Now go shop!)")
        newCart()

    def displayCommand():
        SummaryTreeRemove()
        currentSelectedTable = mainComboDropdown.get()
        print("In Display table " + currentSelectedTable)
        if (currentSelectedTable == "Products"):  # if dropdown selected table then
            print("Yes Products display is selected")
            treeRemove()
            displayProductsWindowSetUp()
            queryProducts()
        elif (currentSelectedTable == "Vendors"):
            print("Yes Vendors display is selected")
            treeRemove()
            displayVendorsWindowSetUp()
            queryVendors()
        elif (currentSelectedTable == "Orders"):
            print("Yes Orders display is selected")
            treeRemove()
            displayOrdersWindowSetUp()
            queryOrders()
        elif (currentSelectedTable == "Vendor Price"):
            print("Yes Vendor Price display is selected")
            treeRemove()
            displayVendorPricesWindowSetUp()
            queryVendorPrices()
    def backToSummaryDisplay():
        try:
            display_Products_ContentTree.destroy()
        except:
            print("Tree not defined")
        try:
            display_Orders_ContentTree.destroy()
        except:
            print("Tree not defined")
        try:
            display_VendorPrices_ContentTree.destroy()
        except:
            print("Tree not defined")
        try:
            display_Vendors_ContentTree.destroy()
        except:
            print("Tree not defined")
        displayMainPageQueryWindowSetUp()
        mainPageQuery()


    def sortCommand(): ####################### Comand list for sort in certain type ################################
        currentSelectedSort = mainSortComboDropdown.get()
        if currentSelectedSort == "Price: Low to High":
            mainPageQuery("L2H")
        elif currentSelectedSort == "Price: High to Low":
            mainPageQuery("H2L")
        elif currentSelectedSort == "Alphabetical":
            mainPageQuery("ALPHABETICAL")
        elif currentSelectedSort == "Newest":
            mainPageQuery("Newest")


    def queryProducts():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        # Query DB
        c.execute("SELECT *,oid FROM products")
        records = c.fetchall()

        for row in display_Products_ContentTree.get_children():
            display_Products_ContentTree.delete(row)


        for row in records:
            print(row)
            display_Products_ContentTree.insert("", tk.END, values=row)
        conn.commit()
        conn.close()

    def queryVendors():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        # Query DB
        c.execute('''SELECT v.vendorName, v.phoneNumber, v.email, v.streetAddress, zL.zipCode, zL.city, zL.stateAbbr, v.websiteURL
                            FROM vendors v
                                INNER JOIN zipLocations zL on zL.zipCode = v.zipCode
                        ORDER BY vendorName''')
        records = c.fetchall()

        for row in display_Vendors_ContentTree.get_children():
            display_Vendors_ContentTree.delete(row)

        for row in records:
            print(row)
            display_Vendors_ContentTree.insert("", tk.END, values=row)
        conn.commit()
        conn.close()

    def queryOrders():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        # Query DB
        c.execute('''SELECT o.orderID, o.orderDate, o.orderStatus,
                                (SELECT SUM(oL.itemQuantity)
                                    FROM orderLines oL
                                WHERE o.orderId =oL.orderId )AS "Total Quantity",
                               (SELECT total FROM (SELECT DISTINCT (p.sku), unitListPrice * oL.itemQuantity AS total)) AS total
                            FROM orders o
                                INNER JOIN orderLines oL on o.orderId = oL.orderId
                                INNER JOIN products p on p.SKU = oL.SKU
                                INNER JOIN vendorPrices vP on p.SKU = vP.SKU
                        GROUP BY o.orderID, o.orderDate
                        ORDER BY o.orderDate;''')
        records = c.fetchall()

        for row in display_Orders_ContentTree.get_children():
            display_Orders_ContentTree.delete(row)

        for row in records:
            print(row)
            display_Orders_ContentTree.insert("", tk.END, values=row)
        conn.commit()
        conn.close()
        display_Orders_ContentTree.bind('<Double-1>', doubleClickedOrdersDetails)


    def mainPageQuery(opt = 'REGULAR'):
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        if (opt == 'ALPHABETICAL'):
            c.execute('''SELECT v.vendorName, products.SKU, products.prodDesc, unitListPrice, timeChecked
                            FROM products
                            INNER JOIN vendorPrices vP on products.SKU = vP.SKU
                            INNER JOIN vendors v on v.vendorName = vP.vendorName
                        ORDER BY products.SKU;''')
            records = c.fetchall()
        elif (opt == 'Newest'):
            c.execute('''SELECT v.vendorName, products.SKU, products.prodDesc, unitListPrice, timeChecked
                            FROM products
                            INNER JOIN vendorPrices vP on products.SKU = vP.SKU
                            INNER JOIN vendors v on v.vendorName = vP.vendorName
                        ORDER BY timeChecked;''')
            records = c.fetchall()
        elif(opt == 'L2H'):
            c.execute('''SELECT v.vendorName, products.SKU, products.prodDesc, unitListPrice, timeChecked
                            FROM products
                            INNER JOIN vendorPrices vP on products.SKU = vP.SKU
                            INNER JOIN vendors v on v.vendorName = vP.vendorName
                        ORDER BY unitListPrice ASC;''')
            records = c.fetchall()
        elif (opt == 'H2L'):
            c.execute('''SELECT v.vendorName, products.SKU, products.prodDesc, unitListPrice, timeChecked
                            FROM products
                            INNER JOIN vendorPrices vP on products.SKU = vP.SKU
                            INNER JOIN vendors v on v.vendorName = vP.vendorName
                        ORDER BY unitListPrice DESC;''')
            records = c.fetchall()
        else:
            c.execute('''SELECT v.vendorName, products.SKU, products.prodDesc, unitListPrice, timeChecked
                            FROM products
                            INNER JOIN vendorPrices vP on products.SKU = vP.SKU
                            INNER JOIN vendors v on v.vendorName = vP.vendorName;''')
            records = c.fetchall()

        for row in mainPageQuery_ContentTree.get_children():
            mainPageQuery_ContentTree.delete(row)

        for row in records:
            print(row)
            mainPageQuery_ContentTree.insert("", tk.END, values=row)


    def queryVendorPrices():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        # Query DB
        c.execute('''SELECT v.vendorName, p.prodDesc, unitListPrice, timeChecked
                        FROM vendors v
                            INNER JOIN vendorPrices vP on v.vendorName = vP.vendorName
                            INNER JOIN products p on p.SKU = vP.SKU
                    GROUP BY v.vendorName, p.prodDesc, unitListPrice, timeChecked
                    ORDER BY prodDesc''')
        records = c.fetchall()

        for row in display_VendorPrices_ContentTree.get_children():
            display_VendorPrices_ContentTree.delete(row)

        for row in records:
            print(row)
            display_VendorPrices_ContentTree.insert("", tk.END, values=row)
        conn.commit()
        conn.close()


    # DoubleClicked function
    def doubleClicked(event):
            region = tree.identify_column(event.x)
            conn = sqlite3.connect('Hiccups.db')
            c = conn.cursor()
            selectColumn = tree.focus()
            valuesInColumn = tree.item(selectColumn, "values")
            mycart = []
            mycart.append(valuesInColumn[0])
            c.execute("SELECT productURL FROM cart WHERE SKU = ?", (mycart[0],))
            url = c.fetchall()
            listoutput = [i[0] for i in url]
            webbrowser.open(listoutput[0])

    def doubleClickedOrdersDetails(event):

            region = display_Orders_ContentTree.identify_column(event.x)
            conn = sqlite3.connect('Hiccups.db')
            c = conn.cursor()
            selectColumn = display_Orders_ContentTree.focus()
            valuesInColumn = display_Orders_ContentTree.item(selectColumn, "values")

            global mycart
            mycart = []
            mycart.append(valuesInColumn[0]) #orderID
            mycart.append(valuesInColumn[1]) #date
            mycart.append(valuesInColumn[2]) #Quantity


            orderDetails = Toplevel()
            message = ("Order Details (" + mycart[0] + ")")
            global new_element_header
            new_element_header = [ "Prod Description", "Quantity", "unitPrice"]
            Label(orderDetails, text=message).pack()
            treeScroll = ttk.Scrollbar(orderDetails)
            treeScroll.pack(side=RIGHT, fill=Y)
            global orderDetail
            orderDetails.geometry('%dx%d+%d+%d' % (800, 600, x * 1.5, y * 1.5))
            orderDetail = ttk.Treeview(orderDetails, columns=new_element_header, show="headings", yscrollcommand=treeScroll)

            orderDetail.column("Prod Description", width=500, minwidth=100, anchor=tk.CENTER)
            orderDetail.heading("Prod Description", text="Prod Description")

            orderDetail.column("Quantity", width=150, minwidth=100, anchor=tk.CENTER)
            orderDetail.heading("Quantity", text="Quantity")


            orderDetail.column("unitPrice", width=150, minwidth=100, anchor=tk.CENTER)
            orderDetail.heading("unitPrice", text="unitPrice")

            orderDetail.pack(side=LEFT, fill=BOTH)
            treeScroll.config(command=orderDetail.yview)
            showOrderDetails()

            conn.commit()
            conn.close()

    def showOrderDetails(): #ITS NOT INSERTING BY COLUMNS, NEED CODE

        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        c.execute('''SELECT COUNT(p.sku) FROM products p
                        INNER JOIN orderLines oL on p.SKU = oL.SKU
                        INNER JOIN orders o on o.orderId = oL.orderId
                WHERE o.orderID = ?''',(mycart[0],))
        count = c.fetchone()
        num = count[0]


        c.execute('''SELECT p.prodDesc
                        FROM products p
                            INNER JOIN vendorPrices vP on p.SKU = vP.SKU
                            INNER JOIN orderLines oL on p.SKU = oL.SKU
                            INNER JOIN orders o on o.orderId = oL.orderId
                    WHERE o.orderID = ?
                    GROUP BY p.prodDesc''',(mycart[0],))
        prodDescs = c.fetchall()

        for i in range(0, int(num)):
            orderDetail.insert("", tk.END, values=prodDescs[i])


        c.execute('''SELECT oL.itemQuantity
                            FROM products p
                                INNER JOIN vendorPrices vP on p.SKU = vP.SKU
                                INNER JOIN orderLines oL on p.SKU = oL.SKU
                                INNER JOIN orders o on o.orderId = oL.orderId
                        WHERE o.orderID = ?
                        GROUP BY p.prodDesc''',(mycart[0],))

        quantity = c.fetchall()

        for i in range(0, int(num)):
            orderDetail.insert("", tk.END, values=quantity[i])


        c.execute('''SELECT vP.unitListPrice
                            FROM products p
                                INNER JOIN vendorPrices vP on p.SKU = vP.SKU
                                INNER JOIN orderLines oL on p.SKU = oL.SKU
                                INNER JOIN orders o on o.orderId = oL.orderId
                        WHERE o.orderID = ?
                        GROUP BY p.prodDesc''',(mycart[0],))

        prices = c.fetchall()


        for i in range(0, int(num)):
            orderDetail.insert("",'end', values = prices[i])

        conn.commit()
        conn.close()




    # Add item to product button function
    def submitAddProduct():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        c.execute("INSERT INTO products VALUES (:sku,:desc,:url, :quan,:avail, :level, :stock)",
                  {
                      'sku': productbox1.get(),
                      'desc': productbox3.get(),
                      'url': productbox4.get(),
                      'quan': productbox5.get(),
                      'avail': productbox6.get(),
                      'level': productbox7.get(),
                      'stock': productbox8.get(),
                  })

        # Clear the text box
        productbox1.delete(0, END)
        productbox3.delete(0, END)
        productbox4.delete(0, END)
        productbox5.delete(0, END)
        productbox6.delete(0, END)
        productbox7.delete(0, END)
        productbox8.delete(0, END)

        conn.commit()
        conn.close()
        displayCommand()

    def submitAddVendor():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        c.execute("INSERT INTO vendors VALUES (:name, :phone,:email,:address,:URL,:zip)",
                  {
                      'name': vendorbox1.get(),
                      'phone': vendorbox2.get(),
                      'email': vendorbox3.get(),
                      'address': vendorbox4.get(),
                      'URL': vendorbox5.get(),
                      'zip': vendorbox6.get()
                  })
        c.execute("INSERT INTO zipLocations VALUES (:zip, :city, :state)",
                  {
                      'zip': vendorbox6.get(),
                      'city': vendorbox7.get(),
                      'state': vendorbox8.get()
                  })
        # Clear the text box
        vendorbox1.delete(0, END)
        vendorbox2.delete(0, END)
        vendorbox3.delete(0, END)
        vendorbox4.delete(0, END)
        vendorbox5.delete(0, END)
        vendorbox6.delete(0, END)
        vendorbox7.delete(0, END)
        vendorbox8.delete(0, END)
        conn.commit()
        conn.close()
        displayCommand()

    def submitAddVendorPrices():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        uid_str = uuid.uuid4().urn
        id = uid_str[9:]
        c.execute("INSERT INTO vendorPrices VALUES (:price, :vendor,:product,:unitPrice, :timecheck)",
                  {
                      'price': id,
                      'vendor': vendorPricebox2.get(),
                      'product': vendorPricebox3.get(),
                      'unitPrice': vendorPricebox4.get(),
                      'timecheck': vendorPricebox5.get(),
                  })
        vendorPricebox2.delete(0, END)
        vendorPricebox3.delete(0, END)
        vendorPricebox4.delete(0, END)
        vendorPricebox5.delete(0, END)

        conn.commit()
        conn.close()
        displayCommand()


    def submitAddOrder():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        uid_str = uuid.uuid4().urn
        global orderId
        orderId = uid_str[9:]

        c.execute("INSERT INTO orders VALUES (:id, :date,:orderStatus)",
                  {
                      'id': orderId,
                      'date': orderbox2.get(),
                      'orderStatus': orderbox3.get()
                  })
        # Clear the text box
        orderbox1.delete(0, END)
        orderbox2.delete(0, END)
        orderbox3.delete(0, END)

        conn.commit()
        ordersAdd.destroy()
        orderLinesWindowsPopup()



    def submitOrderlines():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        c.execute("INSERT INTO orderLines VALUES (:id, :SKU,:itemQuantity)",
                  {
                      'id': orderId,
                      'SKU': orderlinesbox2.get(),
                      'itemQuantity': orderlinesbox3.get(),
                  })


        c.execute('''UPDATE products
                  SET
                      unitsInStock = :stock + unitsInStock
                    WHERE SKU = :sku''',
                    {
                        'stock': orderlinesbox3.get(),
                        'sku': orderlinesbox2.get(),
                    })

        orderlinesbox2.delete(0, END)
        orderlinesbox3.delete(0, END)

        conn.commit()
        conn.close()
        displayCommand()


    # This def actually make changes to products table in DB
    def submitEditProduct():
        try:
            conn = sqlite3.connect('Hiccups.db')
            c = conn.cursor()
            c.execute('''UPDATE products
                         SET 
                            prodDesc = :name,
                            productURL = :url,
                            quantity = :quan,
                            availability = :avail,
                            reorderLevel = :level,
                            unitsInStock = :stock
                         WHERE SKU = :sku''',
                    {
                           'sku': productEditbox1.get(),
                           'name': productEditbox2.get(),
                           'url': productEditbox3.get(),
                           'quan': productEditbox4.get(),
                           'avail': productEditbox5.get(),
                            'level': productEditbox6.get(),
                            'stock': productEditbox7.get()
                    })
            productEditbox2.delete(0, END)
            productEditbox3.delete(0, END)
            productEditbox4.delete(0, END)
            productEditbox5.delete(0, END)
            productEditbox6.delete(0, END)
            productEditbox7.delete(0, END)


            conn.commit()
            conn.close()
            queryProducts()
        except sqlite3.Error as e:
            print("Failed to update", e)
        # this line below has to be out of try statement
        productsEdit.destroy()
        editConfirmWindow.destroy()

    def submitEditVendor():
        try:
            conn = sqlite3.connect('Hiccups.db')
            c = conn.cursor()
            c.execute('''UPDATE vendors
                         SET phoneNumber = :phone,
                             email = :email,
                             streetAddress = :address,
                             websiteURL = :web,
                             zipCode = :zip
                         WHERE vendorName = :name''',
                      {
                          'name': vendorsEditbox1.get(),
                          'phone': vendorsEditbox2.get(),
                          'email': vendorsEditbox3.get(),
                          'address': vendorsEditbox4.get(),
                          'web': vendorsEditbox5.get(),
                          'zip': vendorsEditbox6.get()
                      })
            vendorsEditbox2.delete(0, END)
            vendorsEditbox3.delete(0, END)
            vendorsEditbox4.delete(0, END)
            vendorsEditbox5.delete(0, END)
            vendorsEditbox6.delete(0, END)

            conn.commit()
            conn.close()
            queryVendors()
        except sqlite3.Error as e:
            print("Failed to update", e)
        # this line below has to be out of try statement
        vendorsEdit.destroy()
        editConfirmWindow.destroy()

    def submitEditOrders():
        try:
            conn = sqlite3.connect('Hiccups.db')
            c = conn.cursor()
            c.execute('''UPDATE orders
                         SET orderDate = :date,
                             orderStatus = :status
                         WHERE orderId = :id''',
                      {
                          'id': ordersEditbox1.get(),
                          'date': ordersEditbox2.get(),
                          'status': ordersEditbox3.get(),
                      })
            ordersEditbox2.delete(0, END)
            ordersEditbox3.delete(0, END)


            conn.commit()
            conn.close()
            queryOrders()
        except sqlite3.Error as e:
            print("Failed to update", e)
        # this line below has to be out of try statement
        ordersEdit.destroy()
        editConfirmWindow.destroy()


    # delete selected after confirmation
    def submitDeleteCommand():
        try:
            conn = sqlite3.connect('Hiccups.db')
            c = conn.cursor()
            c.execute("DELETE from " + columnAxis.currentTable + " WHERE oid = '" + columnAxis.index + "' ")
            conn.commit()
            conn.close()
            queryProducts()
        except sqlite3.Error as e:
            print("Failed to delete", e)
        # this line below has to be out of try statement
        deleteConfirmWindow.destroy()

    def productsAddWindowPopup():
        global productAdd
        productAdd = Tk()
        productAdd.title("Add data to product table")
        productAdd.geometry('%dx%d+%d+%d' % (400, 280, x*1.5, y*1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        global productbox1
        productbox1 = Entry(productAdd, width=30)  # product Code
        productbox1.grid(row=2, column=1, padx=20, pady=(10, 0))
        box1_label = Label(productAdd, text="SKU")
        box1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        global productbox3
        productbox3 = Entry(productAdd, width=30)
        productbox3.grid(row=3, column=1, padx=20, pady=(10, 0))
        global productbox4
        productbox4 = Entry(productAdd, width=30)
        productbox4.grid(row=4, column=1, padx=20, pady=(10, 0))
        global productbox5
        productbox5 = Entry(productAdd, width=30)
        productbox5.grid(row=5, column=1, padx=20, pady=(10, 0))
        global productbox6
        productbox6 = Entry(productAdd, width=30)
        productbox6.grid(row=6, column=1, padx=20, pady=(10, 0))
        global productbox7
        productbox7 = Entry(productAdd, width=30)
        productbox7.grid(row=7, column=1, padx=20, pady=(10, 0))
        global productbox8
        productbox8 = Entry(productAdd, width=30)
        productbox8.grid(row=8, column=1, padx=20, pady=(10, 0))
        # Create labels for display
        box1_label = Label(productAdd, text="SKU")
        box1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        box3_label = Label(productAdd, text="Product Description")
        box3_label.grid(row=3, column=0, padx=20)
        box4_label = Label(productAdd, text="Product URL")
        box4_label.grid(row=4, column=0, padx=20)
        box5_label = Label(productAdd, text="Quantity")
        box5_label.grid(row=5, column=0, padx=20)
        box6_label = Label(productAdd, text="Availability")
        box6_label.grid(row=6, column=0, padx=20)
        box7_label = Label(productAdd, text="Reorder Level")
        box7_label.grid(row=7, column=0, padx=20)
        box8_label = Label(productAdd, text="Units In Stock")
        box8_label.grid(row=8, column=0, padx=20)
        option_Add_btn = Button(productAdd, text="Add Product", command=submitAddProduct)
        option_Add_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

        conn.commit()
        conn.close()

    def vendorsAddWindowPopup():
        global vendorAdd
        vendorAdd = Tk()
        vendorAdd.title("Add New Vendor")
        vendorAdd.geometry('%dx%d+%d+%d' % (400, 300, x*1.5, y*1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        global vendorbox1
        vendorbox1 = Entry(vendorAdd, width=30)  # product Code
        vendorbox1.grid(row=2, column=1, padx=20, pady=(10, 0))
        global vendorbox2
        vendorbox2 = Entry(vendorAdd, width=30)  # product Desc
        vendorbox2.grid(row=3, column=1, padx=20, pady=(10, 0))
        global vendorbox3
        vendorbox3 = Entry(vendorAdd, width=30)  # vendor
        vendorbox3.grid(row=4, column=1, padx=20, pady=(10, 0))
        global vendorbox4
        vendorbox4 = Entry(vendorAdd, width=30)  # category
        vendorbox4.grid(row=5, column=1, padx=20, pady=(10, 0))
        global vendorbox5
        vendorbox5 = Entry(vendorAdd, width=30)  # category
        vendorbox5.grid(row=6, column=1, padx=20, pady=(10, 0))
        global vendorbox6
        vendorbox6 = Entry(vendorAdd, width=30)  # category
        vendorbox6.grid(row=7, column=1, padx=20, pady=(10, 0))
        global vendorbox7
        vendorbox7 = Entry(vendorAdd, width=30)  # category
        vendorbox7.grid(row=8, column=1, padx=20, pady=(10, 0))
        global vendorbox8
        vendorbox8 = Entry(vendorAdd, width=30)  # category
        vendorbox8.grid(row=9, column=1, padx=20, pady=(10, 0))
        # Create labels for display
        vendorbox1_label = Label(vendorAdd, text="Vendor Name")
        vendorbox1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        vendorbox2_label = Label(vendorAdd, text="Phone Number")
        vendorbox2_label.grid(row=3, column=0, padx=20)
        vendorbox3_label = Label(vendorAdd, text="Email")
        vendorbox3_label.grid(row=4, column=0, padx=20)
        vendorbox4_label = Label(vendorAdd, text="Address")
        vendorbox4_label.grid(row=5, column=0, padx=20)
        vendorbox5_label = Label(vendorAdd, text="Web URL")
        vendorbox5_label.grid(row=6, column=0, padx=20)
        vendorbox6_label = Label(vendorAdd, text="Zip Code")
        vendorbox6_label.grid(row=7, column=0, padx=20)
        vendorbox7_label = Label(vendorAdd, text="City")
        vendorbox7_label.grid(row=8, column=0, padx=20)
        vendorbox8_label = Label(vendorAdd, text="State")
        vendorbox8_label.grid(row=9, column=0, padx=20)

        option_Add_btn = Button(vendorAdd, text="Add Vendor info", command=submitAddVendor)
        option_Add_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

        conn.commit()
        conn.close()


    def orderLinesWindowsPopup():
        global orderlinesAdd
        orderlinesAdd = Tk()
        orderlinesAdd.title("Add Item to this order")
        orderlinesAdd.geometry('%dx%d+%d+%d' % (350, 120, x*1.5, y*1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        global orderlinesbox2
        orderlinesbox2 = Entry(orderlinesAdd, width=30)
        orderlinesbox2.grid(row=2, column=1, padx=20, pady=(10, 0))
        global orderlinesbox3
        orderlinesbox3 = Entry(orderlinesAdd, width=30)
        orderlinesbox3.grid(row=3, column=1, padx=20, pady=(10, 0))

        orderlinesbox2_label = Label(orderlinesAdd, text="SKU")
        orderlinesbox2_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        orderlinesbox3_label = Label(orderlinesAdd, text="Item Quantity")
        orderlinesbox3_label.grid(row=3, column=0, padx=20)



        option_Add_btn = Button(orderlinesAdd, text="Add items to Orders", command=submitOrderlines)
        option_Add_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

        conn.commit()
        conn.close()



    def ordersAddWindowPopup():
        global ordersAdd
        ordersAdd = Tk()
        ordersAdd.title("Add record to orders")
        ordersAdd.geometry('%dx%d+%d+%d' % (350, 120, x*1.5, y*1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        global orderbox1
        orderbox1 = Entry(ordersAdd, width=30)
        #orderbox1.grid(row=2, column=1, padx=20, pady=(10, 0))
        global orderbox2
        orderbox2 = Entry(ordersAdd, width=23)
        orderbox2.grid(row=3, column=1, padx=20, pady=(10, 0))
        global orderbox3
        orderbox3 = ttk.Combobox(ordersAdd, values = ["Processing", "Shipped", "Delivered", "Other"])
        orderbox3.grid(row=4, column=1, padx=20, pady=(10, 0))

        orderbox2.insert(0, date.today())


        # Create labels for display
        #orderbox1_label = Label(ordersAdd, text="Order ID")
        #orderbox1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        orderbox2_label = Label(ordersAdd, text="Order Date")
        orderbox2_label.grid(row=3, column=0, padx=20)
        orderbox3_label = Label(ordersAdd, text="Status")
        orderbox3_label.grid(row=4, column=0, padx=20)

        option_Add_btn = Button(ordersAdd, text="Confirm New Order", command=submitAddOrder)
        option_Add_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=20, ipadx=100)


        conn.commit()

    def vendorPricesAddWindowPopup():
        global vendorPriceAdd
        vendorPriceAdd = Tk()
        vendorPriceAdd.title("Add record to VendorPrice")
        vendorPriceAdd.geometry('%dx%d+%d+%d' % (400, 250, x*1.5, y*1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        #global vendorPricebox1
        #vendorPricebox1 = Entry(vendorPriceAdd, width=30)  # product Code
        #vendorPricebox1.grid(row=2, column=1, padx=20, pady=(10, 0))
        global vendorPricebox2
        vendorPricebox2 = Entry(vendorPriceAdd, width=30)  # product Desc
        vendorPricebox2.grid(row=3, column=1, padx=20, pady=(10, 0))
        global vendorPricebox3
        vendorPricebox3 = Entry(vendorPriceAdd, width=30)  # vender
        vendorPricebox3.grid(row=4, column=1, padx=20, pady=(10, 0))
        global vendorPricebox4
        vendorPricebox4 = Entry(vendorPriceAdd, width=30)  # vender
        vendorPricebox4.grid(row=5, column=1, padx=20, pady=(10, 0))
        global vendorPricebox5
        vendorPricebox5 = Entry(vendorPriceAdd, width=30)  # vender
        vendorPricebox5.grid(row=6, column=1, padx=20, pady=(10, 0))
        # Create labels for display
        #vendorPricebox1_label = Label(vendorPriceAdd, text="vendorPriceID")
        #vendorPricebox1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        vendorPricebox2_label = Label(vendorPriceAdd, text="Vendor Name")
        vendorPricebox2_label.grid(row=3, column=0, padx=20)
        vendorPricebox3_label = Label(vendorPriceAdd, text="SKU")
        vendorPricebox3_label.grid(row=4, column=0, padx=20)
        vendorPricebox4_label = Label(vendorPriceAdd, text="unit List Price")
        vendorPricebox4_label.grid(row=5, column=0, padx=20)
        vendorPricebox5_label = Label(vendorPriceAdd, text="Time Checked")
        vendorPricebox5_label.grid(row=6, column=0, padx=20)

        option_Add_btn = Button(vendorPriceAdd, text="Add to Vendor Price List", command=submitAddVendorPrices)
        option_Add_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

        conn.commit()
        conn.close()
    # this def pop-up window for user to edit items in products
    def productEditWindowPopup():
        global productsEdit
        productsEdit = Tk()
        productsEdit.title("Edit highlighted Products")
        productsEdit.geometry('%dx%d+%d+%d' % (400, 280, x*1.5, y*1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        selectColumn = display_Products_ContentTree.focus()

        valuesInColumn = display_Products_ContentTree.item(selectColumn, "values")
        global productEditbox1
        productEditbox1 = Entry(productsEdit, width=30)  # product Code
        # productEditbox1.grid(row=2, column=1, padx=20, pady=(10, 0))
        global productEditbox2
        productEditbox2 = Entry(productsEdit, width=30)  # product Desc
        productEditbox2.grid(row=3, column=1, padx=20, pady=(10, 0))
        global productEditbox3
        productEditbox3 = Entry(productsEdit, width=30)
        productEditbox3.grid(row=4, column=1, padx=20, pady=(10, 0))
        global productEditbox4
        productEditbox4 = Entry(productsEdit, width=30)
        productEditbox4.grid(row=5, column=1, padx=20, pady=(10, 0))
        global productEditbox5
        productEditbox5 = Entry(productsEdit, width=30)
        productEditbox5.grid(row=6, column=1, padx=20, pady=(10, 0))
        global productEditbox6
        productEditbox6 = Entry(productsEdit, width=30)
        productEditbox6.grid(row=7, column=1, padx=20, pady=(10, 0))
        global productEditbox7
        productEditbox7 = Entry(productsEdit, width=30)
        productEditbox7.grid(row=8, column=1, padx=20, pady=(10, 0))

        # Create labels for display
        # box1_label = Label(productsEdit, text="SKU")
        # box1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        box3_label = Label(productsEdit, text="Product Description")
        box3_label.grid(row=3, column=0, padx=20)
        box4_label = Label(productsEdit, text="Product URL")
        box4_label.grid(row=4, column=0, padx=20)
        box5_label = Label(productsEdit, text="Quantity")
        box5_label.grid(row=5, column=0, padx=20)
        box6_label = Label(productsEdit, text="Availability")
        box6_label.grid(row=6, column=0, padx=20)
        box7_label = Label(productsEdit, text="Reorder Level")
        box7_label.grid(row=7, column=0, padx=20)
        box8_label = Label(productsEdit, text="Units In Stock")
        box8_label.grid(row=8, column=0, padx=20)
        option_edit_btn = Button(productsEdit, text="Save Edit", command=editComfirm)
        option_edit_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=20, ipadx=100)
        productEditbox1.insert(0, valuesInColumn[0])
        productEditbox2.insert(0, valuesInColumn[1])
        productEditbox3.insert(0, valuesInColumn[2])
        productEditbox4.insert(0, valuesInColumn[3])
        productEditbox5.insert(0, valuesInColumn[4])
        productEditbox6.insert(0, valuesInColumn[5])
        productEditbox7.insert(0, valuesInColumn[6])


        conn.commit()
        conn.close()

    def vendorsEditWindowPopup():
        global vendorsEdit
        vendorsEdit = Tk()
        vendorsEdit.title("Edit highlighted Vendor")
        vendorsEdit.geometry('%dx%d+%d+%d' % (400, 280, x*1.5, y*1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        selectColumn = display_Vendors_ContentTree.focus()

        valuesInColumn = display_Vendors_ContentTree.item(selectColumn, "values")
        global vendorsEditbox1
        vendorsEditbox1 = Entry(vendorsEdit, width=30)  # product Code
        # productEditbox1.grid(row=2, column=1, padx=20, pady=(10, 0))
        global vendorsEditbox2
        vendorsEditbox2 = Entry(vendorsEdit, width=30)  # product Desc
        vendorsEditbox2.grid(row=3, column=1, padx=20, pady=(10, 0))
        global vendorsEditbox3
        vendorsEditbox3 = Entry(vendorsEdit, width=30)
        vendorsEditbox3.grid(row=4, column=1, padx=20, pady=(10, 0))
        global vendorsEditbox4
        vendorsEditbox4 = Entry(vendorsEdit, width=30)
        vendorsEditbox4.grid(row=5, column=1, padx=20, pady=(10, 0))
        global vendorsEditbox5
        vendorsEditbox5 = Entry(vendorsEdit, width=30)
        vendorsEditbox5.grid(row=6, column=1, padx=20, pady=(10, 0))
        global vendorsEditbox6
        vendorsEditbox6 = Entry(vendorsEdit, width=30)
        vendorsEditbox6.grid(row=7, column=1, padx=20, pady=(10, 0))
        # Create labels for display
        # box1_label = Label(productsEdit, text="Product Code")
        # box1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        box2_label = Label(vendorsEdit, text="Phone Number")
        box2_label.grid(row=3, column=0, padx=20)
        box3_label = Label(vendorsEdit, text="Email")
        box3_label.grid(row=4, column=0, padx=20)
        box4_label = Label(vendorsEdit, text="Address")
        box4_label.grid(row=5, column=0, padx=20)
        box5_label = Label(vendorsEdit, text="Web URL")
        box5_label.grid(row=6, column=0, padx=20)
        box6_label = Label(vendorsEdit, text="Zip Code")
        box6_label.grid(row=7, column=0, padx=20)
        option_edit_btn = Button(vendorsEdit, text="Save Edit", command=editComfirm)
        option_edit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=20, ipadx=100)
        vendorsEditbox1.insert(0, valuesInColumn[0])
        vendorsEditbox2.insert(0, valuesInColumn[1])
        vendorsEditbox3.insert(0, valuesInColumn[2])
        vendorsEditbox4.insert(0, valuesInColumn[3])
        vendorsEditbox5.insert(0, valuesInColumn[4])
        vendorsEditbox6.insert(0, valuesInColumn[5])
        conn.commit()
        conn.close()

    def ordersEditWindowPopup(): # fill this edit
        global ordersEdit
        ordersEdit = Tk()
        ordersEdit.title("Edit highlighted order")
        ordersEdit.geometry('%dx%d+%d+%d' % (350, 120, x * 1.5, y * 1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        selectColumn = display_Orders_ContentTree.focus()

        valuesInColumn = display_Orders_ContentTree.item(selectColumn, "values")
        global ordersEditbox1
        ordersEditbox1 = Entry(ordersEdit, width=30)  # This box is invisible so user cannot edit the Primary Key
        # productEditbox1.grid(row=2, column=1, padx=20, pady=(10, 0))
        global ordersEditbox2
        ordersEditbox2 = Entry(ordersEdit, width=30)  # product Desc
        ordersEditbox2.grid(row=3, column=1, padx=20, pady=(10, 0))
        global ordersEditbox3
        ordersEditbox3 = ttk.Combobox(ordersEdit, values = ["Processing", "Shipped", "Delivered", "Other"])
        ordersEditbox3.grid(row=4, column=1, padx=20, pady=(10, 0), ipadx =20)



        # Create labels for display
        # box1_label = Label(productsEdit, text="Order ID")
        # box1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        box2_label = Label(ordersEdit, text="Order Date")
        box2_label.grid(row=3, column=0, padx=20)
        box3_label = Label(ordersEdit, text="Order Status")
        box3_label.grid(row=4, column=0, padx=20)

        option_edit_btn = Button(ordersEdit, text="Save Edit", command=editComfirm)
        option_edit_btn.grid(row=8, column=0, columnspan=2, pady=10, padx=20, ipadx=100)
        ordersEditbox1.insert(0, valuesInColumn[0])
        ordersEditbox2.insert(0, valuesInColumn[1])
        ordersEditbox3.insert(0, valuesInColumn[2])
        conn.commit()
        conn.close()

    # This confirmation window shows up when user try to save changes in Edit Window
    def editComfirm():
        global editConfirmWindow
        editConfirmWindow = tk.Tk()
        editConfirmWindow.title('Edit Confirm')
        editConfirmWindow.geometry('%dx%d+%d+%d' % (310, 140, x*1.5, y*1.5))
        confirm_message = Label(editConfirmWindow, text=" Are you sure you want to save changes?", padx=10, pady=10)
        confirm_message.grid(row=0, column=0, pady=10)
        yesNoBox = Frame(editConfirmWindow)
        yesNoBox.grid(row=1, column=0, padx=20, pady=(10, 0))
        edit_yes_button = Button(yesNoBox, text="Yes", command=submitEditCommand)
        edit_yes_button.grid(row=0, column=0, columnspan=2, pady=5, padx=1, ipadx=50)
        edit_no_button = Button(yesNoBox, text="No", command=editConfirmWindow.destroy)
        edit_no_button.grid(row=0, column=2, columnspan=2, pady=5, padx=1, ipadx=50)


    def deleteConfirm():  # need to MODIFY values in column when table content changes!!!!
        try:
            global deleteConfirmWindow
            deleteConfirmWindow = tk.Tk()
            deleteConfirmWindow.title('Delete Confirm')
            deleteConfirmWindow.geometry('%dx%d+%d+%d' % (310, 140, x*1.5, y*1.5))
            #Issue fixed
            global columnAxis
            if (tableOndisplay.currentTable == "products"):
                    selectColumn = display_Products_ContentTree.focus()
                    valuesInColumn = display_Products_ContentTree.item(selectColumn, "values")
                    columnAxis = treeCurrentdisplay("products", valuesInColumn[7])
            elif (tableOndisplay.currentTable == "vendors"):
                    selectColumn = display_Vendors_ContentTree.focus()
                    valuesInColumn = display_Vendors_ContentTree.item(selectColumn, "values")
                    columnAxis = treeCurrentdisplay("vendors", valuesInColumn[6])
            elif (tableOndisplay.currentTable == "orders"):
                    selectColumn = display_Orders_ContentTree.focus()
                    valuesInColumn = display_Orders_ContentTree.item(selectColumn, "values")
                    columnAxis = treeCurrentdisplay("orders", valuesInColumn[2])
            elif (tableOndisplay.currentTable == "vendorPrices"):
                    selectColumn = display_VendorPrices_ContentTree.focus()
                    valuesInColumn = display_VendorPrices_ContentTree.item(selectColumn, "values")
                    columnAxis = treeCurrentdisplay("vendorPrices", valuesInColumn[5])
            print(selectColumn)
            confirm_message = Label(deleteConfirmWindow, text="Are you sure you want to delete selected column?", padx=10, pady=10)
            confirm_message.grid(row=0, column=0, pady=10)
            yesNoBox = Frame(deleteConfirmWindow)
            yesNoBox.grid(row=1, column=0, padx=20, pady=(10, 0))
            edit_yes_button = Button(yesNoBox, text="Yes", command=submitDeleteCommand)
            edit_yes_button.grid(row=0, column=0, columnspan=2, pady=5, padx=1, ipadx=50)
            edit_no_button = Button(yesNoBox, text="No", command=deleteConfirmWindow.destroy)
            edit_no_button.grid(row=0, column=2, columnspan=2, pady=5, padx=1, ipadx=50)
        except:
            deleteConfirmWindow.destroy()
            messagebox.showerror("Failed","This cannot be deleted!")

    def displayProductsWindowSetUp():
        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("products", "")
        global display_Products_ContentTree
        display_Products_ContentTree = ttk.Treeview(tab, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings', height=15)
        display_Products_ContentTree.column("#1", width=120, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#1", text="SKU")
        display_Products_ContentTree.column("#2", width=400, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#2", text="Prod Description")
        display_Products_ContentTree.column("#3", width=130, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#3", text="Product URL")
        display_Products_ContentTree.column("#4", width=100, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#4", text="Quantity")
        display_Products_ContentTree.column("#5", width=100, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#5", text="Availability")
        display_Products_ContentTree.column("#6", width=100, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#6", text="Reorder Level")
        display_Products_ContentTree.column("#7", width=50, minwidth=50, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#7", text="Stock")

        display_Products_ContentTree.grid(row=0, column=0, padx=50, pady=20)
        root.geometry("1500x600")

    def displayVendorsWindowSetUp():
        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("vendors", "")
        global display_Vendors_ContentTree
        display_Vendors_ContentTree = ttk.Treeview(tab, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"), show='headings', height=15)
        display_Vendors_ContentTree.column("#1", width=100, minwidth=70, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#1", text="Vendor Name")
        display_Vendors_ContentTree.column("#2", width=100, minwidth=90, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#2", text="Phone Number")
        display_Vendors_ContentTree.column("#3", width=150, minwidth=100, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#3", text="Email")
        display_Vendors_ContentTree.column("#4", width=200, minwidth=100, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#4", text="Address")
        display_Vendors_ContentTree.column("#5", width=100, minwidth=100, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#5", text="Zip Code")
        display_Vendors_ContentTree.column("#6", width=100, minwidth=90, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#6", text="City")
        display_Vendors_ContentTree.column("#7", width=50, minwidth=60, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#7", text="State")
        display_Vendors_ContentTree.column("#8", width=200, minwidth=90, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#8", text="Web URL")

        display_Vendors_ContentTree.grid(row=0, column=0, padx=50, pady=20)
        root.geometry("1500x600")

    def displayOrdersWindowSetUp():
        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("orders", "")
        global display_Orders_ContentTree
        display_Orders_ContentTree = ttk.Treeview(tab, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=15)
        display_Orders_ContentTree.column("#1", width=250, minwidth=150, anchor=tk.CENTER)
        display_Orders_ContentTree.heading("#1", text="Order ID")
        display_Orders_ContentTree.column("#2", width=200, minwidth=80, anchor=tk.CENTER)
        display_Orders_ContentTree.heading("#2", text="Order Date")
        display_Orders_ContentTree.column("#3", width=150, minwidth=100, anchor=tk.CENTER)
        display_Orders_ContentTree.heading("#3", text="Order Status")
        display_Orders_ContentTree.column("#4", width=200, minwidth=80, anchor=tk.CENTER)
        display_Orders_ContentTree.heading("#4", text="Total Quantity")
        display_Orders_ContentTree.column("#5", width=200, minwidth=80, anchor=tk.CENTER)
        display_Orders_ContentTree.heading("#5", text="Order Total")


        display_Orders_ContentTree.grid(row=0, column=0, padx=50, pady=20)
        root.geometry("1500x600")


    def displayVendorPricesWindowSetUp():
        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("vendorPrices", "")
        global display_VendorPrices_ContentTree
        display_VendorPrices_ContentTree = ttk.Treeview(tab, column=("c1", "c2", "c3", "c4"), show='headings', height=15)
        display_VendorPrices_ContentTree.column("#1", width=250, minwidth=150, anchor=tk.CENTER)
        display_VendorPrices_ContentTree.heading("#1", text="Vendor")
        display_VendorPrices_ContentTree.column("#2", width=300, minwidth=80, anchor=tk.CENTER)
        display_VendorPrices_ContentTree.heading("#2", text="Product")
        display_VendorPrices_ContentTree.column("#3", width=150, minwidth=100, anchor=tk.CENTER)
        display_VendorPrices_ContentTree.heading("#3", text="Unit List Price")
        display_VendorPrices_ContentTree.column("#4", width=300, minwidth=100, anchor=tk.CENTER)
        display_VendorPrices_ContentTree.heading("#4", text="Time Checked")


        display_VendorPrices_ContentTree.grid(row=0, column=0, padx=50, pady=20)
        root.geometry("1500x600")

    def displayMainPageQueryWindowSetUp():

        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("Product on Market", "")
        global mainPageQuery_ContentTree
        mainPageQuery_ContentTree = ttk.Treeview(tab, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=15)
        mainPageQuery_ContentTree.column("#1", width=150, minwidth=80, anchor=tk.CENTER)
        mainPageQuery_ContentTree.heading("#1", text="Vendor")
        mainPageQuery_ContentTree.column("#2", width=150, minwidth=80, anchor=tk.CENTER)
        mainPageQuery_ContentTree.heading("#2", text="SKU")
        mainPageQuery_ContentTree.column("#3", width=400, minwidth=100, anchor=tk.CENTER)
        mainPageQuery_ContentTree.heading("#3", text="product Description")
        mainPageQuery_ContentTree.column("#4", width=150, minwidth=100, anchor=tk.CENTER)
        mainPageQuery_ContentTree.heading("#4", text="Unit List Price")
        mainPageQuery_ContentTree.column("#5", width=150, minwidth=100, anchor=tk.CENTER)
        mainPageQuery_ContentTree.heading("#5", text="Time Checked")
        mainPageQuery_ContentTree.grid(row=0, column=0, padx=50, pady=20)

        root.geometry("1500x600")



    # Main Screen Labels
    main_table_select_label = Label(mainOptionFrame, text="Choose Table")
    main_table_select_label.grid(row=1, column=0, pady=10, padx=1)
    main_sortBy_label = Label(mainOptionFrame, text="Sort by")
    main_sortBy_label.grid(row=7, column=0)
    # Insert data button in Main screen
    main_insert_button = Button(mainOptionFrame, text="Add Data to Table", command=addCommand, bg = 'light gray', fg = 'black')
    main_insert_button.grid(row=3, column=0, columnspan=2, pady=10, padx=1, ipadx=70)
    # Display table button in Main screen
    main_select_display = Button(mainOptionFrame, text="Display Table", command=displayCommand, bg = 'light gray', fg = 'black')
    main_select_display.grid(row=2, column=0, columnspan=2, pady=10, padx=1, ipadx=83)
    # Edit button in Main Screen
    main_edit_button = Button(mainOptionFrame, text="Edit selected Column", command=editCommand, bg = 'light gray', fg = 'black')
    main_edit_button.grid(row=5, column=0, columnspan=2, pady=10, padx=1, ipadx=62)
    # Sort button in Main Screen
    main_sort_button = Button(mainOptionFrame, text="Sort", command=sortCommand, bg = 'light gray', fg = 'black')
    main_sort_button.grid(row=8, column=0, columnspan=2, pady=10, padx=1, ipadx=112) # row 6 is left for drop down

    # Delete button in Main Screen
    main_delete_button = Button(mainOptionFrame, text="Delete Selected Column", command=deleteConfirm, bg = 'light gray', fg = 'black')
    main_delete_button.grid(row=6, column=0, columnspan=2, pady=10, padx=1, ipadx=55)
    main_backToMainPage_button = Button(mainOptionFrame, text="Back to Summary Table", command=backToSummaryDisplay, bg = 'light gray', fg = 'black')
    main_backToMainPage_button.grid(row=10, column=0, columnspan=2, pady=10, padx=1, ipadx=60)


    def queryStock():
        treeRemove()
        displayProductsWindowSetUp()
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        # Query DB
        c.execute("SELECT * FROM products WHERE unitsInStock != 0 OR unitsInStock != 0.0 ORDER BY unitsInStock")
        records = c.fetchall()

        for row in display_Products_ContentTree.get_children():
            display_Products_ContentTree.delete(row)

        for row in records:
            print(row)
            display_Products_ContentTree.insert("", tk.END, values=row)
        conn.commit()
        conn.close()

    def queryActiveOrders():
        treeRemove()
        displayOrdersWindowSetUp()
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        # Query DB
        try:
                c.execute('''SELECT o.orderID, o.orderDate, o.orderStatus,
                                (SELECT SUM(oL.itemQuantity)
                                    FROM orderLines oL
                                WHERE o.orderId =oL.orderId )AS "Total Quantity",
                               (SELECT total FROM (SELECT DISTINCT (p.sku), unitListPrice * oL.itemQuantity AS total)) AS total
                            FROM orders o
                                INNER JOIN orderLines oL on o.orderId = oL.orderId
                                INNER JOIN products p on p.SKU = oL.SKU
                                INNER JOIN vendorPrices vP on p.SKU = vP.SKU
                        WHERE orderStatus != 'Delivered'
                        GROUP BY o.orderID, o.orderDate
                        ORDER BY o.orderDate;''')
                records = c.fetchall()
                for row in display_Orders_ContentTree.get_children():
                    display_Orders_ContentTree.delete(row)

                for row in records:
                    print(row)
                    display_Orders_ContentTree.insert("", tk.END, values=row)
        except:
            messagebox.showwarning('Whoops','There are no active orders')

        conn.commit()
        conn.close()

    check_stock_button = Button(mainOptionFrame, text="Inventory", command=queryStock, bg = 'light gray', fg = 'black')
    check_stock_button.grid(row=11, column=0, columnspan=2, pady=10, padx=1, ipadx=100)

    check_active_orders_button = Button(mainOptionFrame, text="Active Orders", command=queryActiveOrders, bg = 'light gray', fg = 'black')
    check_active_orders_button.grid(row=12, column=0, columnspan=2, pady=10, padx=1, ipadx=90)

    add_cart_button = Button(mainOptionFrame, text="Add Cart", command=addCart,
                                        bg='light gray', fg='black')
    add_cart_button.grid(row=13, column=0, columnspan=1, pady=10, padx=1, ipadx=55)

    add_cart_button = Button(mainOptionFrame, text="Clear Cart", command=newCart,
                                        bg='light gray', fg='black')
    add_cart_button.grid(row=13, column=1, columnspan=1, pady=10, padx=1, ipadx=55)

    add_cart_button = Button(mainOptionFrame, text="Show Cart", command=DisplayCartWindowPopUp,
                                        bg='light gray', fg='black')
    add_cart_button.grid(row=14, column=0, columnspan=1, pady=10, padx=1, ipadx=52)

    add_cart_button = Button(mainOptionFrame, text="Place Order", command=PlaceOrder,
                             bg='light gray', fg='black')
    add_cart_button.grid(row=14, column=1, columnspan=1, pady=10, padx=1, ipadx=52)

    '''button = Button(mainOptionFrame, text="Place Order", command=get_bestware_products(),
                             bg='light gray', fg='black')
    button.grid(row=15, column=0, columnspan=1, pady=10, padx=1, ipadx=52)'''

    # Initial display
    displayMainPageQueryWindowSetUp()
    mainPageQuery()


    # things to be implemented
    #0. ADDING NEW ORDERS NOW HAVE DEFAULT DATE
    #(DONE) 1.DROPDOWN for status when adding new orders, to choose from "processing", "shipped", "delivered", "other"
    #(DONE) ADD INVENTORY & ACTIVE ORDERS BUTTON
    #(DONE) 2.Scroll Bar for all tables
    #(DONE) HIGHLIGHT COLORS OF BUTTON
    #(DONE) WIDEN the data for clear visual
    #(DONE) DOUBLE-CLICK NOWS CAN OPEN WEBSITE FROM CART MENU
    # 3.Connect to csv file by using python  (integrate web crawler to the python)
    # 4.csv file should be corresponding to the implementation for easier import process
    # 5.generate pdf report
    # 6. (OPTIONAL) advanced query based on user filter (products and vendorprices and orders table only)
    # 7. display orderlines by select a specific order low (either double clicking or an extra option)
    # 8. low stock alert
    # 9. sort product by popularity by order history
    #(DONE)10. display active orders
    #(DONE) 11.add to cart

    #thins to enhance
    #(SOLVED) 1. switching tables have some displaying problems
    # 2. make the colors of the odd and even columns different
    # 3. (advanced) right-click to select to edit


    # ORDERDETAIL NEEDS IMPLEMENTATION

    conn.commit()

    # Close our connection
    conn.close()
