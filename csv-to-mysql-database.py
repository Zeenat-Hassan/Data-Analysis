import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123",
  database= "CSV_DB"
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE QA2(QA VARCHAR(255),Processed_Data mediumtext,Category VARCHAR (255),Sub_Category VARCHAR(255))")
dataset = pd.read_csv ('QA2.csv', sep= ',',quotechar='"', encoding='utf8',engine="python",error_bad_lines=False)
df = pd.DataFrame(dataset, columns = ["QA","Processed_Data","Category","Sub_Category"])

#df.drop_duplicates(inplace = True)
#print(df.head(50))
#print(df.info())

for row in df.itertuples():
    sql = "INSERT INTO QA2(QA,Processed_Data,Category,Sub_Category) VALUES (%s,%s,%s,%s)"
    val= (row.QA,row.Processed_Data,row.Category,row.Sub_Category)
    mycursor.execute(sql,val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

