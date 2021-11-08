import mysql.connector
import datetime
from os import * 
# Connecting from the server
conn = mysql.connector.connect(user = 'Shilpa',passwd = "Shilpa@2026",database = 'WholeSale',host = 'localhost',auth_plugin='mysql_native_password')

#conn = mysql.connector.connect(user = 'Shilpa',passwd = "Shilpa@2026",host = 'localhost',auth_plugin='mysql_native_password')
co = conn.cursor()
#co.execute("CREATE DATABASE WholeSale")

"""

co.execute('''create table logins(
	username varchar(15) not null ,
	passwrd varchar(8) not null,
	desig varchar(10) not null,
	primary key (username,passwrd,desig)
);''')
co.execute("create table Delivery_partner(did int(4) not null auto_increment, dname varchar(32) not null, primary key (did));")
co.execute('''create table manufacturer (
    mfid int(4) not null auto_increment,
    mname varchar(32) not null,
    mphone bigint(10) not null,
    primary key (mfid,mname)
);''')


co.execute('''create table category(
    catid int(4) not null auto_increment,
    catname varchar(15) not null,
    primary key (catid)
);''')
co.execute('''create table products (
    pid int(4) not null,
    pname varchar(32) not null,
    size varchar(3) not null,
    unit_price float not null,
    tot_qty int not null,
    mfid int(4) not null,
    catid int(4) not null,
    primary key (pid,pname,size,unit_price),
    foreign key (mfid) references manufacturer(mfid) on delete cascade,
    foreign key (catid) references category(catid) on delete cascade
);''')
co.execute('''create table customer (
    cid int(4) not null auto_increment,
    cname varchar (32) not null,
    cphone bigint(10) not null,
    cmail varchar(32) not null,
    primary key (cid,cname)
);
''')
co.execute('''create table address (
    id int (4) not null,
    name varchar(32) not null,
    building_no int ,
    street_no int not null,
    street_name varchar(32) not null,
    city varchar(32) not null,
    district varchar(32) not null,
    state varchar(15) not null,
    country varchar(20) not null,
    pin int(6) not null,
    primary key (id,name,building_no),
    foreign key (id,name) references customer (cid,cname) on delete cascade
);
''')


co.execute('''create table orders (
    oid int(4) not null,
    odate date not null,
    cid int(4) not null,
    pid int(4) not null,
    pname varchar(32) not null,
    discount float(3,2) default 0.00,
    size varchar(3) not null,
    unit_price float not null,
    p_qty int not null,
    primary key (oid,odate,pid,size),
    foreign key (cid) references customer(cid) on delete cascade,
    foreign key (pid,pname,size,unit_price) references products (pid,pname,size,unit_price) on delete cascade
);''')
co.execute('''create table payment (
    id int(4) not null auto_increment,
    pay_date  date not null,
    cid int(4) not null,
    oid int(4) not null,
    tot_amt float default 0.00,
    mode varchar(15) not null,
    primary key(id,pay_date,oid),
    foreign key (cid) references customer(cid) on delete cascade,
    foreign key (oid) references orders(oid) on delete cascade
);''')


co.execute('''create table shipping (
    trackid int (5) not null,
    shipdate date not null,
    delivdate date null,
    did int(4) not null,
    oid int(4) not null,
    primary key (trackid),
    foreign key (did) references Delivery_partner(did) on delete cascade,
    foreign key (oid) references orders(oid) on delete cascade
);''')
co.execute("drop trigger if exists check_avail;")
co.execute("drop trigger if exists qty_change;")


delimiter //
create trigger check_avail
before insert 
on orders for each row 
begin 
declare qty int;
declare err varchar(255);
set err = ('Not enough stock !');
select tot_qty into qty from products where pid = products.pid and size = products.size limit 1;
if new.p_qty > qty then 
signal sqlstate '45000'
set message_text = err;
end if;
end//

delimiter; 


delimiter //
create trigger qty_change 
after insert
on orders for each row 
begin 
	declare qty int;
	select new.p_qty into qty from orders limit 1;
	update products set tot_qty = tot_qty - qty where pid = new.pid and size = new.size and pname = new.pname;
end //
delimiter;
"""
def new_user():
	username = input("Username : ")
	passwrd = input("Password [Max length 8]: ")
	desig = input("Admin/Customer : ")
	sql = "insert into logins (username,passwrd,desig) values (%s,%s,%s)"
	val = (username,passwrd,desig.upper())
	co.execute(sql,val)
	conn.commit()
