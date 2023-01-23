# **************************************************************************************************************************
# ****************************************************** Librerias *********************************************************
# **************************************************************************************************************************
import pymysql
import sqlalchemy
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
                host = 'aws-sa-east-1.connect.psdb.cloud',
                user = 'hdj11vgbubzez1k2mmw0',
                passwd = 'pscale_pw_xJtpCj9sIr1JRelAqFEIRExmGep2kJrFs12dxipAZrZ',
                db = 'grupo7_pg',
                ssl={"rejectUnauthorized":True})
        cursor = conexion.cursor()
        print("Conexión con base de dato establecida correctamente")
        return [cursor, conexion]
    except:
        print("Error al conectarse a la db")



def enviar_email(validaciones):
    try:
        # create message object instance 
        msg = MIMEMultipart()    
        message = """Reporte automático sobre integridad de datos en base de datos Olist
                                
                    • closed_deals: {}
                    • customers: {} 
                    • marketing_qualified_leads: {} 
                    • order_items: {} 
                    • order_payments: {} 
                    • order_reviews: {} 
                    • orders: {} 
                    • products: {} 
                    • sellers: {} 
                """.format(validaciones[0],validaciones[1],validaciones[2],
                            validaciones[3],validaciones[4],validaciones[5],
                            validaciones[6],validaciones[7],validaciones[8])
        
        # setup the parameters of the message 
        password = "nkdmrcazjvrtoqly"
        msg['From'] = "grupo3.pg@gmail.com"
        msg['To'] = "mmacielaortiz@gmail.com"
        msg['Subject'] = "Probando"
        
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
    db = conect_db()
    cursor = db[0]
    conexion = db[1]

    # **************************************************************************************************************************
    # ************************************************ Importo datasets de la API **********************************************
    # **************************************************************************************************************************

    # Obtenemos dataframe de la API
    print("Iniciando proceso de etl")
    sellers = funciones_etl.sellers_etl()
    products = funciones_etl.products_etl()
    orders = funciones_etl.orders_etl()
    order_items = funciones_etl.order_items_etl()
    order_reviews = funciones_etl.order_reviews_etl()
    order_payments = funciones_etl.order_payments_etl()
    closed_deals = funciones_etl.closed_deals_etl()
    customers = funciones_etl.customers_etl()
    marketing_qualified_leads = funciones_etl.marketing_qualified_leads_etl()
    zip_code_prefix = funciones_etl.zip_code_prefix_etl()
    print("Proceso de etl finalizado correctamente")

    # **************************************************************************************************************************
    # ****************************************************** VALIDACIÓN ********************************************************
    # **************************************************************************************************************************
    def validate_df(dataframe):    
        match dataframe.columns[0]:        
            case "product_id":
                target = products
            case "seller_id":
                target = sellers
            case "customer_id":
                target = customers
            case "order_id":
                if dataframe.columns[1] == 'order_item_id':
                    target = order_items
                elif dataframe.columns[1] == 'payment_sequential':
                    target = order_payments
                else:
                    target = orders
            case "mql_id":
                if dataframe.columns[1] == 'seller_id':
                    target = closed_deals
                else:
                    target = marketing_qualified_leads
            case "review_id":
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
    
    validacion=(validate_df(closed_deals),validate_df(customers),validate_df(marketing_qualified_leads),
            validate_df(order_items), validate_df(order_payments),validate_df(order_reviews),
            validate_df(sellers),validate_df(products),validate_df(orders))
    
    
    enviado = False
    if (enviado == False):
        rta = enviar_email(validacion)
        enviado = True

    #if (rta == 'Mensaje enviado'):
        # PRODUCTS
        cursor.execute("""CREATE TABLE IF NOT EXISTS products(
                                                product_id VARCHAR(50) NOT NULL, 
                                                product_category_name VARCHAR(50) NOT NULL,
                                                product_name_lenght VARCHAR(10),
                                                product_description_lenght VARCHAR(10) NOT NULL,
                                                product_photos_qty INT NOT NULL,
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
        product_id=[]
        product_category_name=[]
        product_name_lenght=[]
        product_description_lenght=[]
        product_photos_qty=[]
        product_weight_g=[]
        product_length_cm=[]
        product_height_cm=[]
        product_width_cm=[]

        for i in range(len(sql)):
            product_id.append(sql[i][0])
            product_category_name.append(sql[i][1])
            product_name_lenght.append(sql[i][2])
            product_description_lenght.append(sql[i][3])
            product_photos_qty.append(sql[i][4])
            product_weight_g.append(sql[i][5])
            product_length_cm.append(sql[i][6])
            product_height_cm.append(sql[i][7])
            product_width_cm.append(sql[i][8])  

        # Armo el dataframe
        sql_dataframe['product_id']=product_id
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
        filas_max = len(filtro.product_id.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO products(
                                        product_id, 
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
                                                        seller_id VARCHAR(50) NOT NULL, 
                                                        seller_zip_code_prefix VARCHAR(20) NOT NULL,
                                                        seller_city VARCHAR(50) NOT NULL,
                                                        seller_state VARCHAR(5) NOT NULL)
                        ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM sellers;')

        sql = cursor.fetchall()

        sql_dataframe = pd.DataFrame()
        # Armo las series
        sellerid=[]
        seller_zip_code_prefix=[]
        seller_city=[]
        seller_state=[]

        for i in range(len(sql)):    
            sellerid.append(sql[i][0])    
            seller_zip_code_prefix.append(sql[i][1])    
            seller_city.append(sql[i][2])    
            seller_state.append(sql[i][3])

        # Armo el dataframe
        sql_dataframe['seller_id']=sellerid
        sql_dataframe['seller_zip_code_prefix']=seller_zip_code_prefix
        sql_dataframe['seller_city']=seller_city
        sql_dataframe['seller_state']=seller_state

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(sellers[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(sellers, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.seller_id.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO sellers(
                                                    seller_id, 
                                                    seller_zip_code_prefix,
                                                    seller_city,
                                                    seller_state
                                                    )VALUES (%s, %s,%s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE sellers SET seller_zip_code_prefix = NULL WHERE seller_zip_code_prefix = '';")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # ORDERS
        cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
                                            order_id VARCHAR(50) NOT NULL, 
                                            customer_id VARCHAR(50) NOT NULL,
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
        order_id=[]
        customer_id=[]
        order_status=[]
        order_purchase_timestamp=[]
        order_approved_at=[]
        order_delivered_carrier_date=[]
        order_delivered_customer_date=[]
        order_estimated_delivery_date=[]

        for i in range(len(sql)):
            order_id.append(sql[i][0])  
            customer_id.append(sql[i][1])  
            order_status.append(sql[i][2])  
            order_purchase_timestamp.append(sql[i][3])  
            order_approved_at.append(sql[i][4])  
            order_delivered_carrier_date.append(sql[i][5])  
            order_delivered_customer_date.append(sql[i][6])  
            order_estimated_delivery_date.append(sql[i][7])  

        # Armo el dataframe
        sql_dataframe['order_id']=order_id
        sql_dataframe['customer_id']=customer_id
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
        filas_max = len(filtro.order_id.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO orders(
                                                order_id, 
                                                customer_id,
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
        # MARKETING_QUALIFIED_LEADS
        cursor.execute("""CREATE TABLE IF NOT EXISTS marketing_qualified_leads(
                                                                            mql_id VARCHAR(50) NOT NULL, 
                                                                            first_contact_date VARCHAR(30) NOT NULL,
                                                                            landing_page_id VARCHAR(50) NOT NULL,
                                                                            origin VARCHAR(20) NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM marketing_qualified_leads;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        mql_id=[]
        first_contact_date=[]
        landing_page_id=[]
        origin=[]

        for i in range(len(sql)):
            mql_id.append(sql[i][0])  
            first_contact_date.append(sql[i][1])  
            landing_page_id.append(sql[i][2])  
            origin.append(sql[i][3])  

        # Armo el dataframe
        sql_dataframe['mql_id']=mql_id
        sql_dataframe['first_contact_date']=first_contact_date
        sql_dataframe['landing_page_id']=landing_page_id
        sql_dataframe['origin']=origin

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(marketing_qualified_leads[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(marketing_qualified_leads, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.mql_id.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO marketing_qualified_leads(
                                                mql_id, 
                                                first_contact_date,
                                                landing_page_id,
                                                origin)VALUES (%s, %s,%s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE marketing_qualified_leads SET first_contact_date = NULL WHERE first_contact_date = '';")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # ORDER_REVIEWS
        cursor.execute("""CREATE TABLE IF NOT EXISTS order_reviews(
                                                    review_id VARCHAR(50) NOT NULL, 
                                                    order_id VARCHAR(50) NOT NULL,
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
        review_id=[]
        order_id=[]
        review_score=[]
        review_comment_title=[]
        review_comment_message=[]
        review_creation_date=[]
        review_answer_timestamp=[]

        for i in range(len(sql)):    
            review_id.append(sql[i][0])    
            order_id.append(sql[i][1])    
            review_score.append(sql[i][2])    
            review_comment_title.append(sql[i][3])
            review_comment_message.append(sql[i][4])
            review_creation_date.append(sql[i][5])
            review_answer_timestamp.append(sql[i][6])

        # Armo el dataframe
        sql_dataframe['review_id']=review_id
        sql_dataframe['order_id']=order_id
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
        filas_max = len(filtro.review_id.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO order_reviews (
                                        review_id, 
                                        order_id,
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS  order_payments(order_id VARCHAR(50) NOT NULL, 
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
        order_id=[]
        payment_sequential=[]
        payment_type=[]
        payment_installments=[]
        payment_value=[]

        for i in range(len(sql)):    
            order_id.append(sql[i][0])    
            payment_sequential.append(sql[i][1])    
            payment_type.append(sql[i][2])    
            payment_installments.append(sql[i][3])
            payment_value.append(sql[i][4])

        # Armo el dataframe
        sql_dataframe['order_id']=order_id
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
        filas_max = len(filtro.order_id.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))
            cursor.executemany("""INSERT INTO order_payments (
                                        order_id, 
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
                                                        order_id VARCHAR(50) NOT NULL, 
                                                        order_item_id VARCHAR(10) NOT NULL,
                                                        product_id VARCHAR(50) NOT NULL,
                                                        seller_id VARCHAR(50) NOT NULL,
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
        order_id=[]
        order_item_id=[]
        product_id=[]
        seller_id=[]
        shipping_limit_date=[]
        price=[]
        freight_value=[]

        for i in range(len(sql)):    
            order_id.append(sql[i][0])    
            order_item_id.append(sql[i][1])    
            product_id.append(sql[i][2])    
            seller_id.append(sql[i][3])
            shipping_limit_date.append(sql[i][4])
            price.append(sql[i][5])
            freight_value.append(sql[i][6])

        # Armo el dataframe
        sql_dataframe['order_id']=order_id
        sql_dataframe['order_item_id']=order_item_id
        sql_dataframe['product_id']=product_id
        sql_dataframe['seller_id']=seller_id
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
        filas_max = len(filtro.order_id.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))
            cursor.executemany("""INSERT INTO order_items (
                                        order_id, 
                                        order_item_id,
                                        product_id,
                                        seller_id,
                                        shipping_limit_date,
                                        price,
                                        freight_value)
                                        VALUES (%s, %s,%s, %s, %s, %s,%s)""", lista)
            conexion.commit() # actualizo para ver los datos
            
        # Cambio los vacios por null
        cursor.execute("UPDATE order_items SET order_item_id = NULL WHERE order_item_id = '';")
        cursor.execute("UPDATE order_items SET shipping_limit_date = NULL WHERE shipping_limit_date = '';")
        cursor.execute("UPDATE order_items SET price = NULL WHERE price = '';")
        cursor.execute("UPDATE order_items SET freight_value = NULL WHERE freight_value = '';")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # CUSTOMERS
        cursor.execute("""CREATE TABLE IF NOT EXISTS customers(
                                                            customer_id VARCHAR(50) NOT NULL, 
                                                            customer_unique_id VARCHAR(50) NOT NULL,
                                                            customer_zip_code_prefix VARCHAR(50) NOT NULL,
                                                            customer_city VARCHAR(50) NOT NULL,
                                                            customer_state VARCHAR(5) NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM customers;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        customer_id=[]
        customer_unique_id=[]
        customer_zip_code_prefix=[]
        customer_city=[]
        customer_state=[]

        for i in range(len(sql)):    
            customer_id.append(sql[i][0])    
            customer_unique_id.append(sql[i][1])    
            customer_zip_code_prefix.append(sql[i][2])    
            customer_city.append(sql[i][3])
            customer_state.append(sql[i][4])

        # Armo el dataframe
        sql_dataframe['customer_id']=customer_id
        sql_dataframe['customer_unique_id']=customer_unique_id
        sql_dataframe['customer_zip_code_prefix']=customer_zip_code_prefix
        sql_dataframe['customer_city']=customer_city
        sql_dataframe['customer_state']=customer_state

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(customers[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(customers, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.customer_id.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO customers (customer_id, 
                                                        customer_unique_id,
                                                        customer_zip_code_prefix,
                                                        customer_city,
                                                        customer_state)
                                                        VALUES (%s, %s, %s, %s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE customers SET customer_zip_code_prefix = NULL WHERE customer_zip_code_prefix = '';")
        conexion.commit()

        # Cambio de tipo de columna
        cursor.execute("ALTER TABLE customers MODIFY COLUMN customer_zip_code_prefix INT;")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # CLOSED_DEALS
        cursor.execute("""CREATE TABLE IF NOT EXISTS closed_deals(
                                                            mql_id VARCHAR(50) NOT NULL, 
                                                            seller_id VARCHAR(50) NOT NULL,
                                                            sdr_id VARCHAR(50) NOT NULL,
                                                            sr_id VARCHAR(50) NOT NULL,
                                                            won_date VARCHAR(50) NOT NULL,
                                                            business_segment VARCHAR(50) NOT NULL,
                                                            lead_type VARCHAR(20) NOT NULL,
                                                            lead_behaviour_profile VARCHAR(20) NOT NULL,
                                                            has_company VARCHAR(10) NOT NULL,
                                                            has_gtin VARCHAR(10) NOT NULL,
                                                            average_stock VARCHAR(10) NOT NULL,
                                                            business_type VARCHAR(20) NOT NULL,
                                                            declared_product_catalog_size VARCHAR(50) DEFAULT NULL,
                                                            declared_monthly_revenue VARCHAR(20) NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM closed_deals;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        mql_id=[]
        seller_id=[]
        sdr_id=[]
        sr_id=[]
        won_date=[]
        business_segment=[]
        lead_type=[]
        lead_behaviour_profile=[]
        has_company=[]
        has_gtin=[]
        average_stock=[]
        business_type=[]
        declared_product_catalog_size=[]
        declared_monthly_revenue=[]

        for i in range(len(sql)):    
            mql_id.append(sql[i][0])    
            seller_id.append(sql[i][1])    
            sdr_id.append(sql[i][2])    
            sr_id.append(sql[i][3])
            won_date.append(sql[i][4])
            business_segment.append(sql[i][5])
            lead_type.append(sql[i][6])
            lead_behaviour_profile.append(sql[i][7])
            has_company.append(sql[i][8])
            has_gtin.append(sql[i][9])
            average_stock.append(sql[i][10])
            business_type.append(sql[i][11])
            declared_product_catalog_size.append(sql[i][12])
            declared_monthly_revenue.append(sql[i][13])

        # Armo el dataframe
        sql_dataframe['mql_id']=mql_id
        sql_dataframe['seller_id']=seller_id
        sql_dataframe['sdr_id']=sdr_id
        sql_dataframe['sr_id']=sr_id
        sql_dataframe['won_date']=won_date
        sql_dataframe['business_segment']=business_segment
        sql_dataframe['lead_type']=lead_type
        sql_dataframe['lead_behaviour_profile']=lead_behaviour_profile
        sql_dataframe['has_company']=has_company
        sql_dataframe['has_gtin']=has_gtin
        sql_dataframe['average_stock']=average_stock
        sql_dataframe['business_type']=business_type
        sql_dataframe['declared_product_catalog_size']=declared_product_catalog_size
        sql_dataframe['declared_monthly_revenue']=declared_monthly_revenue

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(closed_deals[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(closed_deals, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.mql_id.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))
            cursor.executemany("""INSERT INTO closed_deals (
                                                    mql_id, 
                                                    seller_id,
                                                    sdr_id,
                                                    sr_id,
                                                    won_date,
                                                    business_segment,
                                                    lead_type,
                                                    lead_behaviour_profile,
                                                    has_company,
                                                    has_gtin,
                                                    average_stock,
                                                    business_type,
                                                    declared_product_catalog_size,
                                                    declared_monthly_revenue)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos

        # Cambio los vacios por null
        cursor.execute("UPDATE closed_deals SET won_date = NULL WHERE won_date = '';")
        cursor.execute("UPDATE closed_deals SET declared_product_catalog_size = NULL WHERE declared_product_catalog_size = '';")
        cursor.execute("UPDATE closed_deals SET declared_monthly_revenue = NULL WHERE declared_monthly_revenue = '';")
        conexion.commit()

        # -----------------------------------------------------------------------------------------------------------------------
        # ZIP_CODE_PREFIX
        cursor.execute("""CREATE TABLE IF NOT EXISTS zip_code_prefix(
                                                            prefix INT NOT NULL, 
                                                            customer_state VARCHAR(50) NOT NULL,
                                                            lat FLOAT NOT NULL,
                                                            long FLOAT NOT NULL)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;""") # Ejecute cualquier Query deseada
        conexion.commit() # actualizo para ver los datos

        cursor.execute('SELECT * FROM zip_code_prefix;')
        sql = cursor.fetchall()
        sql_dataframe = pd.DataFrame()

        # Armo las series
        prefix=[]
        customer_state=[]
        lat=[]
        long=[]

        for i in range(len(sql)):    
            prefix.append(sql[i][0])
            customer_state.append(sql[i][1])
            lat.append(sql[i][2])
            long.append(sql[i][3])

        # Armo el dataframe
        sql_dataframe['prefix']=prefix
        sql_dataframe['customer_state']=customer_state
        sql_dataframe['lat']=lat
        sql_dataframe['long']=long

        # Normalizamos los tipos de dato
        lst = sql_dataframe.columns.to_list()
        for i in range(len(lst)):
            sql_dataframe[lst[i]] = sql_dataframe[lst[i]].astype(zip_code_prefix[lst[i]].dtype)

        # Check de informacion nueva
        filtro = sql_dataframe.merge(zip_code_prefix, how='outer', indicator='union')
        filtro = filtro[filtro['union']=='right_only']
        filtro = filtro[filtro.columns[:-1]]

        # Carga a base de datos, de ser necesario.
        filas_max = len(filtro.prefix.to_list())
        if filas_max > 0:
            lista = []
            for i in range (filas_max):
                lista.append(tuple(filtro.iloc[i]))

            cursor.executemany("""INSERT INTO zip_code_prefix(
                                                        prefix, 
                                                        customer_state,
                                                        lat,
                                                        long)VALUES (%s, %s, %s, %s)""", lista)
            conexion.commit() # actualizo para ver los datos
        
    print("Carga finalizada")
    return 'Carga finalizada'