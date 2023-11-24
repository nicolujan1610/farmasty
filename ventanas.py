from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem, QMessageBox,QAbstractItemView
from PyQt6 import uic
import csv
import pandas as pd

# ToDos:
#   Inventario casi listo, por no decir listo...
#   Historial De Ventas:
#     Leer csvs y ponerlos en la tabla
#     Añadir función a los botones
#   Nueva Venta:
#     Leer csvs y ponerlos en la tabla
#     Añadir función a los botones

# ------------------LogIn------------------
class LoginVentana(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('main-ventana.ui', self)
    self.loginBtn.clicked.connect(self.verificar_usuario)
    self.error.setVisible(False)

  def verificar_usuario(self):
    usuario_ingresado = self.username_input.text()
    pw_ingresada = self.password_input.text()

    acierto = False
    with open('usuarios.csv') as f:
      reader = csv.reader(f, delimiter='|')
      for row in reader:
        if row[0] == usuario_ingresado and row[1] == pw_ingresada:
          acierto = True
          usuario = row[0]

    if acierto:
      self.iniciar_sesion(usuario)
    else:
      login_win.error.setVisible(True)

  def iniciar_sesion(self, usuario):
    menu_win.bienvenido_lbl.setText(f"Bienvenido, {usuario}!")
    menu_win.show()
    self.hide()

# ------------------Menú------------------
class MenuVentana(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('menu-ventana.ui', self)
    self.action_cerrar_sesion.triggered.connect(self.cerrar_sesion)
    self.recetas_btn.clicked.connect(self.ir_a_recetas)
    self.nueva_venta_btn.clicked.connect(self.ir_a_venta)
    self.inventario_btn.clicked.connect(self.ir_a_inventario)
    self.historial_ventas_btn.clicked.connect(self.ir_a_historial)

  def ir_a_historial(self):
    historial_win.leer_csv()
    self.hide()
    historial_win.show()

  def ir_a_inventario(self):
    self.hide()
    inventario_win.show()

  def ir_a_venta(self):
    self.hide()
    nueva_venta_win.show()

  def ir_a_recetas(self):
    self.hide()
    receta_win.show()

  def cerrar_sesion(self):
    login_win.show()
    login_win.username_input.setText("")
    login_win.password_input.setText("")
    login_win.error.setVisible(False)
    self.hide()


# ------------------Ventana Nueva Venta------------------
class NuevaVentaVentana(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('nueva-venta/nueva-venta.ui', self)
    self.menu_btn.clicked.connect(self.ir_a_menu)
    self.agg_producto.clicked.connect(self.ir_a_agg_prod)
    self.realizar_venta.clicked.connect(self.ir_a_realizar_venta)
    self.total = 0
    self.ventas_table.setColumnCount(4)
    self.ventas_table.setHorizontalHeaderLabels(('Producto', 'Categoria', 'Precio', 'Cantidad Disponible'))
    self.limpiar_venta.clicked.connect(self.limpiar_venta_clicked)
    self.eliminar_producto.clicked.connect(self.eliminar_producto_clicked)
    self.warning_lbl.setVisible(False)

  def eliminar_producto_clicked(self):
    elementos_seleccionados = self.ventas_table.selectedItems()

    if elementos_seleccionados:
      self.warning_lbl.setVisible(False)
      # Obtener la fila de un elemento seleccionado (asumiendo que es una selección por fila)
      fila_seleccionada = elementos_seleccionados[0].row()
      print(fila_seleccionada)
      # Crear cartel de advertencia
      self.quitar_confirmacion = QMessageBox()
      self.quitar_confirmacion.setIcon(QMessageBox.Icon.Warning)
      buttons = (QMessageBox.StandardButton.No)
      buttons |= QMessageBox.StandardButton.Yes
      self.quitar_confirmacion.setStandardButtons(buttons)
      self.quitar_confirmacion.setWindowTitle("Eliminar Producto")
      self.quitar_confirmacion.setText("¿Desea eliminar por completo el producto?")
      self.quitar_confirmacion.exec()

      if self.quitar_confirmacion.clickedButton().text() == '&Yes':
          # Eliminar la fila seleccionada
          item = self.ventas_table.item(fila_seleccionada, 2)
          self.total = self.total - int(item.text())
          self.total_venta_lbl.setText(f"Total: ${self.total}")
          self.ventas_table.removeRow(fila_seleccionada)
    else:
      # Crear la advertencia de ningun elemento seleccionado.
      self.warning_lbl.setVisible(True)
      


  def limpiar_venta_clicked(self):
    self.ventas_table.setRowCount(0)
    self.total = 0
    self.total_venta_lbl.setText(f"Total: ${self.total}")
    finalizar_venta_win.hide()

  def ir_a_realizar_venta(self):
    finalizar_venta_win.precio_final_lbl.setText(f"{self.total}")
    self.hide()
    finalizar_venta_win.show()

  def ir_a_agg_prod(self):
    agregar_producto_win.products_cbx.setCurrentIndex(0)
    agregar_producto_win.show()

  def ir_a_menu(self):
    self.hide()
    menu_win.show()
    
#||--------Finalizar Venta--------||
class FinalizarVentaVentana(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('nueva-venta/realizar-venta-ventana.ui', self)
    self.cancelar_vta_btn.clicked.connect(self.cancelar_venta)
    self.realizar_vta_btn.clicked.connect(self.realizar_venta)
    self.descuentoAplicado = False
    self.calcular_precio()
    self.obra_si.toggled.connect(self.calcular_precio)
    self.descuento = 0
    self.warning_lbl.setVisible(False)

  def calcular_precio(self):
    if self.obra_si.isChecked():
      self.descuento = nueva_venta_win.total * 0.1
      nueva_venta_win.total = nueva_venta_win.total * 0.9 #Descuento del 10%
      self.precio_final_lbl.setText(f"{nueva_venta_win.total}")
      self.descuentoAplicado = True
    else:
      if self.descuentoAplicado: 
        nueva_venta_win.total = nueva_venta_win.total + self.descuento
        self.precio_final_lbl.setText(f"{nueva_venta_win.total}")

  def realizar_venta(self):
    if float(nueva_venta_win.total) <= 0:
      self.warning_lbl.setVisible(True)
    else: 
      total = float(self.precio_final_lbl.text())
      prods_vendidos = nueva_venta_win.ventas_table.rowCount()
      if self.descuentoAplicado:
        con_descuento = 'Si'
      else:
        con_descuento = 'No'
      
      metodo_de_pago = self.metodo_pago_cb.currentText()
      detalles_de_venta_actual = [total, prods_vendidos, metodo_de_pago, con_descuento]
      lista_completa = [detalles_de_venta_actual]

      with open('historial/historial.csv', "r", encoding='utf-8') as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
          total_venta = row[0]
          prods_vendidos = row[1]
          metodo_de_pago = row[2]
          obra_social = row[3]
          datosLista = [total_venta, prods_vendidos, metodo_de_pago, obra_social]
          lista_completa.append(datosLista)
        
      df = pd.DataFrame(lista_completa)
      # Guardar el DataFrame en el archivo CSV, sobrescribiendo completamente el archivo
      df.to_csv('historial/historial.csv', index=False, header=False, sep='|')
      
      nueva_venta_win.show()
      nueva_venta_win.limpiar_venta_clicked()

  def cancelar_venta(self):
    nueva_venta_win.show()
    self.hide()


# ||--------Agg Producto a Venta--------||
class AgregarProductoVentana(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('nueva-venta/agregar-producto.ui', self)
    self.cancelar_btn.clicked.connect(self.cancelar)
    self.agregar_btn.clicked.connect(self.agregar_producto)
    self.products_cbx.clear()
    self.cargar_cbx()

  def cargar_cbx(self):
    lista = []
    with open('inventario/inventario.csv', 'r', encoding='utf-8') as f:
      reader = csv.reader(f, delimiter="|")
      for row in reader:
        producto = row[0]
        lista.append(producto)
    self.products_cbx.addItems(sorted(lista))


  def agregar_producto(self):
    elemento_texto = self.products_cbx.currentText()
    with open('inventario/inventario.csv', 'r', encoding='utf-8') as f:
      reader = csv.reader(f, delimiter="|")
      for row in reader:
        if elemento_texto == row[0]:
          detalles_elemento = [row[0],row[1],row[2],row[3]]
          nueva_venta_win.total = int(nueva_venta_win.total) + int(row[2])
          nueva_venta_win.total_venta_lbl.setText(f"Total: ${nueva_venta_win.total}")

    contador = 0
    filasActuales = nueva_venta_win.ventas_table.rowCount()
    nueva_venta_win.ventas_table.insertRow(filasActuales)
    for dato in detalles_elemento:
      nueva_venta_win.ventas_table.setItem(filasActuales, contador, QTableWidgetItem(dato))
      contador += 1
    
    self.hide()

  def cancelar(self):
    self.products_cbx.setCurrentIndex(0)
    self.hide()






# ------------------Ventana Recetas------------------
class RecetasVentana(QMainWindow):
  def __init__(self):
    super(RecetasVentana, self).__init__()
    uic.loadUi('./recetas/recetas-ventana.ui', self)
    self.volver_menu_btn.clicked.connect(self.volver_menu_y_cargar_csv)
    self.gotoagg_btn.clicked.connect(self.go_to_agg)
    self.quitar_btn.clicked.connect(self.quitar_fila_clicked)
    self.warning_lbl.setVisible(False)

    self.datos_a_cargar = []
    # Config de la tabla
    self.recetas_table.setColumnCount(6)
    self.recetas_table.setHorizontalHeaderLabels(('Paciente', 'Emisión', 'Medicamento', 'Cantidad', 'Diagnostico', 'Doctor'))

  def showEvent(self, event):
    # Este método se llama cuando la ventana se muestra
    super(RecetasVentana, self).showEvent(event)
    self.completar_tabla_csv()
    
  def completar_tabla_csv(self):
    self.recetas_table.setRowCount(0)

    with open('recetas/recetas.csv', 'r') as f:
      reader = csv.reader(f, delimiter="|")
      for row in reader:
        paciente = row[0]
        emision = row[1]
        medicamento = row[2]
        cantidad = row[3]
        diagnostico = row[4]
        doctor = row[5]
        datosLista = [paciente, emision, medicamento, cantidad, diagnostico, doctor]
        self.cargar_receta(datosLista)

    agregar_receta_win.error_lbl.setVisible(False)

  def quitar_fila_clicked(self):
    elementos_seleccionados = self.recetas_table.selectedItems()

    if elementos_seleccionados:
      self.warning_lbl.setVisible(False)
      # Obtener la fila de un elemento seleccionado (asumiendo que es una selección por fila)
      fila_seleccionada = elementos_seleccionados[0].row()
      print(f"La fila seleccionada es: {fila_seleccionada}")

      # Crear cartel de advertencia
      self.quitar_confirmacion = QMessageBox()
      self.quitar_confirmacion.setIcon(QMessageBox.Icon.Warning)
      buttons = (QMessageBox.StandardButton.No)
      buttons |= QMessageBox.StandardButton.Yes
      self.quitar_confirmacion.setStandardButtons(buttons)
      self.quitar_confirmacion.setWindowTitle("Eliminar Receta")
      self.quitar_confirmacion.setText("¿Desea eliminar receta?")
      self.quitar_confirmacion.exec()

      if self.quitar_confirmacion.clickedButton().text() == '&Yes':
          # Eliminar la fila seleccionada
          self.recetas_table.removeRow(fila_seleccionada)

    else:
      # Crear la advertencia de ningun elemento seleccionado.
      self.warning_lbl.setVisible(True)

  def go_to_agg(self):
    agregar_receta_win.show()

  def volver_menu_y_cargar_csv(self):
    datos_inventario = []

    for row in range(self.recetas_table.rowCount()):
        fila = []
        for column in range(self.recetas_table.columnCount()):
            item = self.recetas_table.item(row, column)
            fila.append(item.text() if item is not None else "")
        datos_inventario.append(fila)

    df = pd.DataFrame(datos_inventario)
    # Guardar el DataFrame en el archivo CSV, sobrescribiendo completamente el archivo
    df.to_csv('recetas/recetas.csv', index=False, header=False, sep='|')

    self.hide()
    menu_win.show()

  def cargar_receta(self, datos):
    contador = 0
    filasActuales = self.recetas_table.rowCount()
    self.recetas_table.insertRow(filasActuales)
    for dato in datos:
      self.recetas_table.setItem(filasActuales, contador, QTableWidgetItem(dato))
      contador += 1

    agregar_receta_win.cancelar_receta()

# ||--------Agg Receta--------||
class AgregarRecetaWidget(QWidget):
  def __init__(self):
    super().__init__()
    uic.loadUi('./recetas/agregar-receta-ventana.ui',self)
    self.agg_receta_btn.clicked.connect(self.agregar_receta_clicked)
    self.cancelar_receta_btn.clicked.connect(self.cancelar_receta)
    # Para cuando tabuleas los inputs tener un buen orden
    self.paciente_input.setFocus()
    self.setTabOrder(self.paciente_input, self.emision_input)
    self.setTabOrder(self.emision_input, self.medicamento_input)
    self.setTabOrder(self.medicamento_input, self.cantidad_input)
    self.setTabOrder(self.cantidad_input, self.diagnostico_input)
    self.setTabOrder(self.diagnostico_input, self.doctor_input)
    self.error_lbl.setVisible(False)

  def cancelar_receta(self):
    self.paciente_input.setText("")
    self.emision_input.setText("")
    self.medicamento_input.setText("")
    self.cantidad_input.setText("")
    self.diagnostico_input.setText("")
    self.doctor_input.setText("")
    self.hide()

  def agregar_receta_clicked(self):
    paciente = self.paciente_input.text()
    medicamento = self.medicamento_input.text()
    emision = self.emision_input.text()
    doctor = self.doctor_input.text()
    diagnostico = self.diagnostico_input.text()
    cantidad = self.cantidad_input.text()

    datosLista = [paciente, emision, medicamento, cantidad, diagnostico, doctor]

    contador = 0
    for dato in datosLista:
      if dato != "":
        contador += 1
    
    if contador == 6:
      receta_win.cargar_receta(datosLista)
      self.error_lbl.setVisible(False)
    else:
      self.error_lbl.setVisible(True)


# ------------------Ventana Inventario------------------
class InventarioVentana(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('./inventario/inventario-ventana.ui',self)
    self.volver_menu_btn.clicked.connect(self.ir_a_menu_y_cargar_csv)
    # Config de la tabla
    self.inventario_table.setRowCount(0)
    self.inventario_table.setColumnCount(4)
    self.inventario_table.setHorizontalHeaderLabels(('Producto', 'Categoria', 'Precio', 'Cantidad'))
    self.agg_btn.clicked.connect(self.ir_a_agregar_producto)
    self.del_btn.clicked.connect(self.quitar_fila_inventario)
    self.warning_lbl.setVisible(False)

  def quitar_fila_inventario(self):
    elementos_seleccionados = self.inventario_table.selectedItems()

    if elementos_seleccionados:
      self.warning_lbl.setVisible(False)
      # Obtener la fila de un elemento seleccionado (asumiendo que es una selección por fila)
      fila_seleccionada = elementos_seleccionados[0].row()

      # Crear cartel de advertencia
      self.quitar_confirmacion = QMessageBox()
      self.quitar_confirmacion.setIcon(QMessageBox.Icon.Warning)
      buttons = (QMessageBox.StandardButton.No)
      buttons |= QMessageBox.StandardButton.Yes
      self.quitar_confirmacion.setStandardButtons(buttons)
      self.quitar_confirmacion.setWindowTitle("Eliminar Producto")
      self.quitar_confirmacion.setText("¿Desea eliminar por completo el producto?")
      self.quitar_confirmacion.exec()

      if self.quitar_confirmacion.clickedButton().text() == '&Yes':
          # Eliminar la fila seleccionada
          self.inventario_table.removeRow(fila_seleccionada)

    else:
      # Crear la advertencia de ningun elemento seleccionado.
      self.warning_lbl.setVisible(True)

  def cargar_producto(self, datos):
    contador = 0
    filasActuales = self.inventario_table.rowCount()
    self.inventario_table.insertRow(filasActuales)
    for dato in datos:
      self.inventario_table.setItem(filasActuales, contador, QTableWidgetItem(dato))
      contador += 1
    agregar_stock_win.hide()

  def ir_a_agregar_producto(self):
    agregar_stock_win.show()

  def showEvent(self, event):
    self.inventario_table.setRowCount(0)
    # Este método se llama cuando la ventana se muestra
    super(InventarioVentana, self).showEvent(event)
    with open('inventario/inventario.csv', encoding='utf-8') as f:
      reader = csv.reader(f, delimiter="|")
      for row in reader:
        producto = row[0]
        categoria = row[1]
        precio = row[2]
        cantidad = row[3]
        datosLista = [producto, categoria, precio, cantidad]
        self.cargar_inventario(datosLista)

  def cargar_inventario(self, datos):
    contador = 0
    filasActuales = self.inventario_table.rowCount()
    self.inventario_table.insertRow(filasActuales)
    for dato in datos:
      self.inventario_table.setItem(filasActuales, contador, QTableWidgetItem(dato))
      contador += 1

  def ir_a_menu_y_cargar_csv(self):

    datos_inventario = []

    for row in range(self.inventario_table.rowCount()):
      fila = []
      for column in range(self.inventario_table.columnCount()):
        item = self.inventario_table.item(row, column)
        fila.append(item.text() if item is not None else "")
      datos_inventario.append(fila)

    df = pd.DataFrame(datos_inventario)
    # Guardar el DataFrame en el archivo CSV, sobrescribiendo completamente el archivo
    df.to_csv('inventario/inventario.csv', index=False, header=False, sep='|')

    self.hide()
    menu_win.show()
    
# ||--------Agg a Stock--------||
class AgregarStockVentana(QWidget):
  def __init__(self):
    super().__init__()
    uic.loadUi('./inventario/agregar-stock-ventana.ui',self)
    self.agg_btn.clicked.connect(self.cargar_inventario)
    self.error_lbl.setVisible(False)

  def cargar_inventario(self):
    producto = self.producto_input.text()
    categoria = self.categoria_input.text()
    precio = self.precio_input.text()
    cantidad = self.cantidad_input.text()
    
    datosLista = [producto, categoria, precio, cantidad]

    contador = 0
    for dato in datosLista:
      if dato != "":
        contador += 1
    
    if contador == 4:
      inventario_win.cargar_producto(datosLista)
      self.error_lbl.setVisible(False)
    else:
      self.error_lbl.setVisible(True)
    


# ------------------Ventana Historial------------------
class HistorialVentasVentana(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('historial/historial-ventana.ui',self)
    self.menu_btn.clicked.connect(self.ir_a_menu)
     # Config de la tabla
    self.historial_table.setRowCount(0)
    self.historial_table.setColumnCount(4)
    self.historial_table.setHorizontalHeaderLabels(('Total', 'Cantidad de productos', 'Metodo de pago', 'Obra Social'))

    self.leer_csv()

  def leer_csv(self):
    self.historial_table.setRowCount(0)
    
    with open('historial/historial.csv', "r", encoding='utf-8') as f:
      reader = csv.reader(f, delimiter="|")
      for row in reader:
        total_venta = row[0]
        prods_vendidos = row[1]
        metodo_de_pago = row[2]
        obra_social = row[3]
        datosLista = [total_venta, prods_vendidos, metodo_de_pago, obra_social]
        self.cargar_historial(datosLista)

  def cargar_historial(self, datos):
    contador = 0
    filasActuales = self.historial_table.rowCount()
    self.historial_table.insertRow(filasActuales)
    for dato in datos:
      self.historial_table.setItem(filasActuales, contador, QTableWidgetItem(dato))
      contador += 1

  def ir_a_menu(self):
    self.hide()
    menu_win.show()
    
app = QApplication([])
agregar_receta_win = AgregarRecetaWidget()
receta_win = RecetasVentana()
menu_win = MenuVentana()
login_win = LoginVentana()
nueva_venta_win = NuevaVentaVentana()
agregar_producto_win = AgregarProductoVentana()
inventario_win = InventarioVentana()
agregar_stock_win = AgregarStockVentana()
historial_win = HistorialVentasVentana()
finalizar_venta_win = FinalizarVentaVentana()

login_win.show()
app.exec()