def admin_log():
	username = input("Username : ")
	passwrd = input("Password [Max length 8]: ")
	desig = "ADMIN"
	sql = "select passwrd from logins where username = %s and desig = %s;"
	val = (username,desig)
	co.execute(sql,val)
	passw = str(co.fetchone()[0])
	if (passw == passwrd):
		print("Successfull login!")
	else : 
		raise Exception("Wrong Password!")

def cust_log():
	username = input("Username : ")
	passwrd = input("Password [Max length 8]: ")
	desig = "CUSTOMER"
	sql = "select passwrd from logins where username = %s and desig = %s;"
	val = (username,desig)
	co.execute(sql,val)
	passw = str(co.fetchone()[0])
	if (passw == passwrd):
		print("Successfull login!")
	else : 
		raise Exception("Wrong Password!")	

def showman():
	sql = "select * from manufacturer;"
	co.execute(sql)
	x = co.fetchall()
	head = ("MANUFACTURER-ID","BRAND-NAME","CONTACT-NO.")
	for y in head :
		print(str(y).ljust(20), end='')
	print()
	for i in x:
		for y in i:
			print(str(y).ljust(20), end='')
		print()
def showdp():
	sql = "select * from Delivery_partner;"
	co.execute(sql)
	x = co.fetchall()
	head = ("DID","DNAME")
	for y in head :
		print(str(y).ljust(20), end='')
	print()
	for i in x:
		for y in i:
			print(str(y).ljust(20), end='')
		print()
def showcat(): 
	sql = "select * from category;"
	co.execute(sql)
	x = co.fetchall()
	head = ("CATEGORY-ID","CATEGORY-NAME")
	for y in head :
		print(str(y).ljust(20), end='')
	print()
	for i in x:
		for y in i:
			print(str(y).ljust(20), end='')
		print()
def showcust():

	sql = "select cid,cname,cphone,cmail,building_no,street_no,street_name, city,district,state,country,pin  FROM customer inner join address on customer.cid = address.id;"
	
	co.execute(sql)
	x = co.fetchall()
	head = ("CID","CUSTOMER-NAME","CUSTOMER-PHONE","CUSTOMER EMAIL","BUILD.NO","ST.NO","ST.NAME","CITY","DIST","STATE","COUNTRY","PIN")
	for y in head :
		print(str(y).ljust(15), end='')
	print()
	for i in x:
		for y in i:
			print(str(y).ljust(15), end='')
		print()
		
def showprod(): 
	sql = "select * from products;"
	co.execute(sql)
	x = co.fetchall()
	head = ("PROD-ID","PROD-NAME","PROD-SIZE","USP","QUANTITY","MANUF-ID","CATEGORY-ID")
	for y in head :
		print(str(y).ljust(20), end='')
	print()
	for i in x:
		for y in i:
			print(str(y).ljust(20), end='')
		print() 
def showord(): 
	sql = "select * from orders;"
	co.execute(sql)
	x = co.fetchall()
	head = ("OID","ODATE","CID","PID","PNAME","DISCOUNT","SIZE","UNIT_PRICE","QUANTITY")
	for y in head :
		print(str(y).ljust(20), end='')
	print()
	for i in x:
		for y in i:
			print(str(y).ljust(20), end='')
		print()
def showpay():
	sql = "select * from payment;"
	co.execute(sql)
	x = co.fetchall()
	head = ("ID","PAY_DATE","CUSTOMER-ID","ORDER-ID","TOTAL-AMNT","MODE")
	for y in head :
		print(str(y).ljust(20), end='')
	print()
	for i in x:
		for y in i:
			print(str(y).ljust(20), end='')
		print()


