import pandas as pd
import ibm_db_sa
import numpy as np
import datetime
import logging
import gc
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import select, create_engine
from sqlalchemy.types import VARCHAR, String, TIME, Date, Numeric, FLOAT, Integer
from sqlalchemy.dialects.mysql import DOUBLE


def auto_test_insert_table_problem(database_connect, insert_data, insert_table, insert_data_type_map):
    """
        自动检测pandas的dataframe的对象插入数据库时是那列出的问题
        输入的参数database_connnect是一个链接数据库的engine
        输入的参数insert_table是一个pandas的dataframe的对象
        输入的参数insert_data_type_map是一个与要插入表的字段类型与长度相对应的dict（如 {"user_id": BIGINT}
    """
    try:
        database_connect.connect()
    except:
        print('Init connect')
    column_names = list(insert_data.columns.values)
    problem_detect = {}
    for column in column_names:
        test_column = insert_data[[column]]
        test_column_type = str(insert_data[column].dtype)
        if insert_data[column].dtype in ('object', 'string_', 'unicode_'):
            test_column_max_length = test_column[column].str.len().max()
        else:
            test_column_max_length = 0
        test_column_insert_type = insert_data_type_map.get(column)
        if not test_column_insert_type:
            test_column_insert_type = 'None'
        problem_detect[column] = (test_column_type,test_column_max_length,test_column_insert_type, "Don't have any problem, total match.")
        try:
            test_column.to_sql(insert_table, database_connect, dtype=insert_data_type_map, if_exists='append', index=False)
        except TypeError:
            problem_detect[column] = (test_column_type,test_column_max_length,test_column_insert_type,"TypeError")
        except Exception as column_error:
            problem_detect[column] = (test_column_type,test_column_max_length,test_column_insert_type,column_error)
    with open("column_problem.text", "a", encoding="utf-8") as problem_save:
        problem_save.write('Test column is ' + ' '.join(list(insert_data.columns.values)) + '\n\n')
        for detect_column, column_problem in problem_detect.items():
            problem_save.write("The detect column is {}, dtype is {}, max length is {} , insert type is {}. \n".format(detect_column, column_problem[0], column_problem[1], column_problem[2]))
            problem_save.write("The column situation is {} . \n\n".format(column_problem[3]))
        problem_save.write('Finish test insert column all check\n')
    print("Finish detect column, The program exit \n\n\n")

if __name__ == "__main__":
    df1 = pd.DataFrame({'A': [1,2,3,4], 'B': ['B0', 'B1', 'B2', 'B3'], 'C': ['C0', 'C1', 'C2', 'C3'],
                        'D': ['D0', 'D1354', 'D2', 'D3']}, index=[0, 1, 2, 3])
    e = create_engine("db2+ibm_db://db2admin:db2@183.3.139.134:50000/csi", echo=True)
    connect, df1, insert_table, insert_data_type_map = e, df1, "", {}
    gc.collect()
    auto_test_insert_table_problem(connect, df1, insert_table, insert_data_type_map)



