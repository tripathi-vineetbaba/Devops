name=input("Enter Name : ")
e_mail=input("Enter E-Mail : ")
with open('/apps/data/container/user.txt','w+') as file:
    file.writelines(name + '\n')
    file.writelines(e_mail)