def showship():
	sql = "select * from shipping;"
	co.execute(sql)
	x = co.fetchall()
	head = ("TRACK-ID","SHIP_DATE","DELIVERED DATE","DELIVERY_PARTNER-ID","ORDER-ID")
	for y in head :
		print(str(y).ljust(20), end='')
	print()
	for i in x:
		for y in i:
			print(str(y).ljust(20), end='')
		print()
		
def ad_menu():
	print('\t\t\t\t\tMENU')
	print("1.Add Manufacturer details ")
	print("2.Add Delivery Partner Details")
	print("3.Add Category Details ")
	print("4.Add Customer Details ")
	print("5.Add Product Details ")
	print("6.Add Payment Details ")
	print("7.Add Shipping Details ")	


def Add_man():
	showman()
	print()
	manname = input("Enter the Brand name : ")
	manphone = input("Enter the contact details of the manufacturer:")
	sql = "insert into manufacturer (mname,mphone) values (%s,%s)"
	val = (manname,manphone)
	try:
		co.execute(sql,val)
		conn.commit()
		print()
		print()
		showman()
		print()
	except Exception as e: 
		print(e)
	
def Add_dp():
	showdp()
	print()
	delname = input("Enter the name of the Company: ")
	sql = "insert into Delivery_partner (dname) values (%s)"
	val = (delname,)
	try:
		co.execute(sql,val)
		conn.commit()
		print()
		print()
		showdp()
		print()
	except Exception as e: 
		print(e)
	
def Add_cat():
	showcat()
	print()
	categname = input("Enter the Category: ") 
	sql = "insert into category (catname) values (%s)"
	val = (categname,)
	try:
		co.execute(sql,val)
		conn.commit()
		print()
		print()
		showcat()
		print()
	except Exception as e: 
		print(e)

def Add_cust():
	showcust()
	print()
	custname = input("Enter the customername ")
	custphone = input("Enter Valid phone number: ")
	custemail = input("Enter a valid email: ")
	sql = "insert into customer (cname,cphone,cmail) values (%s,%s,%s)"
	val = (custname,custphone,custemail)
	co.execute(sql,val)
	conn.commit()
	print("Address Info :")
	sql = "select cid from customer where cname = %s and cphone = %s"
	val = (custname,custphone)
	co.execute(sql,val)
	adid = int(co.fetchone()[0])
	adname = custname 
	adbno = input("Building No : ")
	adstno = input("Street No : ")
	adstna = input("Street Name : ")
	adcity = input("City : ")
	addist = input("District : ")
	adstat = input("State : ")
	adcntr = input("Country : ")
	adpin = input("Pin : ")
	sql = "insert into address (id,name,building_no,street_no,street_name,city,district,state,country,pin) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	val = (adid,adname,adbno,adstno,adstna,adcity,addist,adstat,adcntr,adpin)
	co.execute(sql,val)
	conn.commit()
	print()
	print()
	showcust()
	print()

def Add_prod():
	showprod()
	print()
	showman()
	print()
	showcat()
	print()
	prid = input("Enter the product id : ")
	prname = input("Enter the product name :")
	prsize = input("Enter the size : ")
	prup = input("Enter the unit prize : ")
	prtotq = input("Enter the total quantity : ")
	prmfid = input("Enter the manufacturing id : ")
	prcatid = input("Enter the category id : ")
	
	sql = "insert into products (pid,pname,size,unit_price,tot_qty,mfid,catid) values (%s,%s,%s,%s,%s,%s,%s)"
	val = (prid,prname,prsize,prup,prtotq,prmfid,prcatid)
	try:
		co.execute(sql,val)
		conn.commit()
		print()
		print()
		showprod()
		print()
	except Exception as e: 
		print(e)

