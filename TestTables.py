import uuid
from functools import partial
from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3


def MainScreen(tab, root):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (1400 / 2)
    y = (hs / 2) - (700 / 2)
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
        currentSelectedTable = mainComboDropdown.get()
        print("In ADD table " + currentSelectedTable)
        if (currentSelectedTable == "Products"):  # if dropdown selected table then
            print("Yes Products Add is selected")
            productsAddWindowPopup()
        elif (currentSelectedTable == "Vendors"):
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
        if (currentSelectedTable != "Products"):
            try:
                display_Products_ContentTree.destroy()
                print("ProductTree Gone")
            except:
                print("Tree not defined")
        if (currentSelectedTable != "Orders"):
            try:
                display_Orders_ContentTree.destroy()
                print("OrderTree Gone")
            except:
                print("Tree not defined")
        if (currentSelectedTable != "Vendor Price"):
            try:
                display_VendorPrices_ContentTree.destroy()
                print("VendorPriceTree Gone")
            except:
                print("Tree not defined")

        if (currentSelectedTable != "Vendors"):
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
        elif (tableOndisplay.currentTable == "vendors"):
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

    def sortCommand():  ####################### Comand list for sort in certain type ################################
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
            # print(row)
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
            # print(row)
            display_Vendors_ContentTree.insert("", tk.END, values=row)
        conn.commit()
        conn.close()

    def queryOrders():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()
        # Query DB
        c.execute('''SELECT o.orderID, o.orderDate, o.orderStatus,
                    (SELECT COUNT(oL.sku)
                        FROM orderLines oL
                        WHERE o.orderId =oL.orderId )AS number_of_items,
                        ROUND(SUM(unitListPrice * oL.unitSalePrice)/2, 2) AS total
                    FROM orders o
                        INNER JOIN orderLines oL on o.orderId = oL.orderId
                        INNER JOIN products p on p.SKU = oL.SKU
                        INNER JOIN vendorPrices vP on p.SKU = vP.SKU
                GROUP BY o.orderID, o.orderDate''')
        records = c.fetchall()

        for row in display_Orders_ContentTree.get_children():
            display_Orders_ContentTree.delete(row)

        for row in records:
            # print(row)
            display_Orders_ContentTree.insert("", tk.END, values=row)
        conn.commit()
        conn.close()

    def mainPageQuery(opt='REGULAR'):
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
        elif (opt == 'L2H'):
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
            # print(row)
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
            # print(row)
            display_VendorPrices_ContentTree.insert("", tk.END, values=row)
        conn.commit()
        conn.close()

    # DoubleClicked function
    def doubleClicked(event):
        if (tableOndisplay.currentTable == "Product on Market"):
            region = mainPageQuery_ContentTree.identify_column(event.x)
            print("Sort Flag is " + summaryFlag.flag)
            if region == "#4":
                if summaryFlag.flag == "off":
                    mainPageQuery("L2H")
                    summaryFlag.flag = "on"
                elif summaryFlag.flag == "on":
                    mainPageQuery("H2L")
                    summaryFlag.flag = "off"
        elif(tableOndisplay.currentTable == "orders"):
            region = display_Orders_ContentTree.identify_column(event.x)
            print(region)
            orderDetailWindowPop()

    # Add item to product button function
    def submitAddProduct():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        c.execute("INSERT INTO products VALUES (:sku, :cate,:desc,:url, :quan,:avail, :level, :stock)",
                  {
                      'sku': productbox1.get(),
                      'cate': productbox2.get(),
                      'desc': productbox3.get(),
                      'url': productbox4.get(),
                      'quan': productbox5.get(),
                      'avail': productbox6.get(),
                      'level': productbox7.get(),
                      'stock': productbox8.get(),
                  })
        c.execute("INSERT INTO categories VALUES (:name)",
                  {
                      'name': productbox2.get()
                  })
        # Clear the text box
        productbox1.delete(0, END)
        productbox2.delete(0, END)
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
                      'orderStatus': orderStatusDropDown.get()
                  })
        # Clear the text box
        orderbox1.delete(0, END)
        orderbox2.delete(0, END)
        # orderbox3.delete(0, END)

        conn.commit()
        ordersAdd.destroy()
        orderLinesWindowsPopup()

    def submitOrderlines():
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        c.execute("INSERT INTO orderLines VALUES (:id, :SKU,:unitSalePrice)",
                  {
                      'id': orderId,
                      'SKU': orderlinesbox2.get(),
                      'unitSalePrice': orderlinesbox3.get(),
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
                            category = :cate,
                            prodDesc = :name,
                            productURL = :url,
                            quantity = :quan,
                            availability = :avail,
                            reorderLevel = :level,
                            unitsInStock = :stock
                         WHERE SKU = :sku''',
                      {
                          'sku': productEditbox1.get(),
                          'cate': productEditbox2.get(),
                          'name': productEditbox3.get(),
                          'url': productEditbox4.get(),
                          'quan': productEditbox5.get(),
                          'avail': productEditbox6.get(),
                          'level': productEditbox7.get(),
                          'stock': productEditbox8.get()
                      })
            productEditbox2.delete(0, END)
            productEditbox3.delete(0, END)
            productEditbox4.delete(0, END)
            productEditbox5.delete(0, END)
            productEditbox6.delete(0, END)
            productEditbox7.delete(0, END)
            productEditbox8.delete(0, END)

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
                          'status': orderStatusDropDown.get(),
                      })
            ordersEditbox2.delete(0, END)


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
        productAdd.geometry('%dx%d+%d+%d' % (400, 280, x * 1.5, y * 1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        global productbox1
        productbox1 = Entry(productAdd, width=30)  # product Code
        productbox1.grid(row=2, column=1, padx=20, pady=(10, 0))
        global productbox2
        productbox2 = Entry(productAdd, width=30)  # product Desc
        productbox2.grid(row=3, column=1, padx=20, pady=(10, 0))
        global productbox3
        productbox3 = Entry(productAdd, width=30)
        productbox3.grid(row=4, column=1, padx=20, pady=(10, 0))
        global productbox4
        productbox4 = Entry(productAdd, width=30)
        productbox4.grid(row=5, column=1, padx=20, pady=(10, 0))
        global productbox5
        productbox5 = Entry(productAdd, width=30)
        productbox5.grid(row=6, column=1, padx=20, pady=(10, 0))
        global productbox6
        productbox6 = Entry(productAdd, width=30)
        productbox6.grid(row=7, column=1, padx=20, pady=(10, 0))
        global productbox7
        productbox7 = Entry(productAdd, width=30)
        productbox7.grid(row=8, column=1, padx=20, pady=(10, 0))
        global productbox8
        productbox8 = Entry(productAdd, width=30)
        productbox8.grid(row=9, column=1, padx=20, pady=(10, 0))
        # Create labels for display
        box1_label = Label(productAdd, text="SKU")
        box1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        box2_label = Label(productAdd, text="Category")
        box2_label.grid(row=3, column=0, padx=20)
        box3_label = Label(productAdd, text="Product Description")
        box3_label.grid(row=4, column=0, padx=20)
        box4_label = Label(productAdd, text="Product URL")
        box4_label.grid(row=5, column=0, padx=20)
        box5_label = Label(productAdd, text="Quantity")
        box5_label.grid(row=6, column=0, padx=20)
        box6_label = Label(productAdd, text="Availability")
        box6_label.grid(row=7, column=0, padx=20)
        box7_label = Label(productAdd, text="Reorder Level")
        box7_label.grid(row=8, column=0, padx=20)
        box8_label = Label(productAdd, text="Units In Stock")
        box8_label.grid(row=9, column=0, padx=20)
        option_Add_btn = Button(productAdd, text="Add Product", command=submitAddProduct)
        option_Add_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

        conn.commit()
        conn.close()

    def vendorsAddWindowPopup():
        global vendorAdd
        vendorAdd = Tk()
        vendorAdd.title("Add New Vendor")
        vendorAdd.geometry('%dx%d+%d+%d' % (400, 300, x * 1.5, y * 1.5))
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
        orderlinesAdd.geometry('%dx%d+%d+%d' % (400, 250, x * 1.5, y * 1.5))
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
        orderlinesbox3_label = Label(orderlinesAdd, text="Unit Sale Price")
        orderlinesbox3_label.grid(row=3, column=0, padx=20)

        option_Add_btn = Button(orderlinesAdd, text="Add items to Orders", command=submitOrderlines)
        option_Add_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=20, ipadx=100)

        conn.commit()
        conn.close()

    def ordersAddWindowPopup():
        displayMainPageQueryWindowSetUp()
        mainPageQuery()

        global ordersAdd
        ordersAdd = Tk()
        ordersAdd.title("Add record to orders")
        ordersAdd.geometry('%dx%d+%d+%d' % (400, 200, x * 1.5, y * 1.5))
        # Drop down for the addOrder and EditOrder window
        global orderStatusDropDown
        global statusList
        statusList = ["Processing", "Shipped", "Delivered", "Other"]
        orderStatusDropDown = ttk.Combobox(ordersAdd, value=statusList)
        orderStatusDropDown.bind("<<ComboboxSelected>>")
        orderStatusDropDown.grid(row=4, column=1, pady=(10, 0), padx=1)

        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        global orderbox1
        orderbox1 = Entry(ordersAdd, width=30)
        # orderbox1.grid(row=2, column=1, padx=20, pady=(10, 0))
        global orderbox2
        orderbox2 = Entry(ordersAdd, width=30)
        orderbox2.grid(row=3, column=1, padx=20, pady=(10, 0))
        global orderbox3
        orderbox3 = Entry(ordersAdd, width=30)
        #orderbox3.grid(row=4, column=1, padx=20, pady=(10, 0))

        # Create labels for display
        # orderbox1_label = Label(ordersAdd, text="Order ID")
        # orderbox1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
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
        vendorPriceAdd.geometry('%dx%d+%d+%d' % (400, 250, x * 1.5, y * 1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        # global vendorPricebox1
        # vendorPricebox1 = Entry(vendorPriceAdd, width=30)  # product Code
        # vendorPricebox1.grid(row=2, column=1, padx=20, pady=(10, 0))
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
        # vendorPricebox1_label = Label(vendorPriceAdd, text="vendorPriceID")
        # vendorPricebox1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
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
        productsEdit.geometry('%dx%d+%d+%d' % (400, 280, x * 1.5, y * 1.5))
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
        global productEditbox8
        productEditbox8 = Entry(productsEdit, width=30)
        productEditbox8.grid(row=9, column=1, padx=20, pady=(10, 0))
        # Create labels for display
        # box1_label = Label(productsEdit, text="SKU")
        # box1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        box2_label = Label(productsEdit, text="Category")
        box2_label.grid(row=3, column=0, padx=20)
        box3_label = Label(productsEdit, text="Product Description")
        box3_label.grid(row=4, column=0, padx=20)
        box4_label = Label(productsEdit, text="Product URL")
        box4_label.grid(row=5, column=0, padx=20)
        box5_label = Label(productsEdit, text="Quantity")
        box5_label.grid(row=6, column=0, padx=20)
        box6_label = Label(productsEdit, text="Availability")
        box6_label.grid(row=7, column=0, padx=20)
        box7_label = Label(productsEdit, text="Reorder Level")
        box7_label.grid(row=8, column=0, padx=20)
        box8_label = Label(productsEdit, text="Units In Stock")
        box8_label.grid(row=9, column=0, padx=20)
        option_edit_btn = Button(productsEdit, text="Save Edit", command=editComfirm)
        option_edit_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=20, ipadx=100)
        productEditbox1.insert(0, valuesInColumn[0])
        productEditbox2.insert(0, valuesInColumn[1])
        productEditbox3.insert(0, valuesInColumn[2])
        productEditbox4.insert(0, valuesInColumn[3])
        productEditbox5.insert(0, valuesInColumn[4])
        productEditbox6.insert(0, valuesInColumn[5])
        productEditbox7.insert(0, valuesInColumn[6])
        productEditbox8.insert(0, valuesInColumn[7])
        conn.commit()
        conn.close()

    def vendorsEditWindowPopup():
        global vendorsEdit
        vendorsEdit = Tk()
        vendorsEdit.title("Edit highlighted Vendor")
        vendorsEdit.geometry('%dx%d+%d+%d' % (400, 280, x * 1.5, y * 1.5))
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

    def ordersEditWindowPopup():  # fill this edit
        global ordersEdit
        ordersEdit = Tk()
        ordersEdit.title("Edit highlighted order")
        ordersEdit.geometry('%dx%d+%d+%d' % (400, 280, x * 1.5, y * 1.5))
        global statusList
        global orderStatusDropDown
        statusList = ["Processing", "Shipped", "Delivered", "Other"]
        orderStatusDropDown = ttk.Combobox(ordersEdit, value=statusList)
        orderStatusDropDown.bind("<<ComboboxSelected>>")
        orderStatusDropDown.grid(row=4, column=1, pady=(10, 0), padx=1)

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
        # global ordersEditbox3
        # ordersEditbox3 = Entry(ordersEdit, width=30)
        # ordersEditbox3.grid(row=4, column=1, padx=20, pady=(10, 0))

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

        conn.commit()
        conn.close()

    #order Detail pop-up window
    def orderDetailWindowPop():
        global ordersDetail
        ordersDetail = Tk()
        ordersDetail.title("Detail of order")
        ordersDetail.geometry('%dx%d+%d+%d' % (480, 280, x * 1.5, y * 1.5))
        conn = sqlite3.connect('Hiccups.db')
        c = conn.cursor()

        selectColumn = display_Orders_ContentTree.focus()
        print(selectColumn)
        valuesInColumn = display_Orders_ContentTree.item(selectColumn, "values") # need new query for
        for i in valuesInColumn:
            print(i)
        LocalSKU = str(valuesInColumn[2])
        print("Local SKU is "+LocalSKU)
        #c.execute("SELECT productURL, vendorName, unitListPrice, timeChecked from products inner join vendorPrices where SKU = '" + LocalSKU +"'")
        moreInfo = c.fetchall()
        for i in moreInfo:
            print(i)
        global ordersDetailField1
        ordersDetailField1 = Label(ordersDetail, width=40, text=str(valuesInColumn[0]))  # This box is invisible so user cannot edit the Primary Key
        ordersDetailField1.grid(row=2, column=1, padx=20, pady=(10, 0))
        global ordersDetailField2
        ordersDetailField2 = Label(ordersDetail, width=30, text=str(valuesInColumn[1]))
        ordersDetailField2.grid(row=3, column=1, padx=20, pady=(10, 0))
        global ordersDetailField3
        ordersDetailField3 = Label(ordersDetail, width=30, text=str(valuesInColumn[2]))
        ordersDetailField3.grid(row=4, column=1, padx=20, pady=(10, 0))
        global ordersDetailField4
        ordersDetailField4 = Label(ordersDetail, width=30, text=str(valuesInColumn[3]))
        ordersDetailField4.grid(row=5, column=1, padx=20, pady=(10, 0))
        # Create labels for display
        box1_label = Label(ordersDetail, text="Order ID")
        box1_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        box2_label = Label(ordersDetail, text="Order Date")
        box2_label.grid(row=3, column=0, padx=20)
        box3_label = Label(ordersDetail, text="SKU")
        box3_label.grid(row=4, column=0, padx=20)
        box4_label = Label(ordersDetail, text="Order Status")
        box4_label.grid(row=5, column=0, padx=20)
        conn.commit()
        conn.close()

    # This confirmation window shows up when user try to save changes in Edit Window
    def editComfirm():
        global editConfirmWindow
        editConfirmWindow = tk.Tk()
        editConfirmWindow.title('Edit Confirm')
        editConfirmWindow.geometry('%dx%d+%d+%d' % (310, 140, x * 1.5, y * 1.5))
        confirm_message = Label(editConfirmWindow, text=" Are you sure you want to save changes?", padx=10, pady=10)
        confirm_message.grid(row=0, column=0, pady=10)
        yesNoBox = Frame(editConfirmWindow)
        yesNoBox.grid(row=1, column=0, padx=20, pady=(10, 0))
        edit_yes_button = Button(yesNoBox, text="Yes", command=submitEditCommand)
        edit_yes_button.grid(row=0, column=0, columnspan=2, pady=5, padx=1, ipadx=50)
        edit_no_button = Button(yesNoBox, text="No", command=editConfirmWindow.destroy)
        edit_no_button.grid(row=0, column=2, columnspan=2, pady=5, padx=1, ipadx=50)

    def deleteConfirm():  # need to MODIFY values in column when table content changes!!!!
        global deleteConfirmWindow
        deleteConfirmWindow = tk.Tk()
        deleteConfirmWindow.title('Delete Confirm')
        deleteConfirmWindow.geometry('%dx%d+%d+%d' % (310, 140, x * 1.5, y * 1.5))
        # Issue fixed
        global columnAxis
        if (tableOndisplay.currentTable == "products"):
            selectColumn = display_Products_ContentTree.focus()
            valuesInColumn = display_Products_ContentTree.item(selectColumn, "values")
            columnAxis = treeCurrentdisplay("products", valuesInColumn[8])
        elif (tableOndisplay.currentTable == "vendors"):
            selectColumn = display_Vendors_ContentTree.focus()
            valuesInColumn = display_Vendors_ContentTree.item(selectColumn, "values")
            columnAxis = treeCurrentdisplay("vendors", valuesInColumn[8])
        elif (tableOndisplay.currentTable == "orders"):
            selectColumn = display_Orders_ContentTree.focus()
            valuesInColumn = display_Orders_ContentTree.item(selectColumn, "values")
            columnAxis = treeCurrentdisplay("orders", valuesInColumn[2])
        elif (tableOndisplay.currentTable == "vendorPrices"):
            selectColumn = display_VendorPrices_ContentTree.focus()
            valuesInColumn = display_VendorPrices_ContentTree.item(selectColumn, "values")
            columnAxis = treeCurrentdisplay("vendorPrices", valuesInColumn[5])
        print(selectColumn)
        confirm_message = Label(deleteConfirmWindow, text="Are you sure you want to delete selected column?", padx=10,
                                pady=10)
        confirm_message.grid(row=0, column=0, pady=10)
        yesNoBox = Frame(deleteConfirmWindow)
        yesNoBox.grid(row=1, column=0, padx=20, pady=(10, 0))
        edit_yes_button = Button(yesNoBox, text="Yes", command=submitDeleteCommand)
        edit_yes_button.grid(row=0, column=0, columnspan=2, pady=5, padx=1, ipadx=50)
        edit_no_button = Button(yesNoBox, text="No", command=deleteConfirmWindow.destroy)
        edit_no_button.grid(row=0, column=2, columnspan=2, pady=5, padx=1, ipadx=50)
    #tables btn mod
    def tablebtnModify():
        main_insert_button.grid()
        main_edit_button.grid()
        main_delete_button.grid()
        main_backToMainPage_button.grid()
        main_sort_button.grid_remove()
        main_sortBy_label.grid_remove()
        mainSortComboDropdown.grid_remove()
    #summary page btn modify
    def summarybtnModify():
        main_insert_button.grid_remove()
        main_edit_button.grid_remove()
        main_delete_button.grid_remove()
        main_backToMainPage_button.grid_remove()
        main_sort_button.grid()
        main_sortBy_label.grid()
        mainSortComboDropdown.grid()

    def displayProductsWindowSetUp():
        global product_tree_frame
        product_tree_frame = Frame(tab)
        product_tree_frame.grid(row=0, column=0, padx=50, pady=20)
        product_tree_scroll = Scrollbar(product_tree_frame)
        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("products", "")
        global display_Products_ContentTree
        display_Products_ContentTree = ttk.Treeview(product_tree_frame, yscrollcommand=product_tree_scroll.set,
                                                    column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"),
                                                    show='headings')
        product_tree_scroll.grid(column=1, row=0, sticky='NSE')
        product_tree_scroll.config(command=display_Products_ContentTree.yview)
        display_Products_ContentTree.column("#1", width=150, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#1", text="SKU")
        # display_Products_ContentTree.column("#2", width=50, minwidth=50, anchor=tk.CENTER)
        # display_Products_ContentTree.heading("#2", text="Category")
        display_Products_ContentTree.column("#3", width=180, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#3", text="Prod Description")
        display_Products_ContentTree.column("#4", width=180, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#4", text="Product URL")
        display_Products_ContentTree.column("#5", width=80, minwidth=80, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#5", text="Quantity")
        display_Products_ContentTree.column("#6", width=120, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#6", text="Availability")
        display_Products_ContentTree.column("#7", width=120, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#7", text="Reorder Level")
        display_Products_ContentTree.column("#8", width=120, minwidth=100, anchor=tk.CENTER)
        display_Products_ContentTree.heading("#8", text="Units In Stock")
        display_Products_ContentTree.grid(row=0, column=0)
        tablebtnModify()
        root.geometry("1600x460")

    def displayVendorsWindowSetUp():
        global vendor_tree_frame
        vendor_tree_frame = Frame(tab)
        vendor_tree_frame.grid(row=0, column=0, padx=50, pady=20)
        vendor_tree_scroll = Scrollbar(vendor_tree_frame)
        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("vendors", "")
        global display_Vendors_ContentTree
        display_Vendors_ContentTree = ttk.Treeview(vendor_tree_frame, yscrollcommand=vendor_tree_scroll.set,
                                                   column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"),
                                                   show='headings')
        vendor_tree_scroll.grid(column=1, row=0, sticky='NSE')
        vendor_tree_scroll.config(command=display_Vendors_ContentTree.yview)
        display_Vendors_ContentTree.column("#1", width=120, minwidth=70, anchor=tk.W)
        display_Vendors_ContentTree.heading("#1", text="Vendor Name")
        display_Vendors_ContentTree.column("#2", width=130, minwidth=90, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#2", text="Phone Number")
        display_Vendors_ContentTree.column("#3", width=170, minwidth=100, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#3", text="Email")
        display_Vendors_ContentTree.column("#4", width=160, minwidth=100, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#4", text="Address")
        display_Vendors_ContentTree.column("#5", width=80, minwidth=100, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#5", text="Zip Code")
        display_Vendors_ContentTree.column("#6", width=100, minwidth=90, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#6", text="City")
        display_Vendors_ContentTree.column("#7", width=70, minwidth=60, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#7", text="State")
        display_Vendors_ContentTree.column("#8", width=100, minwidth=90, anchor=tk.CENTER)
        display_Vendors_ContentTree.heading("#8", text="Web URL")

        display_Vendors_ContentTree.grid(row=0, column=0)
        tablebtnModify()
        root.geometry("1480x460")

    def displayOrdersWindowSetUp():
        global order_tree_frame
        order_tree_frame = Frame(tab)
        order_tree_frame.grid(row=0, column=0, padx=50, pady=20)
        order_tree_scroll = Scrollbar(order_tree_frame)
        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("orders", "")
        global display_Orders_ContentTree
        display_Orders_ContentTree = ttk.Treeview(order_tree_frame, yscrollcommand=order_tree_scroll.set,
                                                  column=("c1", "c2", "c3", "c4", "c5"), show='headings')
        order_tree_scroll.grid(column=1, row=0, sticky='NSE')
        order_tree_scroll.config(command=display_Orders_ContentTree.yview)
        display_Orders_ContentTree.column("#1", width=250, minwidth=150, anchor=tk.W)
        display_Orders_ContentTree.heading("#1", text="order ID")
        display_Orders_ContentTree.column("#2", width=180, minwidth=80, anchor=tk.CENTER)
        display_Orders_ContentTree.heading("#2", text="Order Date")
        display_Orders_ContentTree.column("#3", width=140, minwidth=100, anchor=tk.CENTER)
        display_Orders_ContentTree.heading("#3", text="Status")
        display_Orders_ContentTree.column("#4", width=100, minwidth=80, anchor=tk.CENTER)
        display_Orders_ContentTree.heading("#4", text="Quantity")
        display_Orders_ContentTree.column("#5", width=100, minwidth=80, anchor=tk.CENTER)
        display_Orders_ContentTree.heading("#5", text="Total Sum")

        display_Orders_ContentTree.grid(row=0, column=0)
        display_Orders_ContentTree.bind('<Double-1>', doubleClicked)
        tablebtnModify()
        root.geometry("1200x460")

    def displayVendorPricesWindowSetUp():
        global vp_tree_frame
        vp_tree_frame = Frame(tab)
        vp_tree_frame.grid(row=0, column=0, padx=50, pady=20)
        vp_tree_scroll = Scrollbar(vp_tree_frame)
        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("vendorPrices", "")
        global display_VendorPrices_ContentTree
        display_VendorPrices_ContentTree = ttk.Treeview(vp_tree_frame, yscrollcommand=vp_tree_scroll.set,
                                                        column=("c1", "c2", "c3", "c4"), show='headings')
        vp_tree_scroll.grid(column=1, row=0, sticky='NSE')
        vp_tree_scroll.config(command=display_VendorPrices_ContentTree.yview)
        display_VendorPrices_ContentTree.column("#1", width=250, minwidth=150, anchor=tk.W)
        display_VendorPrices_ContentTree.heading("#1", text="Vendor")
        display_VendorPrices_ContentTree.column("#2", width=180, minwidth=80, anchor=tk.CENTER)
        display_VendorPrices_ContentTree.heading("#2", text="SKU")
        display_VendorPrices_ContentTree.column("#3", width=140, minwidth=100, anchor=tk.CENTER)
        display_VendorPrices_ContentTree.heading("#3", text="Unit List Price")
        display_VendorPrices_ContentTree.column("#4", width=140, minwidth=100, anchor=tk.CENTER)
        display_VendorPrices_ContentTree.heading("#4", text="Time Checked")

        display_VendorPrices_ContentTree.grid(row=0, column=0)
        tablebtnModify()
        root.geometry("1300x460")

    def displayMainPageQueryWindowSetUp():
        global summary_tree_frame
        summary_tree_frame = Frame(tab)
        summary_tree_frame.grid(row=0, column=0, padx=50, pady=20)
        summary_tree_scroll = Scrollbar(summary_tree_frame)
        global tableOndisplay
        tableOndisplay = treeCurrentdisplay("Product on Market", "")
        global mainPageQuery_ContentTree
        mainPageQuery_ContentTree = ttk.Treeview(summary_tree_frame, yscrollcommand=summary_tree_scroll.set,
                                                 column=("c1", "c2", "c3", "c4", "c5"), show='headings')
        summary_tree_scroll.grid(column=1, row=0, sticky='NSE')
        summary_tree_scroll.config(command=mainPageQuery_ContentTree.yview)
        mainPageQuery_ContentTree.column("#1", width=100, minwidth=80, anchor=tk.W)
        mainPageQuery_ContentTree.heading("#1", text="Vendor")
        mainPageQuery_ContentTree.column("#2", width=120, minwidth=80, anchor=tk.CENTER)
        mainPageQuery_ContentTree.heading("#2", text="SKU")
        mainPageQuery_ContentTree.column("#3", width=350, minwidth=100, anchor=tk.CENTER)
        mainPageQuery_ContentTree.heading("#3", text="product Description")
        mainPageQuery_ContentTree.column("#4", width=140, minwidth=100, anchor=tk.CENTER)
        mainPageQuery_ContentTree.heading("#4", text="Unit List Price")
        mainPageQuery_ContentTree.column("#5", width=140, minwidth=100, anchor=tk.CENTER)
        mainPageQuery_ContentTree.heading("#5", text="Time Checked")

        mainPageQuery_ContentTree.grid(row=0, column=0)
        global summaryFlag
        summaryFlag = summaryDCFlag("off")
        mainPageQuery_ContentTree.bind('<Double-1>', doubleClicked)
        summarybtnModify()
        root.geometry("1300x460")

    # Main Screen Labels
    main_table_select_label = Label(mainOptionFrame, text="Choose Table")
    main_table_select_label.grid(row=1, column=0, pady=10, padx=1)
    main_sortBy_label = Label(mainOptionFrame, text="Sort by")
    main_sortBy_label.grid(row=7, column=0)
    # Insert data button in Main screen
    main_insert_button = Button(mainOptionFrame, text="Add Data to Table", command=addCommand)
    main_insert_button.grid(row=3, column=0, columnspan=2, pady=10, padx=1, ipadx=70)
    # Display table button in Main screen
    main_select_display = Button(mainOptionFrame, text="Display Table", command=displayCommand)
    main_select_display.grid(row=2, column=0, columnspan=2, pady=10, padx=1, ipadx=83)
    # Edit button in Main Screen
    main_edit_button = Button(mainOptionFrame, text="Edit selected Column", command=editCommand)
    main_edit_button.grid(row=5, column=0, columnspan=2, pady=10, padx=1, ipadx=62)
    # Sort button in Main Screen
    main_sort_button = Button(mainOptionFrame, text="Sort", command=sortCommand)
    main_sort_button.grid(row=8, column=0, columnspan=2, pady=10, padx=1, ipadx=112)  # row 6 is left for drop down

    # Delete button in Main Screen
    main_delete_button = Button(mainOptionFrame, text="Delete Selected Column", command=deleteConfirm)
    main_delete_button.grid(row=6, column=0, columnspan=2, pady=10, padx=1, ipadx=55)
    main_backToMainPage_button = Button(mainOptionFrame, text="Back to Summary Table", command=backToSummaryDisplay)
    main_backToMainPage_button.grid(row=10, column=0, columnspan=2, pady=30, padx=1, ipadx=55)
    # Initial display
    displayMainPageQueryWindowSetUp()
    mainPageQuery()

    # things to be implemented
    # 1.DROPDOWN for status when adding new orders, to choose from "processing", "shipped", "delivered", "other" DONE
    # 2.Scroll Bar for all tables DONE
    # 3.Connect to csv file by using python  (integrate web crawler to the python)
    # 4.csv file should be corresponding to the implementation for easier import process
    # 5.generate pdf report
    # 6. (OPTIONAL) advanced query based on user filter (products and vendorprices and orders table only)
    # 7. display orderlines by select a specific order low (either double clicking or an extra option)
    # 8. low stock alert
    # 9. sort product by popularity by order history
    # 10. display active orders

    # thins to enhance
    # 1. switching tables have some displaying problems
    # 2. make the colors of the odd and even columns different
    # 3. (advanced) right-click to select to edit


    # main Pages before “Hiccups Management System”， option to webclawer
    # Cart
    conn.commit()

    # Close our connection
    conn.close()
