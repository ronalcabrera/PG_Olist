# Importación de librerías
import pandas as  pd
import numpy as np

## A continuación de detallan las funciones para realizar el proceso de etl de cada dataset. 

# Limpieza del dataset olist_products_dataset
def products_etl():
    # Ingestamos dataset
    url = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_products_dataset.csv'
    products = pd.read_csv(url, delimiter=',', encoding='UTF-8')   
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    products.columns=products.columns.str.lower().strip()
    # Ingesto el dataset de categorias en inglés, para comparar
    url = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/product_category_name_translation.csv'
    cat_ingles = pd.read_csv(url, delimiter=',', encoding='UTF-8')
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    cat_ingles.columns=cat_ingles.columns.str.lower().strip()
    # Vamos a proceder a agregar estas categorías:
    cat_ingles.loc[len(cat_ingles)] = ['portateis_cozinha_e_preparadores_de_alimentos', 'kitchen_and_food_preparation_racks']
    cat_ingles.loc[len(cat_ingles)] = ['pc_gamer', 'pc_gamer']
    # Quitamos los guiones
    cat_ingles['product_category_name_english'] = cat_ingles['product_category_name_english'].str.replace('_',' ')
    # Ponemos la primer letra en mayúscula
    cat_ingles['product_category_name_english'] = cat_ingles['product_category_name_english'].str.capitalize()
    # Reemplazamos los nombres en portugués por los nombres en inglés:
    products['product_category_name'] = products['product_category_name'].map(cat_ingles.set_index('product_category_name')['product_category_name_english'])
    products = products[products.product_category_name.notnull()] # elimina 610 registros
    products = products[products.product_weight_g.notnull()] # elimina 1 registro
    return products

# Limpieza del dataset olist_sellers_dataset
def sellers_etl():
    # Ingestamos dataset
    url = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_sellers_dataset.csv'
    sellers = pd.read_csv(url, delimiter=',', encoding='UTF-8')
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    sellers.columns=sellers.columns.str.lower().strip()
    # Creamos dataset limpio
    return sellers

#Limpieza del dataset olist_customers_dataset
def customers_etl():
    # Ingestamos dataset
    url = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_customers_dataset.csv'
    customers = pd.read_csv(url, delimiter=',', encoding='UTF-8')
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    customers.columns=customers.columns.str.lower().strip()
    return customers

#Limpieza del dataset olist_orders_dataset
def orders_etl():
    # Ingestamos dataset
    url = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_orders_dataset.csv'
    orders = pd.read_csv(url, delimiter=',', encoding='UTF-8')
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    orders.columns=orders.columns.str.lower().strip()
    # Cambiamos los tipos de datos para las fechas
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], format='%Y/%m/%d')
    orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'], format='%Y/%m/%d')
    orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'], format='%Y/%m/%d')
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'], format='%Y/%m/%d')
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'], format='%Y/%m/%d') 
    return orders

# Limpieza del dataset olist_geolocation_dataset
def geolocation_etl():
    # Ingestamos dataset
    url = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_geolocation_dataset.csv'
    geolocation = pd.read_csv(url, delimiter=',', encoding='UTF-8')
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    geolocation.columns=geolocation.columns.str.lower().strip()
    return geolocation

# Limpieza del dataset olist_marketing_qualified_leads_dataset
def marketing_qualified_leads_etl():
    # Ingestamos dataset
    url='https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_marketing_qualified_leads_dataset.csv'
    marketing_qualified_leads=pd.read_csv(url, delimiter=',', encoding='UTF-8')
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    marketing_qualified_leads.columns=marketing_qualified_leads.columns.str.lower().strip()
    # En la columna 'origin' reemplamos los NaN por 'Sin Dato'
    marketing_qualified_leads['origin']=marketing_qualified_leads['origin'].replace(np.nan,'Sin Dato')
    # Cambiaremos el tipo de dato de la columna 'first_contact_date'
    marketing_qualified_leads['first_contact_date']=marketing_qualified_leads['first_contact_date'].astype('datetime64')
    return marketing_qualified_leads

#Limpieza del dataset olist_order_items_dataset
def order_items_etl():
    # Ingestamos dataset
    url = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_order_items_dataset.csv'
    df_order_items = pd.read_csv(url, delimiter=',', encoding='UTF-8')
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    df_order_items.columns=df_order_items.columns.str.lower().strip()   
    # Cambiar la columna shipping_limit_date a tipo datetime
    df_order_items['shipping_limit_date'] = pd.to_datetime(df_order_items['shipping_limit_date'])
    return df_order_items

#Limpieza del dataset olist_order_payments_dataset
def order_payments_etl():
    # Ingestamos dataset
    url='https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_order_payments_dataset.csv'
    payments= pd.read_csv(url, delimiter=',', encoding='UTF-8') 
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    payments.columns=payments.columns.str.lower().strip()
    return payments