def Add_ord():

	showprod()
	print()
	oid = input("Enter the order id : ")
	odate = input("Enter the date in  yyyy-mm-dd format : ")
	cid = input("Enter the customer id : ")
	pid = input("Enter the product id : ")
	pname = input("Enter the product name :")
	size =  input("Enter the size : ")
	p_qty = input("Enter the quantity : ")
	
	sql = "select unit_price from products where pid = %s and size = %s"
	val = (pid,size)
	co.execute(sql,val)
	unit_price = float(co.fetchone()[0])
	tot = float(p_qty) * unit_price
	if(tot >= 5000 and tot < 10000):
		discount = 0.05
	elif(tot >= 10000 and tot < 15000):
		discount = 0.10
	elif(tot >= 15000 and tot < 20000):
		discount = 0.15
	elif(tot >= 20000):
		discount = 0.25
	else: discount = 0.00
	
	  
	sql = "insert into orders (oid,odate,cid,pid,pname,discount,size,unit_price,p_qty) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	val = (oid,odate,cid,pid,pname,discount,size,unit_price,p_qty)
	"""discount = 0
	args = [oid,pid,size,p_qty]
	co.callproc('calc_disc',args)"""
	try:
		co.execute(sql,val)
		conn.commit()
		print()
		print()
		showord()
		print()
	except Exception as e: 
		print(e)
def Add_pay():
	showord()
	print()
	pay_date = input("Enter the date of payment : ")
	cid = input("Enter the customer id : ")
	oid = input("Enter the order id : ")
	mode = input("Enter the mode of payment : ") 
	sql = "select sum(unit_price * p_qty - (unit_price * p_qty * discount)) from orders where oid = %s;"
	val = (oid,)
	co.execute(sql,val)
	amt = float(co.fetchone()[0])
	amt = round(amt,2)
	sql = "insert into payment (pay_date,cid,oid,tot_amt,mode) values (%s,%s,%s,%s,%s)"
	val = (pay_date,cid,oid,amt,mode)
	try:
		co.execute(sql,val)
		conn.commit()
		print()
		print()
		showpay()
		print()
	except Exception as e: 
		print(e)
def Add_ship():
	print("NOT SHIPPED ORDERS :")
	print()
	disp_notshipped()
	print()
	trackid = input("Enter the tracking id : ")
	shipdate = input("Enter the shipping date in yyyy-mm-dd format : ")
	did = input("Enter the delivery id : ")
	oid = input("Enter the order id : ")
	sql = "insert into shipping (trackid,shipdate,did,oid) values (%s,%s,%s,%s)"
	val = (trackid,shipdate,did,oid)
	try:
		co.execute(sql,val)
		conn.commit()
		
	except Exception as e: 
		print(e)
	x = input('Is the delivery done ? Enter [y/n] : ')
	if (x == 'y' or x == 'Y'):
		delivdate = input("Enter the delivery date in yyyy-mm-dd format : ")
		sql = "update shipping set delivdate = %s where trackid = %s"
		val = (delivdate,trackid)
		try :
			co.execute(sql,val)
			conn.commit()
		except Exception as e:
			print(e)
	else : pass
	print()
	print()		
	showship()
	print()
def up_menu():
	print('\t\t\t\t\tMENU')
	print("1.Update Manufacturers Phone Number ")
	print("2.Update Product Quantity")
	print("3.Update Delivery Date ")
	
def up_man():
	showman()
	print()
	mfid = input("Manufacturer ID :")
	mphone = input("New Phone Number : ")
	try :
		sql = "update manufacturer set mphone = %s where mfid = %s"
		val = (mfid,mphone)
		co.execute(sql,val)
		conn.commit()
		print()
		print("Successfully Updated")
		print()
		showman()
		print()
	except Exception as e: 
		print(e) 
		print("Unsuccessful !")
				
	
def up_pq():
	showprod()
	print()
	pid = input("PRODUCT ID: ")
	pname = input("PRODUCT NAME: ")
	size = input("PRODUCT SIZE:")
	pqty = input ("QTY ADDED: ")
	sql = "update products set tot_qty = tot_qty + %s where pid = %s and pname = %s and size = %s"
	val = (pqty,pid,pname,size)
	try:
		co.execute(sql,val)
		conn.commit()
		print()
		print("Successfully Updated")
		print()
		showprod()
		print()
	except Exception as e: 
		print(e) 
		print("Unsuccessful !")
