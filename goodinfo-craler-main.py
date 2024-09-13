import csv 
import os
import time
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options # 匯入chrome選項的套件 用於控制chrome畫面大小、禁用談窗等等
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import os 
import time

# 爬蟲


def update_data(company_code):
    company_code = str(company_code)
    goodinfo_page = "https://goodinfo.tw/tw/ShowSaleMonChart.asp?STOCK_ID=" + company_code

    driver = webdriver.Chrome()
    driver.get(goodinfo_page)
    time.sleep(4)

    # choose "ALL" data 
    select = Select(driver.find_element(By.ID,'selSaleMonChartPeriod')) 
    select.select_by_value("ALL")

    # that the data appear ; if no using this, the  than we click download , may download just 5  years data
    time.sleep(10) 

    driver.find_element(By.CSS_SELECTOR,'input[value="HTML"]').click() # click download buttom
    time.sleep(4)

    driver.close()

    # open the downloaded html file in the "Downloads" file
    path = r'/home/anderson/Downloads/SaleMonDetail.html'

    file = open(path,encoding='utf-8')
    html = file.read()

    soup = BeautifulSoup(html, 'html.parser') 
    SaleMonTable = soup.find("table")

    d = SaleMonTable.find_all("tr", align="center")

    main_list = []
    for row in d:
        temp = []
        for td in row.find_all("td"):
            temp.append(td.text)
        main_list.append(temp)

    # store the data into dataframe
    df = pd.DataFrame(main_list)

    # delete the file
    os.unlink(path)
    print("Delete File")

    # connect database
    connection = mysql.connector.connect(
        host = 'localhost',
        database = 'example',
        user = 'user',
        password = '920303'
    )

    # database connect test
    if connection.is_connected():
        db_info = connection.get_server_info()

        # show database version
        print(f"database version {db_info}")

        # show current use dataset 
        cur = connection.cursor()
        cur.execute("SELECT DATABASE();")
        record = cur.fetchone()
        print("current use data set: ", record)

    # rename the columns beacse, the dataframe column is "0-17" , we must change the number to the column's name in the website
    new_columns = {
        0: 'month',
        1: 'open_price',
        2: 'close_price',
        3: 'high_price',
        4: 'low_price',
        5: 'price_change_currency',
        6: 'price_change_pct',
        7: 'op_income_monthly_revenue',
        8: 'op_income_monthly_growth_pct',
        9: 'op_income_yearly_growth_pct',
        10: 'op_income_accumulated_revenue',
        11: 'op_income_accumulated_yearly_growth_pct',
        12: 'cons_op_income_monthly_revenue',
        13: 'cons_op_income_monthly_growth_pct',
        14: 'cons_op_income_yearly_growth_pct',
        15: 'cons_op_income_accumulated_revenue',
        16: 'cons_op_income_accumulated_yearly_growth_pct'
    }
    df.rename(columns=new_columns, inplace=True)

    t0 = time.time()
    columns = ','.join([f'{x}' for x in df.columns])
    param_placeholders = ','.join(['%s' for x in range(len(df.columns))])

 


    frist = 1 # use for judje the first data is new data or not
    def insert(c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16):
        try:
            # Assuming 'id' is the primary key in your financial_data table
            check_statement = (
                # "SELECT month FROM financial_data WHERE "
                "SELECT month FROM s"+ company_code +" WHERE "
                "month = %s AND open_price = %s AND close_price = %s AND high_price = %s AND low_price = %s AND "
                "price_change_currency = %s AND price_change_pct = %s AND op_income_monthly_revenue = %s AND "
                "op_income_monthly_growth_pct = %s AND op_income_yearly_growth_pct = %s AND "
                "op_income_accumulated_revenue = %s AND op_income_accumulated_yearly_growth_pct = %s AND "
                "cons_op_income_monthly_revenue = %s AND cons_op_income_monthly_growth_pct = %s AND "
                "cons_op_income_yearly_growth_pct = %s AND cons_op_income_accumulated_revenue = %s AND "
                "cons_op_income_accumulated_yearly_growth_pct = %s"
            )
            check_data = (c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16)
            
            cur.execute(check_statement, check_data)
            result = cur.fetchone()

            if not result:
                # Data does not exist, proceed with insertion
                # insertStatement = f"INSERT INTO financial_data ({columns}) VALUES ({param_placeholders})"
                insertStatement = f"INSERT INTO s{company_code} ({columns}) VALUES ({param_placeholders})"
                data = (c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16)
                cur.execute(insertStatement, data)
                connection.commit()
                print(time.time()-t0)
                print("Successfully added entry to database")

            else:
                print("Data already exists in the database, skipping insertion")
                return 1 # means that the hole dataframe data is already in databases

        except Error as e:
            print(f"Error adding entry to database: {e}")

    
    col_m = df.columns.to_list()
    for i in range(len(df)):
        if(frist==1):
            a = insert(df[col_m[0]][i], df[col_m[1]][i], df[col_m[2]][i], df[col_m[3]][i], df[col_m[4]][i], df[col_m[5]][i], df[col_m[6]][i], df[col_m[7]][i],df[col_m[8]][i],df[col_m[9]][i],df[col_m[10]][i],df[col_m[11]][i],df[col_m[12]][i],df[col_m[13]][i],df[col_m[14]][i],df[col_m[15]][i],df[col_m[16]][i])
            if(a==1):
                print("data is already add no updata")
                break



if __name__ == '__main__':
    # update_data(2454)
    # time.sleep(2)
    update_data(1234)