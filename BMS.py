from tabulate import tabulate
import mysql.connector
con=mysql.connector.connect(host='localhost',
                           username='root',
                           password='A@nn#5u')
cur=con.cursor()
cur.execute("create database if not exists ALLINDIABANK")
print("Database created successfully..")
cur.execute("use ALLINDIABANK")
cur.execute("create table if not exists ACCOUNT_REGISTRY(accno int primary key not null,name char(15) not null,username varchar(10) not null,acctype varchar(10) not null,balance int,age int,kyc varchar(20))")
print("Table created successfully..")
while True:
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('Press 1 for Registering a new bank account ')
    print('Press 2 for Displaying all the Accounts Details')
    print("Press 3 Display an Account")
    print("Press 4 Delete Accounts details")
    print("Press 5 Delete an Account ")
    print("Press 6 Modify an Account")
    print("Press 7 Deposit money")
    print("Press 8 Withdraw money")
    print("Press 9 for updating or adding KYC details")
    print("Press 0 Exit")
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    choice=int(input("Option :- "))
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    if choice==1:
        try:
            print('Fill these details to register your account')
            accno=int(input("enter  account no:-"))
            name=input("Enter  name :- ")
            username=input('Enter  username :-')
            acctype=input('Enter  account type :- ')
            balance=int(input('Enter  balance :- '))
            age=int(input('Enter  age :- '))
            kyc='not done'
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            value=(accno,name,username,acctype,balance,age,kyc)
            query="insert into ACCOUNT_REGISTRY values(%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query,value)
            con.commit()
            print("Record added successfully")
        except:
            print("some error in adding")
    elif choice==2:
        try:
            query="select * from ACCOUNT_REGISTRY "
            cur.execute(query)
            detail=cur.fetchall()
            print(tabulate(detail,tablefmt="psql"))
        except:
            print("Error in Displaying details")

        if detail==[]:
            print("NO RECORD EXIST")
        else:
            print("ALL ACCOUNT DETAILS")

    elif choice==3:
        try:
            no=input("Enter Account Number to Display")
            query="select * from ACCOUNT_REGISTRY where accno="+no
            cur.execute(query)
            myrecord=cur.fetchone()
            print("Record of Account number :"+no)
            print(myrecord)
            c=cur.rowcount
            if c==-1:
                print("Account not found ")
        except:
            print("Error in Displaying account details")

    elif choice==4:
        try:
            ch=input("Do you want to delete All Records (Y/N)")
            if ch=='Y'or'y':
                query="DELETE FROM ACCOUNT_REGISTRY"
                cur.execute(query)
                con.commit()
                print(" All Records Deleted")
        except:
            print("Error in Deleting Records")

    elif choice==5:
        try:
            no=input("Enter Account Number to Delete")
            query="delete from ACCOUNT_REGISTRY where accno="+no
            cur.execute(query)
            con.commit()
            c=cur.rowcount
            if c>=0:
                print("account  Deleted ")
        except:
            print("Error in Deleting record")
    elif choice==6:
        try:
            no=input("Enter Account Number to Modify")
            query="select * from ACCOUNT_REGISTRY where accno= "+no
            cur.execute(query)
            myrecord=cur.fetchone()
            c=cur.rowcount
            if c==-1:
                print("Account Number "+no+" does not exist")
            else:
                name=myrecord[1]
                typ=myrecord[3]
                username=myrecord[2]
                bal=myrecord[4]
                ag=myrecord[5]
                print(type(myrecord[5]))

                print("AccNO      : ",myrecord[0])
                print("NAME       : ",myrecord[1])
                print("USERNAME   : ",myrecord[2])
                print("AccType    : ",myrecord[3])
                print("Balance    : ",myrecord[4])
                print("AGE        : ",myrecord[5])

                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                print("ENTER THE NEW VALUE FOR CHANGE OR JUST LEAVE AND PRESS ENTER")
                x=input("Enter new name or leave")
                if len(x)>0:
                    name=x
                y=input("Enter new Account Type or leave ")
                if len(y)>0:
                    typ=y
                z=input("Enter new username or leave")
                if len(z)>0:
                    username=z
                b=input("Enter new age or leave")
                if len(b)>0:
                    ag=int(b)
                query='update ACCOUNT_REGISTRY set name='+"'"+name+"'"+','+'acctype='+"'"+typ+"'"+','+'username='+"'"+username+"'"+','+' age='+str(ag)+' where accno=' +no
                
                cur.execute(query)
                con.commit()
                print("details modified")
        except Exception as e:
            print("error in modifying")
            print(e)
    elif choice==7:
        try:
            no=input("Enter Account Number ")
            query="select * from ACCOUNT_REGISTRY where accno= "+no
            cur.execute(query)
            myrecord=cur.fetchone()
            c=cur.rowcount
            if c==-1:
                print("Account Number "+no+" does not exist")
            else:
                amount=int(input("Enter amount to deposit"))
                bal=amount+int(myrecord[4])
                query='update ACCOUNT_REGISTRY set balance=%s where '+\
                       'accno=%s'
                rec=(bal,no)

                cur.execute(query,rec)
                con.commit()
                print("Amount Deposited in account no",no)
        except:
            print("error in Depositing Amount")
    elif choice==8:
        try:
            no=input("Enter Account Number ")
            query="select * from ACCOUNT_REGISTRY where accno= "+no
            cur.execute(query)
            myrecord=cur.fetchone()
            c=cur.rowcount
            if c==-1:
                print("Account Number "+no+" does not exist")
            else:
                amount=int(input("Enter amount to withdraw"))
                if amount<myrecord[4]:
                    bal=int(myrecord[4])- amount
                    if bal>1000:
                        query='update ACCOUNT_REGISTRY set balance=%s where '+\
                       'accno=%s'
                        rec=(bal,no)
                        cur.execute(query,rec)
                        con.commit()
                        print("Amount Withdrawn")
                    else:
                        print("insufficient balance so cant withdraw ")
                else:
                    print("amount to be withdrawn greater than your balance available")
        except:
            print("error in Withdrawing Amount")

    elif choice==9:
        no=input("Enter Your Account Number")
        query="select * from ACCOUNT_REGISTRY where accno= "+no
        cur.execute(query)
        myrecord=cur.fetchone()
        c=cur.rowcount
        if c==-1:
            print("Account Number "+no+" does not exist")
        else:
            if myrecord[6]=='not done':
                print('For KYC you need to provide details from one of these government id')
                print('Press 1 for Aadhar Card')
                print('Press 2 for Voter Id Card')
                print('Press 3 for Pan Card')
                print('Press 4 for Driving License')
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                cho=int(input("Enter your choice :- "))
                if cho==1:
                    ad=int(input("Aadhar Number :- "))
                    cur.execute('update ACCOUNT_REGISTRY set kyc='+str(ad)+' where '+'accno='+no)
                    con.commit()
                    print("KYC Done")
                elif cho==2:
                    vi=int(input("Voter Id Number :- "))
                    cur.execute('update ACCOUNT_REGISTRY set kyc='+str(vi)+' where ' + 'accno='+no)
                    con.commit()
                    print("KYC Done")
                elif cho==3:
                    pc=int(input("Pan Card Number :- "))
                    cur.execute('update ACCOUNT_REGISTRY set kyc=+'+str(pc)+' where '+'accno='+no)
                    con.commit()
                    print("KYC Done")
                elif cho==4:
                    dl=int(input("Driving License Number :- "))
                    cur.execute('update ACCOUNT_REGISTRY set kyc='+str(dl)+' where '+'accno='+no)
                    con.commit()
                    print("KYC Done")
                else:
                    print('Wrong Choice')
            else:
                print("kyc already done")
    elif choice==0:
        break
    else :
        print("YOU CHOOSE WRONG OPTION")
                    
