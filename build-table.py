import mysql.connector
import pymysql
from mysql.connector import Error
import pandas as pd 
import os 
import time

# connect database
connection = mysql.connector.connect(
    host = 'localhost',
    database = 'example',
    user = 'user',
    password = ''
)

mycursor = connection.cursor()

def table_exits(table_name):
    mycursor.execute("show tables")
    l = [ "".join(x) for x in mycursor]
    if(table_name in l): return 1
    else: return 0


def build_table(company_code):
    company_name = "s"+str(company_code) # table's name rule is ex : s2330

    if(table_exits(company_name)==0): # judje the table exits or not in the database
        s = f"""
        CREATE TABLE {company_name}(
            month VARCHAR(20),
            open_price VARCHAR(20),
            close_price VARCHAR(20),
            high_price VARCHAR(20),
            low_price VARCHAR(20),
            price_change_currency VARCHAR(20),
            price_change_pct VARCHAR(20),
            op_income_monthly_revenue VARCHAR(20),
            op_income_monthly_growth_pct VARCHAR(20),
            op_income_yearly_growth_pct VARCHAR(20),
            op_income_accumulated_revenue VARCHAR(20),
            op_income_accumulated_yearly_growth_pct VARCHAR(20),
            cons_op_income_monthly_revenue VARCHAR(20),
            cons_op_income_monthly_growth_pct VARCHAR(20),
            cons_op_income_yearly_growth_pct VARCHAR(20),
            cons_op_income_accumulated_revenue VARCHAR(20),
            cons_op_income_accumulated_yearly_growth_pct VARCHAR(20)
        );
        """
        mycursor.execute(s)
        print(f"Add new talbe {company_name} successful")
    else:
        print(f"{company_name} is already exits")


if __name__ == '__main__':
    # mycursor.execute("select * from s2330")
    # for x in mycursor:
    #     print(x)

    build_table(1234)    