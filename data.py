import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="115.147.39.104",

    user="aptadmin",
    passwd="Pe*UyxpBZ_C0VL2c",
    database="airlock",
    port=5061,
)
query = "select *, DATE(last_update) as date, TIME(last_update) as time, HOUR(last_update) as hour, MINUTE(last_update) as minute, SECOND(last_update) as second, MONTH(last_update) AS month, DAY(last_update) as day, YEAR(last_update) as year from failures where last_update > '2023-01-01'"
sql_query = pd.read_sql(
    "select *, DATE(last_update) as date, TIME(last_update) as time, HOUR(last_update) as hour, MINUTE(last_update) as minute, SECOND(last_update) as second, MONTH(last_update) AS month, DAY(last_update) as day, YEAR(last_update) as year from failures where last_update > '2023-01-01'",
    mydb
)
#sql_query = pd.read_sql("select * from failures", mydb)

df = pd.DataFrame(sql_query, columns=['tower_id', 'pm2_5', 'humidity', 'temp', 'voc', 'pressure', 'last_update', 'hour'])

#df = pd.DataFrame(sql_query, columns=['last_update'])

print(df)