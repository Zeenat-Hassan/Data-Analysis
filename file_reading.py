import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123",
  database= "CSV_DB"
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE QA1 (Processed_Data mediumtext,Case_Category VARCHAR(255),Case_Issues VARCHAR (255))")
dataset = pd.read_csv ('nps_customer_1.csv', sep= ',',quotechar='"', encoding='utf8',engine="python",error_bad_lines=False)
df = pd.DataFrame(dataset, columns = ["Processed_Data","Case_Category","Case_Issues"])

#df.drop_duplicates(inplace = True)
#print(df.head(50))
#print(df.info())

for row in df.itertuples():
    sql = "INSERT INTO QA1(Processed_Data,Case_Category,Case_Issues) VALUES (%s,%s,%s)"
    val= (row.Processed_Data,row.Case_Category,row.Case_Issues,)
    mycursor.execute(sql,val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