def up_oddate():
	showship()
	print()
	trackid = input("TRACKING ID: ")
	oid = input("ORDER ID : ")
	delivdate = input("DELIVERY DATE:")
	sql = "update shipping set delivdate = %s where trackid = %s and oid = %s"
	val = (delivdate,trackid,oid)
	try:
		co.execute(sql,val)
		conn.commit()
		print()
		print("Successfully Updated")
		print()
		showship()
		print()
	except Exception as e: 
		print(e) 
		print("Unsuccessful !")
	

def disp_menu():
	print('\t\t\t\t\tMENU')
	print("1.Display Order Details using order id")
	print("2.Display All orders by a customer ")
	print("3.Display the Details of not delivered orders")
	print("4.Display list of depleted Products ")
	print("5.Display Shipping  Details")
	print("6.Display Orders that are not shipped")
	print("7.Dispaly details of payment defaulters")
	


def disp_not_deliv():
	sql = "select * from orders where oid in (select oid from shipping where delivdate is null)"
	try: 
		co.execute(sql)
		x = co.fetchall()
		head = ("OID","ODATE","CID","PID","PNAME","DISCOUNT","SIZE","UNIT_PRICE","QUANTITY")
		print()
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 
		
		
def disp_ship():
	trackid = input("Enter the tracking id : ")
	sql = "select * from shipping where trackid = %s"
	val = (trackid,)
	try:
		co.execute(sql,val)
		x = co.fetchall()
		head = ("TRACKID","SHIP-DATE","DELIVERY-DATE","DELIVERY_PARTNER-ID","ORDER-ID")
		print()
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 
		

def disp_o_cust():
	cid = input("Enter the Customer id : ")
	sql = "select * from orders where cid = %s"
	val = (cid,)
	try:
		co.execute(sql,val)
		x = co.fetchall()
		head = ("OID","ODATE","CID","PID","PNAME","DISCOUNT","SIZE","UNIT_PRICE","QUANTITY")
		print()
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 
		
def disp_oid():
	oid = input("Enter the Order id : ")
	sql = "select * from orders where oid = %s"
	val = (oid,)
	try:
		co.execute(sql,val)
		x = co.fetchall()
		head = ("OID","ODATE","CID","PID","PNAME","DISCOUNT","SIZE","UNIT_PRICE","QUANTITY")
		print()
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 
		
def disp_depl():
	sql = "select products.pid,products.pname,products.size,products.unit_price,products.mfid,manufacturer.mname,products.catid from products inner join manufacturer on products.mfid = manufacturer.mfid where tot_qty = 0;"
	try:
		co.execute(sql)
		x = co.fetchall()
		head = ("PRODUCT-ID","NAME","SIZE","USP","MANUF.ID","MANUFACTURER-NAME","CATEGORY-ID")
		print()
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 
		

def disp_pay_def():
	sql = "select distinct(orders.cid),customer.cname , oid from orders inner join customer on orders.cid = customer.cid  where orders.cid not in (select cid from payment);"
	try:
		co.execute(sql)
		x = co.fetchall()
		head = ("CUSTOMER-ID","NAME","ORDER-ID")
		print()
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 
		
def disp_notshipped():
	sql = "select * from orders where oid not in (select oid from shipping);"
	try:
		co.execute(sql)
		x = co.fetchall()
		head = ("OID","ODATE","CID","PID","PNAME","DISCOUNT","SIZE","UNIT_PRICE","QUANTITY")
		print()
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 
			

def del_menu():
	print('\t\t\t\t\tMENU')
	print("1.Delete Brand")
	print("2.Delete Product")
	print("3.Delete Delivery Partner")
	print("4.Delete depleted Products ")

def del_brand():
	showman()
	print()
	mfid = input("Manufacturer ID: ")
	sql = ("delete from manufacturer where mfid = %s")
	val = (mfid,)
	try:
		co.execute(sql,val)
		conn.commit()
		showman()
		print()
	except Exception as e: 
		print(e) 
	
def del_prod():
	showprod()
	print()
	pid = input("Product ID: ")
	sql = ("delete from products where pid = %s")
	val = (pid,)
	try:
		co.execute(sql,val)
		conn.commit()
		showprod()
		print()
	except Exception as e: 
		print(e) 
