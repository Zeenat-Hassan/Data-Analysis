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
# dataset = pd.read_csv ('nps_customer_1.csv', sep= ',',quotechar='"', encoding='utf8',engine="python",error_bad_lines=False)
# df = pd.DataFrame(dataset, columns = ["Processed_Data","Case_Category","Case_Issues"])
#
# #df.drop_duplicates(inplace = True)
# #print(df.head(50))
# #print(df.info())
#
# for row in df.itertuples():
#     sql = "INSERT INTO QA1(Processed_Data,Case_Category,Case_Issues) VALUES (%s,%s,%s)"
#     val= (row.Processed_Data,row.Case_Category,row.Case_Issues,)
#     mycursor.execute(sql,val)
#     mydb.commit()
#
#     print(mycursor.rowcount, "record inserted.")



"""
    Now Writing queries to perform Data Analysis
"""


"""
Query # 1
Query to see the count of the QA1 table
"""

# sql="Select count(*) from QA1"
# mycursor.execute(sql)
# myresult=mycursor.fetchall()
# print(myresult)


"""
Query No # 2
To see how many Case_Category present is Case_Category Column
"""

sql="Select count(Case_Category),Case_Category from QA1 group by Case_Category"
mycursor.execute(sql)
myresult=mycursor.fetchall()
print(myresult)

"""
Query # 3
to see which 2 entries are missing or null in Case_Category
"""
# sql="Select Case_Category from QA1 where Case_Category not in ('Account','Payments','Merchants')"
# mycursor.execute(sql)
# myresult=mycursor.fetchall()
# print(myresult)

"""
other way
"""
# sql="Select Case_Category from QA1 where Case_Category= \"null\""
# mycursor.execute(sql)
# myresult=mycursor.fetchall()
# print(myresult)


"""
To see how many Case_Issues present is Case_Issues Column
"""

# sql="Select count(Case_Issues),Case_Issues from QA1 group by Case_Issues"
# mycursor.execute(sql)
# myresult=mycursor.fetchall()
# print(myresult)


"""
Query to  see that in "Account" Case Category has how many Case_Issues 
"""
# sql="Select count(Case_Issues),Case_Issues from QA1 where Case_Category=\"Account\"  group by Case_Issues"
# mycursor.execute(sql)
# myresult=mycursor.fetchall()
# print(myresult)

"""
Query to see that in   "Merchants" Case Category has how many Case_Issues 
"""
# sql="Select count(Case_Issues),Case_Issues from QA1 where Case_Category=\"Merchants\"  group by Case_Issues"
# mycursor.execute(sql)
# myresult=mycursor.fetchall()
# print(myresult)

"""
Query to see that in   "Payments" Case Category has how many Case_Issues 
"""
# sql="Select count(Case_Issues),Case_Issues from QA1 where Case_Category=\"Payments\"  group by Case_Issues"
# mycursor.execute(sql)
# myresult=mycursor.fetchall()
# print(myresult)


"""
Query No # 2
To see how many Case_Category present is Case_Category Column in percentage
"""

# sql="Select (count(Case_Category)*100/(Select count(*) from QA1)),Case_Category from QA1 group by Case_Category"
# mycursor.execute(sql)
# myresult=mycursor.fetchall()
# print(myresult)