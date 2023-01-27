# **************************************************************************************************************************
# ****************************************************** Librerias *********************************************************
# **************************************************************************************************************************
import pymysql
import pandas as pd
import funciones_etl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# **************************************************************************************************************************
# ************************************************ Conexión a Base de datos * **********************************************
# **************************************************************************************************************************
def conect_db():
    try:
        print("Iniciando conexión a base de datos")
        conexion = pymysql.connect(
                host = '104.154.230.150',
                user = 'admin',
                passwd = 'admin',
                db = 'dbolist',
                ssl={"rejectUnauthorized":True})
        print("Conexión con base de dato establecida correctamente")
        return conexion
    except:
        print("Error al conectarse a la db")


def enviar_email(validaciones):
    try:
        # create message object instance 
        msg = MIMEMultipart()    
        message = """Reporte automático sobre integridad de datos en base de datos Olist
                                
                    • customers: {} 
                    • order_items: {} 
                    • order_payments: {} 
                    • order_reviews: {} 
                    • orders: {} 
                    • products: {} 
                    • sellers: {} 
                """.format(validaciones[0],validaciones[1],validaciones[2],
                            validaciones[3],validaciones[4],validaciones[5],
                            validaciones[6])
        print(message)
        # setup the parameters of the message 
        password = "oiwgkqfnjywwhval"
        msg['From'] = "grupo3.olist@gmail.com"
        msg['To'] = "mmacielaortiz@gmail.com"
        msg['Subject'] = "Validacion"
        
        # add in the message body 
        msg.attach(MIMEText(message, 'plain'))
        
        #create server 
        server = smtplib.SMTP('smtp.gmail.com: 587')
        
        server.starttls()
        
        # Login Credentials for sending the mail 
        server.login(msg['From'], password)
        
        
        # send the message via the server. 
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        
        server.quit()
        
        print("Email enviado")
        return 'Email enviado'
    except:
        print("Error al enviar mail")
        return "Error al enviar mail"