#Limpieza del dataset olist_order_reviews_dataset
def order_reviews_etl():
    # Ingestamos dataset
    url='https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_order_reviews_dataset.csv'
    reviews=pd.read_csv(url, delimiter=',', encoding='UTF-8')
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    reviews.columns=reviews.columns.str.lower().strip()
    # Reemplazo los NaN por 'Sin Dato'
    reviews['review_comment_title'] = reviews['review_comment_title'].replace(np.nan,'Sin Dato')
    # Reemplazo los saltos de lineas por ' ' 
    reviews['review_comment_title'] = reviews['review_comment_title'].str.replace('\n',' ')
    # Remplezo en los mensajes que inician con el o finalizan con "
    reviews['review_comment_title'] = reviews['review_comment_title'].str.replace('"','')    
    # Reemplazo los NaN por 'Sin Dato'
    reviews['review_comment_message'] = reviews['review_comment_message'].replace(np.nan,'Sin Dato')
    # Reemplazo los saltos de linea por ' '
    reviews['review_comment_message'] = reviews['review_comment_message'].str.replace('\n',' ')
    # Remplezo en los mensajes que inician con el o finalizan con "
    reviews['review_comment_message'] = reviews['review_comment_message'].str.replace('"','')
    # Al hacer este cambio de tipo de dato, la hora se sacará porque todas son 00
    # Cambio tipo de dato : de 'object' a 'datetime64'
    reviews['review_creation_date']=reviews['review_creation_date'].astype('datetime64')
    # Cambio tipo de dato : de 'object' a 'datetime64'
    reviews['review_answer_timestamp']=reviews['review_answer_timestamp'].astype('datetime64')
    return reviews

# Limpieza del dataset olist_closed_deals_dataset
def closed_deals_etl():
    # Ingestamos dataset
    url = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_closed_deals_dataset.csv'
    df_closed_deals = pd.read_csv(url, delimiter=',', encoding='UTF-8') 
    # Converimos el nombre de las columnas en minúsculas y eliminamos espacios
    df_closed_deals.columns=df_closed_deals.columns.str.lower().strip()
    df_closed_deals.drop_duplicates() # No hay duplicados
    # Cambiar la columna won_date a tipo datetime
    df_closed_deals['won_date'] = pd.to_datetime(df_closed_deals['won_date']) 
    # Reemplazamos los valores NaN por 'Sin dato'
    df_closed_deals.fillna({'business_segment': 'Sin dato', 'lead_type': 'Sin dato', 'lead_behaviour_profile': 'Sin dato', 
                            'has_company': 'Sin dato' ,'has_gtin': 'Sin dato','average_stock': 'Sin dato',
                            'business_type': 'Sin dato'}, inplace=True)   
    # Reemplazamos en average_stock los 'unknown' por 'Sin dato'
    df_closed_deals['average_stock'].replace('unknown','Sin dato', inplace=True)
    return df_closed_deals

