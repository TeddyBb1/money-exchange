import sys
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon  # Importăm QIcon din QtGui
from PySide6.QtCore import QSize
import requests
import os

# Funcție pentru obținerea tuturor monedelor disponibile
def get_available_currencies():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        data = response.json()
        return list(data['rates'].keys())  # Returnează toate cheile (monedele disponibile)
    except Exception as e:
        print(f"Error fetching available currencies: {e}")
        return []

# Funcție pentru obținerea ratei de schimb valutar
def get_exchange_rate(from_currency, to_currency):
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        return data['rates'][to_currency]
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

# Funcție pentru actualizarea conversiei
def update_conversion():
    amount = float(amount_input.text())
    from_currency = from_currency_combobox.currentText()
    to_currency = to_currency_combobox.currentText()
    
    rate = get_exchange_rate(from_currency, to_currency)
    
    if rate:
        converted_amount = amount * rate
        result_input.setText(f"{converted_amount:.2f}")
    else:
        result_input.setText("Eroare conversie")

# Funcție pentru maparea codurilor valutare la steaguri
def get_flag_icon(currency_code):
    # Înlocuiește această cale cu calea corectă unde ai steagurile pe disc
    flag_path = f"./flags/{currency_code.lower()}.png"
    if os.path.exists(flag_path):
        return QIcon(flag_path)
    return QIcon()  # Returnăm un QIcon gol dacă steagul nu există

# Aplicația PySide
app = QApplication(sys.argv)

# Crearea ferestrei principale
window = QWidget()
window.setWindowTitle("Schimb Valutar cu Steaguri")

# Layout principal
main_layout = QVBoxLayout()

# Layout pentru prima linie (input și moneda de plecare)
input_layout = QHBoxLayout()
amount_input = QLineEdit()
amount_input.setPlaceholderText("Suma")
amount_input.setText("1")  # Valoare implicită

from_currency_combobox = QComboBox()
to_currency_combobox = QComboBox()

# Populăm combobox-urile cu toate monedele disponibile
available_currencies = get_available_currencies()

for currency in available_currencies:
    # Adăugăm moneda împreună cu steagul asociat
    from_currency_combobox.addItem(get_flag_icon(currency), currency)
    to_currency_combobox.addItem(get_flag_icon(currency), currency)

# Setăm valoarea implicită (USD -> EUR)
from_currency_combobox.setCurrentText("USD")
to_currency_combobox.setCurrentText("EUR")

input_layout.addWidget(amount_input)
input_layout.addWidget(from_currency_combobox)

# Layout pentru a doua linie (rezultatul și moneda de destinație)
output_layout = QHBoxLayout()
result_input = QLineEdit()
result_input.setPlaceholderText("Rezultat")
result_input.setReadOnly(True)  # Setăm rezultatul ca readonly

output_layout.addWidget(result_input)
output_layout.addWidget(to_currency_combobox)

# Buton pentru efectuarea conversiei
convert_button = QPushButton("Convertește")
convert_button.clicked.connect(update_conversion)

# Adăugăm toate layout-urile în layout-ul principal
main_layout.addLayout(input_layout)
main_layout.addLayout(output_layout)
main_layout.addWidget(convert_button)

# Setăm layout-ul ferestrei principale
window.setLayout(main_layout)

# Afișăm fereastra
window.show()

# Rulăm aplicația
sys.exit(app.exec())
