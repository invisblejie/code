import io

output = io.StringIO()
# ignore the index
df_a.to_csv(output, sep='\t', index=False, header=False)
output.getvalue()
# jump to start of stream
output.seek(0)

connection = engine.raw_connection()  # engine 是 from sqlalchemy import create_engine
cursor = connection.cursor()
# null value become ''
cursor.copy_from(output, table_name, null='')
connection.commit()
cursor.close()

"""本来50万条数据，使用pd.to_sql方法，设置chunksize=2000，跑了5个小时。
而上面这个方法，插40万条数据，只需1分钟。
方法来自国外大牛，搬运至此，造福大家。
其实原理是使用了pg内置的copy_from方法，SUPER FAST"""