def del_dp():
	showdp()
	print()
	did = input("Delivery Partner ID: ")
	sql = ("delete from Delivery_partner where did = %s")
	val = (did,)
	try:
		co.execute(sql,val)
		conn.commit()
		showdp()
		print()
	except Exception as e: 
		print(e) 
def del_depp():
	disp_depl()
	print()
	sql = "delete from products where tot_qty = 0;"
	try:
		co.execute(sql)
		conn.commit()
		print("DELETED !!")
	except Exception as e: 
		print(e) 
		
def admin_menu ():
	a = 'y'
	while (a == 'y' or a == 'Y'):
        
		print('\t\t\t\t\tMENU')
		print("1.Add Details")
		print("2.Update Details")
		print("3.Display Details ")
		print("4.Delete Details ")
		
		n = input("Enter the option : ")
		print(n)
		if (n == '1') :
			opt = 'y'
			while (opt == 'y' or opt == 'Y'):
				system('clear')
				ad_menu()
				m = input("Enter the option : ")
				system('clear')
				if(m == '1'):
					Add_man()
				elif (m == '2'):
					Add_dp()
				elif (m == '3'):
					Add_cat()
				elif (m == '4'):
					Add_cust()
				elif (m == '5'):
					Add_prod()
				elif (m == '6'):
					Add_pay()
				elif (m == '7'):
					Add_ship()
				else :
					print("Invalid Option")
				opt = input ("Press 'y' to continue and 'n' to go back to Admin Menu:")
		elif (n == '2'):
			opt = 'y'
			while (opt == 'y' or opt == 'Y'):
				system('clear')
				up_menu()
				m = input("Enter the option : ")
				system('clear')
				if (m == '1'):
					up_man()
				elif (m == '2'):
					up_pq()
				elif (m == '3'):
					up_oddate()
				else :
					print("Invalid Option")
				opt = input ("Press 'y' to continue and 'n' to go back to Admin Menu:")
			
		elif (n == '3'): 
			opt = 'y'
			while (opt == 'y' or opt == 'Y'):
				system('clear')
				disp_menu()
				m = input("Enter the option : ")
				system('clear')
				if(m == '1'):
					disp_oid()
				elif (m == '2'):
					disp_o_cust()
				elif (m == '3'):
					disp_not_deliv()
				elif (m == '4'):
					disp_depl()
				elif (m == '5'):
					disp_ship()
				elif (m == '6'):
					disp_notshipped()
				elif (m == '7'):
					disp_pay_def()
				else :
					print("Invalid Option")
				opt = input ("Press 'y' to continue and 'n' to go back to Admin Menu:")
		elif (n == '4'): 
			opt = 'y'
			while (opt == 'y' or opt == 'Y'):
				system('clear')
				del_menu()
				m = input("Enter the option : ")
				system('clear')
				if(m == '1'):
					del_brand()
				elif (m == '2'):
					del_prod()
				elif (m == '3'):
					del_dp()
				elif (m == '4'):
					del_depp()
				else :
					print("Invalid Option")
				opt = input ("Press 'y' to continue and 'n' to go back to Admin Menu:")
		
		else :	print("Invalid Option !")
		
		a = input("Press 'y' to continue and 'n' to go back to Admin page:")
		if (a == 'n' or a == 'N'):
			return
			
			
def c_ad_menu():
	print('\t\t\t\t\tMENU')
	print("1.Add Customer Details ")
	print("2.Add Order Details ")
	print("3.Add Payment Details ")
	

def c_up_menu():
	print('\t\t\t\t\tMENU')
	print("1.Update Customer Phone Number ")
	print("2.Update Customer Email ")
	print("3.Update Payment Mode ")	


def c_disp_menu():
	print('\t\t\t\t\tMENU')
	print("1.Dispaly Customer information")
	print("2.Display All orders by a customer id ")
	print("3.Display Order Details using order id")
	print("4.Display payment details of an order ")
	print("5.Filter all Products using brand")
	print("6.Filter all  Products using category")
	print("7.Filter all Products using Price Range")


def c_del_menu():
	print('\t\t\t\t\tMENU')
	print("1.Delete Customer")
	print("2.Delete Order")

