import os
import sqlite3
import time
import xml.etree.ElementTree as ET
from slugify import slugify
import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
import random


conn = mysql.connector.connect(
    host="localhost",
    database="falex728_978.com.ua",
    user="falex728_ilya",
    password="Vbvb2003")

tree = ET.parse('wByx7xJQyn5PoYIF.xml')
root = tree.getroot()


def fell_top_category(root):
    for num in range(1, 4):
        for i in root.findall(f'./shop/categories/category[@id="{num}"]'):
            top_category_id = i.attrib["id"]
            title = i.text
            slug = slugify(i.text)
            data = f"""
            DO $$  
            BEGIN
                IF NOT EXISTS
                    ( SELECT FROM mainapp_topcategory topcategory WHERE topcategory.id = {top_category_id}) 
                THEN 
                    INSERT INTO mainapp_topcategory(id, title, slug) VALUES(%s,%s,%s);
                END IF;
            END
            $$;
                """
            c = conn.cursor()
            c.execute(data, (top_category_id, title, slug))
    return conn.commit()


def fell_category(root):
    for i in root.findall(f'./shop/categories/category[@parent_id]'):
        category_id = i.attrib["id"]
        title = i.text.replace(' ', '')
        slug = slugify(i.text)
        slug_text = f'{slug}-{random.randint(1, 4000)}'
        top_category_id = i.attrib["parent_id"]
        # data = """INSERT INTO mainapp_category(id, title ,slug, top_category_id) VALUES(?,?,?,?)"""
        data = f"""
                   DO $$  
                   BEGIN
                       IF NOT EXISTS
                           ( SELECT FROM mainapp_category category WHERE category.id = {category_id}) 
                       THEN 
                           INSERT INTO mainapp_category(title, slug, top_category_id, id) VALUES(%s,%s,%s,%s);
                       END IF;
                   END
                   $$;
                       """
        c = conn.cursor()
        try:
            c.execute(data, (title, slug_text, top_category_id, category_id))
        except errors.lookup(UNIQUE_VIOLATION, ):
            c.execute(data, (title, f'{slug}-{random.randint(1, 4000)}', top_category_id, category_id))
    return conn.commit()


def download_media(root):
    start = time.time()
    f = []
    m = []
    g = []
    for i in root.findall('./shop/offers/offer'):
        img = i.findall('picture')
        m.append(img)
        product_id = i.find('vendorCode')
        g.append(product_id)
        num = len(img)
        for a in img:
            file_name = f'media/images/product/{product_id.text}-{random.randint(1, 1000)}.jpg'
            f.append(a)
            import requests
            # file_name = f'media/product/{product_id}.jpg'
            with open(f'{file_name}', 'wb') as handle:
                response = requests.get(str(a.text.strip()),
                                        stream=True)
                if not response.ok:
                    print(f'{a.text} - {response.status_code}')
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
        time.sleep(0.1)
    end = time.time() - start
    print(end)
    return end


def filling_product_img_table(root):
    c = conn.cursor()
    select = """SELECT id FROM mainapp_product WHERE product_code=(%s)"""
    for i in root.findall('./shop/offers/offer'):
        vendorCode = i.find('vendorCode').text
        c.execute(select, (vendorCode,))
        ids = c.fetchall()
        for file in os.listdir('media/images/product'):
            for id in ids:
                if file.startswith(f'{vendorCode}'):
                    data = f"""
                                                  DO $$  
                                                  BEGIN
                                                      IF NOT EXISTS
                                                          ( SELECT FROM mainapp_productimage img WHERE img.img = '{file}') 
                                                      THEN 
                                                          INSERT INTO mainapp_productimage(img, product_id) VALUES(%s, %s);
                                                      END IF;
                                                  END
                                                  $$;
                                                      """
                    c.execute(data, (file, id[0]))
                    conn.commit()
    return conn.commit()


def product_filling(root):
    for i in root.findall('./shop/offers/offer'):
        title = i.find('name').text
        supplier_product_url = i.find('url').text
        slug = slugify(title)
        vendorCode = i.find('vendorCode').text
        price = i.find('price').text
        description = i.find('description').text
        category_id = i.find('categoryId').text
        c = conn.cursor()
        dataa = (f"""       DO $$
                               BEGIN
                                   IF NOT EXISTS
                                       ( SELECT FROM mainapp_product product WHERE product.product_code = {vendorCode}) 
                                   THEN 
                                       INSERT INTO mainapp_product(title, slug, product_code, price, description, category_id,supplier_product_url,ordered,popular) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);
                                   END IF;
                               END
                               $$;
                                   """)
        try:
            c.execute(dataa, (title, slug, vendorCode, price, description, category_id, supplier_product_url, '0', '1'))
            conn.commit()
        except psycopg2.errors.lookup("23503") as e:
            print(f' {e} - {title}')
            conn.rollback()
        except psycopg2.errors.lookup('23505') as e:
            print(f' {e} - {title}')
            conn.rollback()
    return conn.commit()


