from pathlib import Path
from time import sleep
from pysnmp.hlapi import *
from sqlite3 import connect as db_connect

db = db_connect(Path("/data/samples.db"))
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS samples(
    id INTEGER PRIMARY KEY,
    ts TEXT,
    dt1 REAL,
    dt2 REAL,
    dt3 REAL,
    dt4 REAL,
    dt5 REAL,
    dt6 REAL,
    dt7 REAL,
    dt8 REAL
);
""")


while True:
    sleep(1)

    iterator = bulkCmd(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget(('192.168.101.250', 161)),
        ContextData(),
        0, 50,
        ObjectType(ObjectIdentity(f'1.3.6.1.2.1.2.2.1.10')),
        maxRows=8
    )
    values = []
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))
                values.append(varBinds[1])

    if len(values) == 8:
        values_str = ",".join(values)
        res = cur.execute(f"""
        INSERT INTO samples (ts, dt1, dt2, dt3, dt4, dt5, dt6, dt7, dt8)
        VALUES (CURRENT_TIMESTAMP, {values_str});
        """)
        db.commit()