# **************************************************************************************************************************
# ****************************************************** Cargo a MySQL *****************************************************
# **************************************************************************************************************************
def motor():
    print("Iniciando ejecución de función motor")
    conexion=conect_db()
    cursor = conexion.cursor()

    # **************************************************************************************************************************
    # ************************************************ Importo datasets  *******************************************************
    # **************************************************************************************************************************

    # Obtenemos dataframe del proceso de ETL
    print("Iniciando proceso de etl")
    sellers = funciones_etl.sellers_etl()
    products = funciones_etl.products_etl()
    orders = funciones_etl.orders_etl()
    order_items = funciones_etl.order_items_etl()
    order_reviews = funciones_etl.order_reviews_etl()
    order_payments = funciones_etl.order_payments_etl()
    customers = funciones_etl.customers_etl()
    zip_code_prefix = funciones_etl.zip_code_prefix_etl()
    geolocation =funciones_etl.geolocation_etl()
    print("Proceso de etl finalizado correctamente")

    # **************************************************************************************************************************
    # ****************************************************** VALIDACIÓN ********************************************************
    # **************************************************************************************************************************
    def validate_df(dataframe):    
        match dataframe.columns[0]:        
            case "id_product":
                target = products
            case "id_seller":
                target = sellers
            case "id_customer":
                target = customers
            case "id_order":
                if dataframe.columns[1] == 'id_order_item':
                    target = order_items
                elif dataframe.columns[1] == 'payment_sequential':
                    target = order_payments
                else:
                    target = orders
            case "id_review":
                target = order_reviews

        # Verificar la cantidad de columnas
        if len(dataframe.columns) != len(target.columns):
            return False
        # Verificar los nombres de las columnas
        if set(dataframe.columns) != set(target.columns):
            return False
        # Verificar el tipo de datos de las columnas    
        for column, dtype in target.items():
            if dataframe[column].dtype != dtype:
                return False
        return True
    
    validacion=(validate_df(customers),
            validate_df(order_items), validate_df(order_payments),validate_df(order_reviews),
            validate_df(sellers),validate_df(products),validate_df(orders))
    
    
    enviado = False
    if (enviado == False):
        rta = enviar_email(validacion)
        enviado = True


        # PRODUCTS
        print("Iniciando proceso de creación de tablas")
        cursor.execute("""CREATE TABLE IF NOT EXISTS products(
                                                id_product VARCHAR(50) NOT NULL, 
                                                product_category_name VARCHAR(50) NOT NULL,
                                                product_name_lenght VARCHAR(10),
                                                product_description_lenght VARCHAR(10) NOT NULL,
                                                product_photos_qty VARCHAR(50) NOT NULL,
                                                product_weight_g VARCHAR(20) NOT NULL,
                                                product_length_cm VARCHAR(20) NOT NULL,
                                                product_height_cm VARCHAR(20) NOT NULL,
                                                product_width_cm VARCHAR(20) NOT NULL
                                                )
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM products;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        id_product=[]
        product_category_name=[]
        product_name_lenght=[]
        product_description_lenght=[]
        product_photos_qty=[]
        product_weight_g=[]
        product_length_cm=[]
        product_height_cm=[]
        product_width_cm=[]

        for i in range(len(sql)):
            id_product.append(sql[i][0])
            product_category_name.append(sql[i][1])
            product_name_lenght.append(sql[i][2])
            product_description_lenght.append(sql[i][3])
            product_photos_qty.append(sql[i][4])
            product_weight_g.append(sql[i][5])
            product_length_cm.append(sql[i][6])
            product_height_cm.append(sql[i][7])
            product_width_cm.append(sql[i][8])  

        # Armo el dataframe
        sql_dataframe['id_product']=id_product
        sql_dataframe['product_category_name']=product_category_name
        sql_dataframe['product_name_lenght']=product_name_lenght
        sql_dataframe['product_description_lenght']=product_description_lenght
        sql_dataframe['product_photos_qty']=product_photos_qty
        sql_dataframe['product_weight_g']=product_weight_g
        sql_dataframe['product_length_cm']=product_length_cm
        sql_dataframe['product_height_cm']=product_height_cm
        sql_dataframe['product_width_cm']=product_width_cm

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(products[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(products, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.id_product.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO products(
                                        id_product, 
                                        product_category_name,
                                        product_name_lenght,
                                        product_description_lenght,
                                        product_photos_qty,
                                        product_weight_g,
                                        product_length_cm,
                                        product_height_cm,
                                        product_width_cm)
                                        VALUES (%s, %s,%s, %s, %s, %s,%s, %s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE products SET product_name_lenght = NULL WHERE product_name_lenght = '';")
        cursor.execute("UPDATE products SET product_description_lenght = NULL WHERE product_description_lenght = '';")
        cursor.execute("UPDATE products SET product_photos_qty = NULL WHERE product_photos_qty = '';")
        cursor.execute("UPDATE products SET product_weight_g = NULL WHERE product_weight_g = '';")
        cursor.execute("UPDATE products SET product_length_cm = NULL WHERE product_length_cm = '';")
        cursor.execute("UPDATE products SET product_height_cm = NULL WHERE product_height_cm = '';")
        cursor.execute("UPDATE products SET product_width_cm = NULL WHERE product_width_cm = '';")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # SELLERS
        cursor.execute("""CREATE TABLE IF NOT EXISTS sellers(
                                                        id_seller VARCHAR(50) NOT NULL, 
                                                        id_code_prefix VARCHAR(20) NOT NULL)
                        ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM sellers;')

        sql = cursor.fetchall()

        sql_dataframe = pd.DataFrame()
        # Armo las series
        sellerid=[]
        id_code_prefix=[]

        for i in range(len(sql)):    
            sellerid.append(sql[i][0])    
            id_code_prefix.append(sql[i][1])     

        # Armo el dataframe
        sql_dataframe['id_seller']=sellerid
        sql_dataframe['id_code_prefix']=id_code_prefix

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(sellers[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(sellers, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.id_seller.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO sellers(
                                                    id_seller, 
                                                    id_code_prefix) VALUES (%s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE sellers SET id_code_prefix = NULL WHERE id_code_prefix = '';")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # ORDERS
        cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
                                            id_order VARCHAR(50) NOT NULL, 
                                            id_customer VARCHAR(50) NOT NULL,
                                            order_status VARCHAR(20) NOT NULL,
                                            order_purchase_timestamp VARCHAR(50) NOT NULL,
                                            order_approved_at VARCHAR(50) DEFAULT NULL,
                                            order_delivered_carrier_date VARCHAR(50) DEFAULT NULL,
                                            order_delivered_customer_date VARCHAR(50) DEFAULT NULL,
                                            order_estimated_delivery_date VARCHAR(50) DEFAULT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM orders;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        id_order=[]
        id_customer=[]
        order_status=[]
        order_purchase_timestamp=[]
        order_approved_at=[]
        order_delivered_carrier_date=[]
        order_delivered_customer_date=[]
        order_estimated_delivery_date=[]

        for i in range(len(sql)):
            id_order.append(sql[i][0])  
            id_customer.append(sql[i][1])  
            order_status.append(sql[i][2])  
            order_purchase_timestamp.append(sql[i][3])  
            order_approved_at.append(sql[i][4])  
            order_delivered_carrier_date.append(sql[i][5])  
            order_delivered_customer_date.append(sql[i][6])  
            order_estimated_delivery_date.append(sql[i][7])  

        # Armo el dataframe
        sql_dataframe['id_order']=id_order
        sql_dataframe['id_customer']=id_customer
        sql_dataframe['order_status']=order_status
        sql_dataframe['order_purchase_timestamp']=order_purchase_timestamp
        sql_dataframe['order_approved_at']=order_approved_at
        sql_dataframe['order_delivered_carrier_date']=order_delivered_carrier_date
        sql_dataframe['order_delivered_customer_date']=order_delivered_customer_date
        sql_dataframe['order_estimated_delivery_date']=order_estimated_delivery_date

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(orders[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(orders, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.id_order.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO orders(
                                                id_order, 
                                                id_customer,
                                                order_status,
                                                order_purchase_timestamp,
                                                order_approved_at,
                                                order_delivered_carrier_date,
                                                order_delivered_customer_date,
                                                order_estimated_delivery_date)
                                                VALUES (%s, %s,%s, %s, %s, %s,%s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE orders SET order_purchase_timestamp = NULL WHERE order_purchase_timestamp = '';")
        cursor.execute("UPDATE orders SET order_approved_at = NULL WHERE order_approved_at = '';")
        cursor.execute("UPDATE orders SET order_delivered_carrier_date = NULL WHERE order_delivered_carrier_date = '';")
        cursor.execute("UPDATE orders SET order_delivered_customer_date = NULL WHERE order_delivered_customer_date = '';")
        cursor.execute("UPDATE orders SET order_estimated_delivery_date = NULL WHERE order_estimated_delivery_date = '';")
        conexion.commit()
        
        # -----------------------------------------------------------------------------------------------------------------------
        # ORDER_REVIEWS
        cursor.execute("""CREATE TABLE IF NOT EXISTS order_reviews(
                                                    id_review VARCHAR(50) NOT NULL, 
                                                    id_order VARCHAR(50) NOT NULL,
                                                    review_score VARCHAR(5) NOT NULL,
                                                    review_comment_title VARCHAR(100) NOT NULL,
                                                    review_comment_message VARCHAR(500) NOT NULL,
                                                    review_creation_date VARCHAR(30) NOT NULL,
                                                    review_answer_timestamp VARCHAR(30) NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        # Query para llenar tabla
        cursor.execute('SELECT * FROM order_reviews;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        id_review=[]
        id_order=[]
        review_score=[]
        review_comment_title=[]
        review_comment_message=[]
        review_creation_date=[]
        review_answer_timestamp=[]

        for i in range(len(sql)):    
            id_review.append(sql[i][0])    
            id_order.append(sql[i][1])    
            review_score.append(sql[i][2])    
            review_comment_title.append(sql[i][3])
            review_comment_message.append(sql[i][4])
            review_creation_date.append(sql[i][5])
            review_answer_timestamp.append(sql[i][6])

        # Armo el dataframe
        sql_dataframe['id_review']=id_review
        sql_dataframe['id_order']=id_order
        sql_dataframe['review_score']=review_score
        sql_dataframe['review_comment_title']=review_comment_title
        sql_dataframe['review_comment_message']=review_comment_message
        sql_dataframe['review_creation_date']=review_creation_date
        sql_dataframe['review_answer_timestamp']=review_answer_timestamp

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(order_reviews[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(order_reviews, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.id_review.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO order_reviews (
                                        id_review, 
                                        id_order,
                                        review_score,
                                        review_comment_title,
                                        review_comment_message,
                                        review_creation_date,
                                        review_answer_timestamp)
                                        VALUES (%s, %s,%s, %s, %s, %s,%s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE order_reviews SET review_score = NULL WHERE review_score = '';")
        cursor.execute("UPDATE order_reviews SET review_creation_date = NULL WHERE review_creation_date = '';")
        cursor.execute("UPDATE order_reviews SET review_answer_timestamp = NULL WHERE review_answer_timestamp = '';")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # ORDER_PAYMENTS
        cursor.execute("""CREATE TABLE IF NOT EXISTS order_payments(id_order VARCHAR(50) NOT NULL, 
                                                    payment_sequential VARCHAR(5) NOT NULL,
                                                    payment_type VARCHAR(20) NOT NULL,
                                                    payment_installments VARCHAR(5) NOT NULL,
                                                    payment_value VARCHAR(20) NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        # Query para llenar tabla
        cursor.execute('SELECT * FROM order_payments;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        id_order=[]
        payment_sequential=[]
        payment_type=[]
        payment_installments=[]
        payment_value=[]

        for i in range(len(sql)):    
            id_order.append(sql[i][0])    
            payment_sequential.append(sql[i][1])    
            payment_type.append(sql[i][2])    
            payment_installments.append(sql[i][3])
            payment_value.append(sql[i][4])

        # Armo el dataframe
        sql_dataframe['id_order']=id_order
        sql_dataframe['payment_sequential']=payment_sequential
        sql_dataframe['payment_type']=payment_type
        sql_dataframe['payment_installments']=payment_installments
        sql_dataframe['payment_value']=payment_value

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(order_payments[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(order_payments, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.id_order.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))
            cursor.executemany("""INSERT INTO order_payments (
                                        id_order, 
                                        payment_sequential,
                                        payment_type,
                                        payment_installments,
                                        payment_value)
                                        VALUES (%s, %s,%s, %s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE order_payments SET payment_sequential = NULL WHERE payment_sequential = '';")
        cursor.execute("UPDATE order_payments SET payment_installments = NULL WHERE payment_installments = '';")
        cursor.execute("UPDATE order_payments SET payment_value = NULL WHERE payment_value = '';")
        conexion.commit()


        # -----------------------------------------------------------------------------------------------------------------------
        # ORDER_ITEMS
        cursor.execute("""CREATE TABLE IF NOT EXISTS order_items(
                                                        id_order VARCHAR(50) NOT NULL, 
                                                        id_order_item VARCHAR(10) NOT NULL,
                                                        id_product VARCHAR(50) NOT NULL,
                                                        id_seller VARCHAR(50) NOT NULL,
                                                        shipping_limit_date VARCHAR(50) NOT NULL,
                                                        price VARCHAR(20) NOT NULL,
                                                        freight_value VARCHAR(20) NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        # Query para llenar tabla
        cursor.execute('SELECT * FROM order_items;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        id_order=[]
        id_order_item=[]
        id_product=[]
        id_seller=[]
        shipping_limit_date=[]
        price=[]
        freight_value=[]

        for i in range(len(sql)):    
            id_order.append(sql[i][0])    
            id_order_item.append(sql[i][1])    
            id_product.append(sql[i][2])    
            id_seller.append(sql[i][3])
            shipping_limit_date.append(sql[i][4])
            price.append(sql[i][5])
            freight_value.append(sql[i][6])

        # Armo el dataframe
        sql_dataframe['id_order']=id_order
        sql_dataframe['id_order_item']=id_order_item
        sql_dataframe['id_product']=id_product
        sql_dataframe['id_seller']=id_seller
        sql_dataframe['shipping_limit_date']=shipping_limit_date
        sql_dataframe['price']=price
        sql_dataframe['freight_value']=freight_value

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(order_items[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(order_items, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.id_order.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))
            cursor.executemany("""INSERT INTO order_items (
                                        id_order, 
                                        id_order_item,
                                        id_product,
                                        id_seller,
                                        shipping_limit_date,
                                        price,
                                        freight_value)
                                        VALUES (%s, %s,%s, %s, %s, %s,%s)""", lista)
            conexion.commit() # actualizo para ver los datos
            
        # Cambio los vacios por null
        cursor.execute("UPDATE order_items SET id_order_item = NULL WHERE id_order_item = '';")
        cursor.execute("UPDATE order_items SET shipping_limit_date = NULL WHERE shipping_limit_date = '';")
        cursor.execute("UPDATE order_items SET price = NULL WHERE price = '';")
        cursor.execute("UPDATE order_items SET freight_value = NULL WHERE freight_value = '';")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # CUSTOMERS
        cursor.execute("""CREATE TABLE IF NOT EXISTS customers(
                                                            id_customer VARCHAR(50) NOT NULL, 
                                                            id_customer_unique VARCHAR(50) NOT NULL,
                                                            id_code_prefix VARCHAR(50) NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM customers;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        id_customer=[]
        id_customer_unique=[]
        id_code_prefix=[]

        for i in range(len(sql)):    
            id_customer.append(sql[i][0])    
            id_customer_unique.append(sql[i][1])    
            id_code_prefix.append(sql[i][2])    

        # Armo el dataframe
        sql_dataframe['id_customer']=id_customer
        sql_dataframe['id_customer_unique']=id_customer_unique
        sql_dataframe['id_code_prefix']=id_code_prefix

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(customers[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(customers, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.id_customer.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO customers (id_customer, 
                                                        id_customer_unique,
                                                        id_code_prefix)
                                                        VALUES (%s, %s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE customers SET id_code_prefix = NULL WHERE id_code_prefix = '';")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # ZIP_CODE_PREFIX
        cursor.execute("""CREATE TABLE IF NOT EXISTS zip_code_prefix(
                                                            id_state VARCHAR(10) NOT NULL,
                                                            id_code_prefix VARCHAR(50) NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM zip_code_prefix;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        id_state=[]
        id_code_prefix=[]

        for i in range(len(sql)):    
            id_state.append(sql[i][0])
            id_code_prefix.append(sql[i][1])

        # Armo el dataframe
        sql_dataframe['id_state']=id_state
        sql_dataframe['id_code_prefix']=id_code_prefix

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(zip_code_prefix[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(zip_code_prefix, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.id_state.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO zip_code_prefix(
                                                        id_state, 
                                                        id_code_prefix)VALUES (%s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos
        # -----------------------------------------------------------------------------------------------------------------------
        # GEOLOCATION
        cursor.execute("""CREATE TABLE IF NOT EXISTS geolocation(
                                                            id_state VARCHAR(5) NOT NULL, 
                                                            state_name VARCHAR(50) NOT NULL,
                                                            region VARCHAR(50) NOT NULL,
                                                            lat VARCHAR(50) NOT NULL,
                                                            lng VARCHAR(50) NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM geolocation;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        id_state=[]
        state_name=[]
        region=[]
        lat=[]
        lng=[]

        for i in range(len(sql)):    
            id_state.append(sql[i][0])    
            state_name.append(sql[i][1])    
            region.append(sql[i][2])    
            lat.append(sql[i][3])
            lng.append(sql[i][4])

        # Armo el dataframe
        sql_dataframe['id_state']=id_state
        sql_dataframe['state_name']=state_name
        sql_dataframe['region']=region
        sql_dataframe['lat']=lat
        sql_dataframe['lng']=lng

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(geolocation[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(geolocation, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.id_state.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO geolocation (id_state, 
                                                        state_name,
                                                        region,
                                                        lat,
                                                        lng)
                                                        VALUES (%s, %s, %s, %s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

    cursor.close()
    conexion.close()
    print('Se cerró la conexión a la DB')
    print("Carga finalizada")
    return 'Carga finalizada'

