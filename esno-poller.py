from pysnmp.hlapi import *
import mysql.connector,datetime,csv


myDBConn = mysql.connector.connect(
host="172.50.50.252",
user="kkp",
password="kkp@infokom",
database="newtecSOAP"
)

tgljamdef = datetime.datetime.now()
tgljam = tgljamdef.replace(microsecond = 0)


with open('single.txt') as inventory:
        oid1='1.3.6.1.4.1.5835.5.2.10300.1.1.5.2.1.7.1'
        oid2='1.3.6.1.4.1.5835.5.2.10300.1.1.5.2.1.13.1'
        invcsv=csv.reader(inventory)
        for row in invcsv:
                try:
                        host = row[0]
                        iterator = getCmd(
                        SnmpEngine(),
                        CommunityData('test-agent','ntcpublic',1),
                            UdpTransportTarget((host, 161), timeout=3.0, retries=2),
                            ContextData(),
                            ObjectType(ObjectIdentity(oid1)),
                            ObjectType(ObjectIdentity(oid2))
                )
                except:
                        continue
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

                if errorIndication:
                        #print(errorIndication)
                        myExeQ = myDBConn.cursor()
                        sql = "INSERT INTO esno_bakti_lab (host, esno_value, modcod_value, date_created) VALUES (%s, %s, %s, %s)"
                        val = (host,0,0,tgljam)
                        myExeQ.execute(sql, val)
                        myDBConn.commit()
                        print host, '= 0'

                elif errorStatus:
                        myExeQ = myDBConn.cursor()
                        sql = "INSERT INTO esno_bakti_lab (host, esno_value, modcod_value, date_created) VALUES (%s, %s, %s, %s)"
                        val = (host,0,0,tgljam)
                        myExeQ.execute(sql, val)
                        myDBConn.commit()
                        #print host, '= 0'
                        # print('%s at %s' % (errorStatus.prettyPrint(),
                                                                # errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

                else:
                        value=[]
                        for name, val in varBinds:
                                value.append(int(val))

                        esnoVal=(value[0])
                        modcodVal=(value[1])
                        myExeQ = myDBConn.cursor()
                        sql = "INSERT INTO esno_bakti_lab (host,esno_value, modcod_value, date_created) VALUES (%s, %s, %s, %s)"
                        val = (host, esnoVal, modcodVal ,tgljam)
                        myExeQ.execute(sql, val)
                        myDBConn.commit()
                        #print host, '=',(value[0]) #Esno value
                        #print (value[1]) #modcod value