def feel_spec_category(root):
    data = """INSERT INTO specs_categoryfeature(feature_name, feature_filter_name,category_id) VALUES(%s,%s,%s);"""
    for i in root.findall('./shop/offers/offer'):
        category_id = i.find('categoryId').text
        for a in i.findall('param[@name]'):
            feature_name = a.attrib['name'].strip()
            data = f"""
                        DO $$
                        BEGIN
                                INSERT INTO specs_categoryfeature(feature_name, feature_filter_name,category_id) VALUES(%s,%s,%s) ;
                        EXCEPTION
                            WHEN UNIQUE_VIOLATION THEN
                                RAISE NOTICE 'duplicate row';
                        END
                        $$;
                            """
            try:
                c = conn.cursor()
                c.execute(data, (feature_name, slugify(feature_name), category_id))
                conn.commit()
            except psycopg2.errors.lookup("23503") as e:
                conn.rollback()
                print(f' {e}')
            except psycopg2.errors.lookup("23503") as e:
                conn.rollback()
                print(f'{e}')


def feel_spec_product(root):
    c = conn.cursor()
    select_specs_categoryfeature = """SELECT id  FROM specs_categoryfeature WHERE feature_name=(%s) """
    select_product_id = """SELECT id from mainapp_product mp WHERE mp.product_code=(%s)"""
    for i in root.findall('./shop/offers/offer'):
        product_code = i.find('vendorCode').text
        product_ids = c.execute(select_product_id, (product_code,))
        pr = c.fetchall()
        for product_id in pr:
            for a in i.findall('param[@name]'):
                feature_name = a.attrib['name'].strip()
                value = a.text
                c.execute(select_specs_categoryfeature, (feature_name,))
                records = c.fetchall()
                for r in records:
                    feature_id = r[0]
                    try:
                        # data = """INSERT INTO specs_productfeatures(value, feature_id, product_id) VALUES(%s,%s,%s)"""
                        data = f"""
                                           DO $$  
                                           BEGIN
                                               IF NOT EXISTS
                                                   ( SELECT FROM specs_productfeatures WHERE feature_id = {feature_id} AND product_id = {product_id[0]})
                                               THEN 
                                                   INSERT INTO specs_productfeatures(value, feature_id, product_id) VALUES(%s,%s,%s);
                                               END IF;
                                           END
                                           $$;
                                               """
                        c = conn.cursor()
                        c.execute(data, (value, feature_id, product_id[0]))
                        conn.commit()
                    except sqlite3.IntegrityError as error:
                        print(f'ERROR - {error}')


def combin_spec(root):
    select = """SELECT id, product_id  FROM specs_productfeatures"""
    data = """INSERT INTO mainapp_product_features(product_id, productfeatures_id) VALUES (%s,%s)"""
    c = conn.cursor()
    c.execute(select)
    records = c.fetchall()
    for r in records:
        productfeatures_id = r[0]
        product_id = r[1]
        # print(f'{product_id}-{productfeatures_id}')
        try:
            data = f"""
                              DO $$  
                              BEGIN
                                  IF NOT EXISTS
                                      ( SELECT FROM mainapp_product_features WHERE productfeatures_id = {productfeatures_id}) 
                                  THEN 
                                      INSERT INTO mainapp_product_features(product_id, productfeatures_id) VALUES (%s,%s);
                                  END IF;
                              END
                              $$;
                                  """
            c = conn.cursor()
            c.execute(data, (product_id, productfeatures_id))
            conn.commit()
        except sqlite3.IntegrityError as error:
            print(f'ERROR = {error}')

def main(root):
    start = time.time()

    start1 = time.time()
    fell_top_category(root)
    end1 = time.time() - start1

    start2 = time.time()
    fell_category(root)
    end2 = time.time() - start2

    start3 = time.time()
    product_filling(root)
    end3 = time.time() - start3

    # start4 = time.time()
    # filling_product_img_table(root)
    # end4 = time.time() - start4

    start5 = time.time()
    feel_spec_category(root)
    end5 = time.time() - start5

    start6 = time.time()
    feel_spec_product(root)
    end6 = time.time() - start6

    start7 = time.time()
    combin_spec(root)
    end7 = time.time() - start7

    # end = time.time() - start

    # print(f'{end1} - fell_top_category')
    # print(f'{end2} - fell_category')
    # print(f'{end3} - product_filling')
    # print(f'{end4} - filling_product_img_table')
    # print(f'{end5} - feel_spec_category')
    # print(f'{end6} - feel_spec_product')
    # print(f'{end7} - combin_spec')
    # print(f'В загальному {end} або {end / 60} хв.')

main(root)