def c_del_cust():
	showcust()
	print()
	cid = input("Customer ID: ")
	sql = "delete from customer where cid = %s"
	val = (cid,)
	try:
		co.execute(sql,val)
		conn.commit()
		print()
		showcust()
		print()
	except Exception as e: 
		print(e) 
	
def c_del_ord():
	showord()
	print()
	oid = input("Order id : ")
	sql = "SELECT distinct(oid), IF(oid not in (select oid from shipping), 1, 0) FROM orders where oid = %s"
	val = (oid,)
	co.execute(sql,val)
	s = str(co.fetchone()[1])
	if (s == '0'):
		print("Not Possible to Delete")
	else : 
		sql = "delete from orders where oid = %s"
		val = (oid,)
		try:
			co.execute(sql,val)
			conn.commit()
			print()
			showord()
			print()
		except Exception as e: 
			print(e) 
def c_disp_custinfo():
	
	cid = input("Customer ID: ")
	sql = "select cid,cname,cphone,cmail,building_no,street_no,street_name, city,district,state,country,pin  FROM customer inner join address on customer.cid = address.id where cid = %s"
	val = (cid,)
	try:
		co.execute(sql,val)
		x = co.fetchall()
		head = ("CID","CUSTOMER-NAME","CUSTOMER-PHONE","CUSTOMER EMAIL","BUILD.NO","ST.NO","ST.NAME","CITY","DIST","STATE","COUNTRY","PIN")
		for y in head :
			print(str(y).ljust(15), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(15), end='')
			print()
	except Exception as e: 
		print(e) 
			
def c_disp_pd():
	oid = input("Order id : ")
	sql = "select * from payment where oid = %s"
	val = (oid,)
	try:
		co.execute(sql,val)
		x = co.fetchall()
		print()
		head = ("ID","PAYMENT_DATE","CUSTOMER-ID","ORDER-ID","TOTAL-AMOUNT","PAYMENT-MODE")
		print()
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 		
def fil_brand_prod():
	mname = input("Brand Name : ")
	sql = "select pid,pname,size,unit_price, tot_qty,catid, manufacturer.mfid, manufacturer.mname from products inner join manufacturer on products.mfid = manufacturer.mfid where manufacturer.mname = %s"
	val = (mname,)	
	try:
		co.execute(sql,val)
		x = co.fetchall()
		head = ("PRODUCT-ID","NAME","SIZE","USP","QUANTITY","CATEGORY-ID","MANUF.ID","MANUFACTURER-NAME")
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()	
	except Exception as e: 
		print(e) 
			
def fil_cat_prod():	
	catname = input("Category: ")
	sql = "select pid,pname,size,unit_price, tot_qty, category.catid, category.catname from products inner join category on products.catid = category.catid where category.catname = %s"
	val = (catname,)	
	try:
		co.execute(sql,val)
		x = co.fetchall()
		head = ("PRODUCT-ID","NAME","SIZE","USP","QUANTITY","CATEGORY-ID","CATEGORY-NAME")
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 
		
def fil_price_prod():
	maxp = input("Max Price Limit: ")
	minp = input("Min Price Limit: ")
	sql = "select * from products where unit_price between %s and %s"
	val = (minp,maxp)
	try:
		co.execute(sql,val)
		x = co.fetchall()
		head = ("PRODUCT-ID","NAME","SIZE","USP","QUANTITY","MANUF.ID","CATEGORY-ID")
		for y in head :
			print(str(y).ljust(20), end='')
		print()
		for i in x:
			for y in i:
				print(str(y).ljust(20), end='')
			print()
	except Exception as e: 
		print(e) 
def c_up_cp():
	showcust()
	cid = input("Customer ID: ")
	cname = input("Customer Name: ")
	cphone = input("Enter New Phone Number: ")
	sql = "update customer set cphone = %s where cid = %s and cname = %s"
	val = (cphone,cid,cname )
	try:
		co.execute(sql,val)
		conn.commit()
	except Exception as e: 
		print(e) 	
def c_up_email():
	showcust()
	cid = input("Customer ID: ")
	cemail = input("Customer email: ")
	sql = "update customer set cmail = %s where cid = %s"
	val = (cemail,cid)
	try:
		co.execute(sql,val)
		conn.commit()
	except Exception as e: 
		print(e) 

