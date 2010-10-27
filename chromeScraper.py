#!/usr/bin/env python
import Image
import sys
import getopt
from pysqlite2 import dbapi2 as sqlite

try:
    from sqlite import encode, decode
except ImportError:
    import base64
    sqlite.encode = base64.encodestring
    sqlite.decode = base64.decodestring
else:
    sqlite.encode = encode
    sqlite.decode = decode


def usage():
    print >>sys.stderr, 'Usage: %s [-u username]' % sys.argv[0]
    sys.exit(1)

def main():

    opts, args = getopt.getopt(sys.argv[1:], 'u:h')
    username = "root"
    for o, a in opts:
        if o == '-u':
            username = a
        else:
            usage()
    
    path = "/home/"+str(username)+"/.config/google-chrome/Default/Thumbnails"
    try:
        con = sqlite.connect(path)
    except sqlite.OperationalError:
        print >>sys.stderr, 'path to Thumbnails db does not exist: %s' % path
        exit(1)
        
        
    cur = con.cursor()
    for i in range(1, 20):
        statement = "select data from thumbnails where url_id = " + str(i)
        try:
            cur.execute(statement)
        except sqlite.OperationalError:
            print >>sys.stderr, 'DB is locked, please close Chrome browser and try again'
            exit(1)   
        result = cur.fetchall()
        name='/tmp/img'+str(i)+'.png'
        f = open(name, 'wb')
        try:
            f.write(result[0][0])
            f.close()
            Image.open(name).show()
        except IndexError:
            f.close()
    con.close()

if __name__ == '__main__':
    main()

