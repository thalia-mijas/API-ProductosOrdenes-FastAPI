from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from linked_list import LinkedList
from binary_search_tree import BST

app = FastAPI()
binary_tree = BST()
linked_list = LinkedList()

#Definir producto
class Product(BaseModel):
  quantity: int
  name: str
  price: float

#Definir orden
class Order(BaseModel):
  quantity: int
  product: str

#Definir documentos de almacenamiento
PRODUCTS_JSON_PATH = 'products.json'
ORDERS_JSON_PATH = 'orders.json'

#Leer archivos json
def read_json(file_path):
  try:
      with open(file_path, "r") as file:
          list = json.load(file)
  except FileNotFoundError:
       list = []

  return list

#Actualizar archivos json
def write_json(file_path, list):
  with open(file_path, "w") as file:
        json.dump(list, file, indent=4)

#Organizar inventario en arbol binario y ordenes en lista enlazada
def create_tree_and_list():

  inventary = read_json(PRODUCTS_JSON_PATH)

  for product in inventary:
    binary_tree.insert(product['key'], product['value']);

  orders = read_json(ORDERS_JSON_PATH)

  for order in orders:
    linked_list.add(order['id'], order['data'])
  
create_tree_and_list()

#Crear producto
@app.post('/api/product')
def create_product(product: Product):

  inventary = read_json(PRODUCTS_JSON_PATH)

  if any(p['value']['name'] == product.name for p in inventary):
    raise HTTPException(status_code=400, detail="Este producto ya existe")

  if (len(inventary) == 0):
    cont = 1
  else:
    cont = inventary[-1]['key'] + 1

  new_product = {
    'quantity': product.quantity,
    'name': product.name,
    'price': product.price
  }

  binary_tree.insert(cont, new_product)

  inventary.append({'key': cont, 'value': new_product})

  write_json(PRODUCTS_JSON_PATH, inventary)

  return {'key': cont, 'value': new_product}

#Consultar producto
@app.get('/api/product/{id}')
def consult_product(id: int):

  product = binary_tree.search(id);

  if product == None:
    raise HTTPException(status_code=404, detail="Producto no existe")

  return {'key': id, 'value': product}

#Crear orden
@app.post('/api/order')
def create_order(order: list[Order]):

  orders = read_json(ORDERS_JSON_PATH)

  inventary = read_json(PRODUCTS_JSON_PATH)

  if (len(orders) == 0):
    cont = 1
  else:
    cont = orders[-1]['id'] + 1

  items = []

  total = 0

  for o in order:
    item = {
      'quantity': o.quantity,
      'product': o.product
    }
    try:
        #Revisa si los productos en la orden existen en el inventario
        product_index = [p['value']['name'] for p in inventary].index(o.product)
        items.append(item)
        total = total + (inventary[product_index]['value']['price'] * o.quantity)
    except:
        raise HTTPException(status_code=404, detail="Producto fuera de stock", headers={'Producto': o.product})
    #Revisa si la cantidad de los productos en la orden existen en el stock
    if o.quantity > inventary[product_index]['value']['quantity']:
        print(inventary[product_index]['value']['quantity'])
        raise HTTPException(status_code=409, detail="Cantidad de producto excede stock", headers={'Producto': o.product})
    else:
        inventary[product_index]['value']['quantity'] = inventary[product_index]['value']['quantity'] - o.quantity
    
  new_order = {
    'items': items,
    'total': round(total, 2)
  }
  
  linked_list.add(cont, new_order)

  orders.append({'id': cont, 'data': new_order})

  write_json(ORDERS_JSON_PATH, orders)

  write_json(PRODUCTS_JSON_PATH, inventary)

  return {'id': cont, 'data': new_order}

#Consultar orden
@app.get('/api/order/{id}')
def consult_order(id: int):

  order_index = linked_list.find(id);

  if order_index == None:
    raise HTTPException(status_code=404, detail="Orden no existe")

  return{'Order': order_index}

#Actualizar orden
@app.put('/api/order/{id}')
def update_order(id: int, order: list[Order]):

  orders = read_json(ORDERS_JSON_PATH)

  inventary = read_json(PRODUCTS_JSON_PATH)

  order_del = linked_list.find(id);

  if order_del == None:
    raise HTTPException(status_code=404, detail="Orden a actualizar no existe")

  #Devuelve a stock los productos de la orden a actualizar
  for i in orders[id-1]['data']['items']:
    product_index = [p['value']['name'] for p in inventary].index(i['product'])
    inventary[product_index]['value']['quantity'] = inventary[product_index]['value']['quantity'] + i['quantity']

  linked_list.delete(id)

  orders.pop(id-1)

  items = []

  total = 0

  for o in order:
    item = {
      'quantity': o.quantity,
      'product': o.product
    }
    try:
        #Revisa si los productos en la orden existen en el inventario
        product_index = [p['value']['name'] for p in inventary].index(o.product)
        items.append(item)
        total = total + (inventary[product_index]['value']['price'] * o.quantity)
    except:
        raise HTTPException(status_code=404, detail="Producto fuera de stock", headers={'Producto': o.product})
    #Revisa si la cantidad de los productos en la orden existen en el stock
    if o.quantity > inventary[product_index]['value']['quantity']:
        print(inventary[product_index]['value']['quantity'])
        raise HTTPException(status_code=409, detail="Cantidad de producto excede stock", headers={'Producto': o.product})
    else:
        inventary[product_index]['value']['quantity'] = inventary[product_index]['value']['quantity'] - o.quantity
    
  new_order = {
    'items': items,
    'total': round(total, 2)
  }
  
  linked_list.add(id, new_order)

  orders.append({'id': id, 'data': new_order})

  write_json(ORDERS_JSON_PATH, orders)

  write_json(PRODUCTS_JSON_PATH, inventary)

  return{'Successfully updated order'}

#Eliminar orden
@app.delete('/api/order/{id}')
def delete_order(id: int):

  orders = read_json(ORDERS_JSON_PATH)

  inventary = read_json(PRODUCTS_JSON_PATH)

  order_del = linked_list.find(id);

  if order_del == None:
    raise HTTPException(status_code=404, detail="Orden a eliminar no existe")

  #Devuelve a stock los productos de la orden a eliminar
  for i in orders[id-1]['data']['items']:
    product_index = [p['value']['name'] for p in inventary].index(i['product'])
    inventary[product_index]['value']['quantity'] = inventary[product_index]['value']['quantity'] + i['quantity']

  linked_list.delete(id)

  orders.pop(id-1)

  write_json(ORDERS_JSON_PATH, orders)

  write_json(PRODUCTS_JSON_PATH, inventary)

  return{'Successfully deleted order'}

#Listar ordenes
@app.get('/api/orders')
def list_orders():

  orders = read_json(ORDERS_JSON_PATH)

  return{'Orders': orders}