def c_up_paymode():
	showpay()
	iid =  input("Payment id / Customer id: ")
	mode = input("Mode: ")
	sql = "update payment set mode = %s where id = %s or cid = %s"
	val = (mode,iid,iid)
	try:
		co.execute(sql,val)
		conn.commit()
	except Exception as e: 
		print(e) 

				
def cust_menu():
	a = 'y'
	while (a == 'y' or a == 'Y'):
        
		print('\t\t\t\t\tMENU')
		print("1.Add Details")
		print("2.Update Details")
		print("3.Display Details ")
		print("4.Delete Details ")
		
		n = input("Enter the option : ")
		print(n)
		if (n == '1') :
			
			opt = 'y'
			while (opt == 'y' or opt == 'Y'):
				system('clear')
				c_ad_menu()
				m = input("Enter the option : ")
				system('clear')
				if(m == '1'):
					Add_cust()
				elif (m == '2'):
					Add_ord()
				elif (m == '3'):
					Add_pay()
				else :
					print("Invalid Option")
				opt = input ("Press 'y' to continue and 'n' to go back to Admin Menu:")
		elif (n == '2'):
			
			opt = 'y'
			while (opt == 'y' or opt == 'Y'):
				system('clear')
				c_up_menu()
				m = input("Enter the option : ")
				system('clear')
				if (m == '1'):
					c_up_cp()
				elif (m == '2'):
					c_up_email()
				elif (m == '3'):
					c_up_paymode()
				else :
					print("Invalid Option")
				opt = input ("Press 'y' to continue and 'n' to go back to Admin Menu:")
			
		elif (n == '3'): 
			opt = 'y'
			while (opt == 'y' or opt == 'Y'):
				system('clear')
				c_disp_menu()
				m = input("Enter the option : ")
				system('clear')
				if(m == '1'):
					c_disp_custinfo()
				elif (m == '2'):
					disp_o_cust()
				elif (m == '3'):
					disp_oid()
				elif (m == '4'):
					c_disp_pd()
				elif (m == '5'):
					fil_brand_prod()
				elif (m == '6'):
					fil_cat_prod()
				elif (m == '7'):
					fil_price_prod()
				else :
					print("Invalid Option")
				opt = input ("Press 'y' to continue and 'n' to go back to Admin Menu:")
		
		elif (n == '4'): 
			opt = 'y'
			while (opt == 'y' or opt == 'Y'):
				system('clear')
				c_del_menu()
				m = input("Enter the option : ")
				system('clear')
				if(m == '1'):
					c_del_cust()
				elif (m == '2'):
					c_del_ord()
				else :
					print("Invalid Option")
				opt = input ("Press 'y' to continue and 'n' to go back to Admin Menu:")
		else :	print("Invalid Option !")
		
		a = input("Press 'y' to continue and 'n' to go back to Admin page:")
		if (a == 'n' or a == 'N'):
			return

def menu():
	print('\t\t\t\t\tLOGIN OPTIONS:')
	print("1.ADMIN LOGIN:")
	print("2.CUSTOMER LOGIN:")
	print("3.NEW USER REGISTRATION")
	print("4.EXIT")

def main():
    a = 'y'
    while (a == 'y' or a == 'Y'):
        menu()
        o = input("Enter the option : ")
        
        if (o == '1'):
        	system('clear')
        	admin_log()
        	system('clear')
        	print("Successfully Logged in!")
        	admin_menu()
        	a = input("Press 'y' to continue and 'n' to Exit:")
        elif(o  == '2'):
        	system('clear')
        	cust_log()
        	system('clear')
        	cust_menu()
        	a = input("Press 'y' to continue and 'n' to Exit:")
        elif (o == '3'):
        	system('clear')        
        	new_user()
        	a = input("Press 'y' to continue and 'n' to Exit :")
        	system('clear')
        elif (o == '4'): exit(0)
        
        else : raise Exception("Invalid Option!")
        
    
    print()
    

if __name__ == "__main__":
    main()

	
