
import psycopg2
import sys

params = "postgresql://zawar:Zawar123@localhost:5432/pcsir"
con = psycopg2.connect(params)
cur = con.cursor()
senddata = '0300676270401'

try:
	cur.execute("SELECT * FROM \"barcode\" WHERE \"id\"=(%s)",(senddata,))
	while True:
		row = cur.fetchone()

		if row == None:
			break

		print(row[0] +","+row[1] +","+row[2] +","+row[3])

except psycopg2.DatabaseError, e:
	if con:
		con.rollback()

	print 'Error %s' % e    
	sys.exit(1)

finally:   
	if con:
		con.close()