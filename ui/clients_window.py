import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFrame, QScrollArea, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QAbstractItemView, QTreeWidgetItem, QMessageBox
from PyQt5.QtGui import QColor

from logic import customers_crud

class ClientsWindow(QMainWindow):
    def __init__(self, master):
        super().__init__(master)
        self.setWindowTitle("Clients details") 
        self.setGeometry(100, 100, 1000, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)

        self.style = "QTreeView { background-color: #D3D3D3D; color: black; row-height: 25px; field-background: #D3D3D3D; show: headings; }" + \
                     "QTreeView::item:selected { background-color: #347083; }"

        self.tree_frame = QFrame()
        self.tree_layout = QVBoxLayout(self.tree_frame)
        self.layout.addWidget(self.tree_frame)

        self.tree = QTreeView()
        self.tree.setStyleSheet(self.style)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree_layout.addWidget(self.tree)

        self.tree.setHeaderLabels(["Customer id", "First Name", "Last Name", "Email", "Contact Number", "Address", "City", "Country"])
        
        self.tree_scroll = QScrollArea()
        self.tree_scroll.setWidgetResizable(True)
        self.tree_scroll.setWidget(self.tree_frame)
        self.layout.addWidget(self.tree_scroll)

        self.data_frame = QFrame()
        self.data_layout = QGridLayout(self.data_frame)
        self.layout.addWidget(self.data_frame)

        self.fn_label = QLabel("First Name")
        self.fn_entry = QLineEdit()
        self.data_layout.addWidget(self.fn_label, 0, 0)
        self.data_layout.addWidget(self.fn_entry, 0, 1)

        self.ln_label = QLabel("Last Name")
        self.ln_entry = QLineEdit()
        self.data_layout.addWidget(self.ln_label, 0, 2)
        self.data_layout.addWidget(self.ln_entry, 0, 3)

        self.id_label = QLabel("Email")
        self.id_entry = QLineEdit()
        self.data_layout.addWidget(self.id_label, 0, 4)
        self.data_layout.addWidget(self.id_entry, 0, 5)

        self.cn_label = QLabel("Contact Number")
        self.cn_entry = QLineEdit()
        self.data_layout.addWidget(self.cn_label, 1, 0)
        self.data_layout.addWidget(self.cn_entry, 1, 1)

        self.address_label = QLabel("Address")
        self.address_entry = QLineEdit()
        self.data_layout.addWidget(self.address_label, 1, 2)
        self.data_layout.addWidget(self.address_entry, 1, 3)

        self.city_label = QLabel("City")
        self.city_entry = QLineEdit()
        self.data_layout.addWidget(self.city_label, 1, 4)
        self.data_layout.addWidget(self.city_entry, 1, 5)

        self.country_label = QLabel("Country")
        self.country_entry = QLineEdit()
        self.data_layout.addWidget(self.country_label, 2, 0)
        self.data_layout.addWidget(self.country_entry, 2, 1)

        self.customer_id_label = QLabel("Customer Id")
        self.customer_id_entry = QLineEdit()
        self.data_layout.addWidget(self.customer_id_label, 2, 2)
        self.data_layout.addWidget(self.customer_id_entry, 2, 3)

        self.update_button = QPushButton("Update Client")
        self.update_button.clicked.connect(self.update_record)
        self.data_layout.addWidget(self.update_button, 0, 6)

        self.add_button = QPushButton("Add Client")
        self.add_button.clicked.connect(self.create_customer)
        self.data_layout.addWidget(self.add_button, 0, 7)

        # Add other buttons and connect them to their respective functions

        self.tree.itemSelectionChanged.connect(self.select_record)
        self.load_customers()

    def load_customers(self):
        records = customers_crud.get_customers()
        self.tree.clear()
        for count, record in enumerate(records):
            item = QTreeWidgetItem([str(item) for item in record])
            if count % 2 == 0:
                item.setBackground(0, QColor("white"))
            else:
                item.setBackground(0, QColor("lightblue"))
            self.tree.addTopLevelItem(item)

    # Implement the other functions (up, down, remove_one, remove_many, remove_all, clear_entries, etc.) similarly

    def select_record(self):
        selected_items = self.tree.selectedItems()
        if selected_items:
            values = [item.text(0) for item in selected_items[0].columnCount()]
            self.customer_id_entry.setText(values[0])
            self.fn_entry.setText(values[1])
            self.ln_entry.setText(values[2])
            self.id_entry.setText(values[3])
            self.cn_entry.setText(values[4])
            self.address_entry.setText(values[5])
            self.city_entry.setText(values[6])
            self.country_entry.setText(values[7])

    def create_customer(self):
        first_name = self.fn_entry.text()
        last_name = self.ln_entry.text()
        email = self.id_entry.text()
        contact_number = self.cn_entry.text()
        address = self.address_entry.text()
        city = self.city_entry.text()
        country = self.country_entry.text()
        customers_crud.create_customer(first_name, last_name, email, contact_number, address, city, country)
        self.clear_entries()
        self.load_customers()

    def update_record(self):
        selected_items = self.tree.selectedItems()
        if selected_items:
            customer_id = selected_items[0].text(0)
            first_name = self.fn_entry.text()
            last_name = self.ln_entry.text()
            email = self.id_entry.text()
            contact_number = self.cn_entry.text()
            address = self.address_entry.text()
            city = self.city_entry.text()
            country = self.country_entry.text()
            customers_crud.update_customer(customer_id, first_name, last_name, email, contact_number, address, city, country)
            self.clear_entries()
            self.load_customers()

    # Implement the other functions (up, down, remove_one, remove_many, remove_all, clear_entries, etc.) similarly