#Crearemos una función que consistirá en la construcción de un dataframe llamado "zip_code_prefix"
def zip_code_prefix_etl():
    # Ingestamos datasets
    url1 = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_sellers_dataset.csv'
    url2 = 'https://raw.githubusercontent.com/ronalcabrera/PG_Olist/main/Datasets/olist_customers_dataset.csv'
    sellers = pd.read_csv(url1, delimiter=',', encoding='UTF-8')
    customers = pd.read_csv(url2, delimiter=',', encoding='UTF-8')
    # Creo tabla con los prefijos y sus correspondientes estados
    # Separo los prefijos únicos de ambas tablas y las convierto en listas.
    prefix = customers['customer_zip_code_prefix'].unique().tolist()
    aux = sellers['seller_zip_code_prefix'].unique().tolist()

    # Agrego a la lista final únicamente los prefijos que no estaban en el otro dataframe.
    for item in aux:
        if not(item in prefix):
            prefix.append(item)

    # Creo el dataframe que voy a exportar, y agrego la columna prefijos.
    zip_code_prefix = pd.DataFrame()
    zip_code_prefix['prefix'] = prefix

    # Ahora le agrego la columna del estado correspondiente a cada prefijo
    czcp = zip_code_prefix.prefix # abrevio para escribir menos y sea mas facil leer.

    zip_code_prefix['customer_state'] = np.where((czcp<20000),'SP',
                                        np.where((czcp>19999)&(czcp<29000),'RJ',
                                        np.where((czcp>28999)&(czcp<30000),'ES',
                                        np.where((czcp>29999)&(czcp<40000),'MG',
                                        np.where((czcp>39999)&(czcp<49000),'BA',
                                        np.where((czcp>48999)&(czcp<50000),'SE',
                                        np.where((czcp>49999)&(czcp<57000),'PE',
                                        np.where((czcp>56999)&(czcp<58000),'AL',
                                        np.where((czcp>57999)&(czcp<59000),'PB',
                                        np.where((czcp>58999)&(czcp<60000),'RN',
                                        np.where((czcp>59999)&(czcp<64000),'CE',
                                        np.where((czcp>63999)&(czcp<65000),'PI',
                                        np.where((czcp>64999)&(czcp<66000),'MA',
                                        np.where((czcp>65999)&(czcp<68900),'PA',
                                        np.where((czcp>68899)&(czcp<69000),'AP',
                                        np.where((czcp>68999)&(czcp<69300),'AM',
                                        np.where((czcp>69299)&(czcp<69400),'RR',
                                        np.where((czcp>69399)&(czcp<69900),'AM',
                                        np.where((czcp>69899)&(czcp<70000),'AC',
                                        np.where((czcp>69999)&(czcp<72800),'DF',
                                        np.where((czcp>72799)&(czcp<73000),'GO',
                                        np.where((czcp>72999)&(czcp<73404),'DF',
                                        np.where((czcp>73403)&(czcp<76800),'GO',
                                        np.where((czcp>76799)&(czcp<77000),'RO',
                                        np.where((czcp>76999)&(czcp<78000),'TO',
                                        np.where((czcp>77999)&(czcp<78900),'MT',
                                        np.where((czcp>78899)&(czcp<79000),'RO',
                                        np.where((czcp>78999)&(czcp<80000),'MS',
                                        np.where((czcp>79999)&(czcp<88000),'PR',
                                        np.where((czcp>87999)&(czcp<90000),'SC',
                                        np.where((czcp>89999)&(czcp<100000),'SC',
                                        'S/D' # Si no esta en el rango, sin datos.
                                        )))))))))))))))))))))))))))))))
    zcpc = zip_code_prefix.customer_state.values

    zip_code_prefix['lat'] =    np.where(zcpc=='SP',-9.974,
                                np.where(zcpc=='RJ',-22.90642,
                                np.where(zcpc=='ES',-22.11583,
                                np.where(zcpc=='MG',-21.235,
                                np.where(zcpc=='BA',-12.97111,
                                np.where(zcpc=='SE',-10.91111,
                                np.where(zcpc=='PE',-8.05389,
                                np.where(zcpc=='AL',-9.66583,
                                np.where(zcpc=='PB',-7.115,
                                np.where(zcpc=='RN',-5.795,
                                np.where(zcpc=='CE',-3.71722,
                                np.where(zcpc=='PI',-5.08917,
                                np.where(zcpc=='MA',-2.52972,
                                np.where(zcpc=='PA',-1.45583,
                                np.where(zcpc=='AP',0.03889,
                                np.where(zcpc=='AM',-3.10194,
                                np.where(zcpc=='RR',2.81972,
                                np.where(zcpc=='AC',-9.97472,
                                np.where(zcpc=='DF',-15.77972,
                                np.where(zcpc=='GO',-16.67861,
                                np.where(zcpc=='RO',-8.76194,
                                np.where(zcpc=='TO',-10.16745,
                                np.where(zcpc=='MT',-15.59611,
                                np.where(zcpc=='MS',-20.44278,
                                np.where(zcpc=='PR',-25.42778,
                                np.where(zcpc=='SC',-27.59667,
                                'S/D'
                                ))))))))))))))))))))))))))

    zip_code_prefix['long'] =   np.where(zcpc=='SP',-67.8076974,
                                np.where(zcpc=='RJ',-43.18223,
                                np.where(zcpc=='ES',-46.68278,
                                np.where(zcpc=='MG',-45.75861,
                                np.where(zcpc=='BA',-38.51083,
                                np.where(zcpc=='SE',-37.07167,
                                np.where(zcpc=='PE',-34.88111,
                                np.where(zcpc=='AL',-35.73528,
                                np.where(zcpc=='PB',-34.86306,
                                np.where(zcpc=='RN',-35.20944,
                                np.where(zcpc=='CE',-38.54306,
                                np.where(zcpc=='PI',-42.80194,
                                np.where(zcpc=='MA',-44.30278,
                                np.where(zcpc=='PA',-48.50444,
                                np.where(zcpc=='AP',-51.06639,
                                np.where(zcpc=='AM',-60.025,
                                np.where(zcpc=='RR',-60.67333,
                                np.where(zcpc=='AC',-67.81,
                                np.where(zcpc=='DF',-47.92972,
                                np.where(zcpc=='GO',-49.25389,
                                np.where(zcpc=='RO',-63.90389,
                                np.where(zcpc=='TO',-48.32766,
                                np.where(zcpc=='MT',-56.09667,
                                np.where(zcpc=='MS',-54.64639,
                                np.where(zcpc=='PR',-49.27306,
                                np.where(zcpc=='SC',-48.54917,
                                'S/D'
                                ))))))))))))))))))))))))))
    return zip_code_prefix




