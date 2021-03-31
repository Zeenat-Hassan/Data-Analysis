import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123",
  database= "CSV_DB"
)


def find_pattern(Pattern):

 mycursor = mydb.cursor()
 sql = 'Select Processed_Data,id from QA_1 where Processed_Data like \"%{} %\"'.format(Pattern)

 mycursor.execute(sql)
 myresult = mycursor.fetchall()
 for x in myresult:

  txt= x[0]
  idd= x[1]
  get_index_of_substring(Pattern, txt,idd)
    #str.find() is case sensitive matches with exact case letters
    # y=txt.find(Pattern)
    # print(y)





def Call_Records_for_Removing_strings():
 print('Enter your string pattern :')
 Take_Input = input()
#Calling find_pattern function
 Call_function_find_pattern= find_pattern(Take_Input)




def get_index_of_substring(Pattern,string,idd):
    pattern_length = len(Pattern)
    start_index= string.find(Pattern)
    end_index= start_index + pattern_length
#Calling slice_substring function
    slice_substring(start_index,end_index,string,idd)



def slice_substring(start_index,end_index,string,idd):
    mycursor = mydb.cursor()
    txt=string
    ID=idd

#if substring is in the middle
    if(start_index!=0 and end_index!=len(txt) ):
        sttr= txt[:start_index-1]+txt[end_index:]
        sql='UPDATE QA_1 set Processed_Data= \"{}\" where id= {}'.format(sttr,ID)
        mycursor.execute(sql)
        mydb.commit()
#if substring is in the start

    if(start_index==0):
        sttr= txt[end_index:]
        sql = 'UPDATE QA_1 set Processed_Data= \"{}\" where id= {}'.format(sttr, ID)
        mycursor.execute(sql)
        mydb.commit()

#if substring is in the end
    if(end_index==len(txt)):
        sttr= txt[:start_index-1]
        sql = 'UPDATE QA_1 set Processed_Data= \"{}\" where id= {}'.format(sttr, ID)
        mycursor.execute(sql)
        mydb.commit()


Call_Records_for_Removing_strings()






# mycursor = mydb.cursor()
#
# ID=1
# while ID<=1188:
#
#     sql = "UPDATE QA_1 set Original_text=Processed_Data WHERE id={}".format(ID)
#
#     mycursor.execute(sql)
#
#     mydb.commit()
#     ID+= 1
#mycursor = mydb.cursor()
# sql = "Update QA_1" \
#       " set Processed_Data= REPLACE(Original_text,SUBSTRING(Original_text, POSITION(\"---- Device:\" IN Original_text), length(Original_text))," " )" \
#       "where Original_text like \'%---- Device:%\'"
# sql= "Select Processed_Data,Original_text from QA_1 where "
# mycursor.execute(sql)
# myresult=mycursor.fetchall()
# for x in myresult:
#     print(x[0])
#     print(x[1])

