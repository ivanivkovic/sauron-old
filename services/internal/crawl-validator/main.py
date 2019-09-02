import string
import random
import http.client
import socket
import mysql.connector
import re
import logging


# Core function, sends request and if response is good then it gets flagged as valid domain
def ping(input):
    try:
        logger.debug(input)
        conn = http.client.HTTPConnection(input)
        conn.request('GET', '/')
        result = conn.getresponse()
        return result.status
    except ConnectionResetError:
        logger.error(input + ' ConnectionResetError catched')
        return None
    except TimeoutError:
        logger.error(input + ' TimeoutError catched')
        return None
    except ConnectionRefusedError:
        logger.error(input + 'ConnectionRefusedError catched')
        return None
    except socket.gaierror:
        logger.debug('socket.gaierror catched')
        return None

# Function for checking random name generator, it will not allow generator to break the domain name rules with dash
def dashChecker(name):
    if name.startswith('-') or name.endswith('-'):
        return False
    else: 
        return True

# Generator function, it has pool of characters that are randomly chosen then sent to output as a string
def generator(int):
    string_pool = string.ascii_lowercase + string.digits + "-"
    input = [random.choice(string_pool) for _ in range(int)]
    input = ''.join(input)
    
    if dashChecker(input):
        return(input)
    else:
        input = [random.choice(string_pool) for _ in range(int)]
        input = ''.join(input)
        return(input)
    

# Function for inserting data into DB currently uses placeholder DB connection
def insertData(input):
    dbConnDomain=mysql.connector.connect(         
        host="localhost",
        user="tester",
        passwd="tester123",
        database="crawline"  
        )
    dbCursorDomain = dbConnDomain.cursor()
    command = "INSERT INTO valid_domains (name) VALUES (%s)"
    try:
        dbCursorDomain.execute(command, (input,))
        dbConnDomain.commit()
    except:
        logger.debug(dbCursorDomain._last_executed)
        raise

    

###    MAIN FUNCTION    ###

#Adding base logging functionality

logger = logging.getLogger('crawl-Validator')
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s  - %(message)s')

console.setFormatter(formatter)
logger.addHandler(console)

# TLD Database connection definition
dbConnTld=mysql.connector.connect(
        host="localhost",
        user="tester",
        passwd="tester123",
        database="crawline"
        )
dbCursorTld = dbConnTld.cursor()


while True:
    dbCursorTld.execute("SELECT name FROM tld")
    for x in dbCursorTld:
        i = 3
        tld = str(x)
        tld = re.sub('[^a-zA-Z]+', '', tld)
        while i < 24:
            string_pool = string.ascii_lowercase + string.digits + "-"
            string_range = [3, 3]

# Converts an integer number to a base x system number.
# Optional parameter: String defines replacement for the base x number (for our purpose).
# Optional parameter: Order - allows us to toggle digit / strign ordering.
            def intToBaseInfString(num, base, length, string='', order = 0):
                digits = []
                
                while num:
                    append = string[int(num % base)]
                    print(int(num % base))
                    digits.append( append )
                    num //= base

                while( len(digits) < length ):
                    append = string[0]
                    digits.append( append )

        # 1 means reverse order
                    if order == 1:
                        return digits[::-1]

                return digits

            string_pool_len = len(string_pool)
# Iterating possible domain name lengths
            for max_len in range( string_range[0], string_range[1] + 1 ):

                domain = [string_pool[0]] * max_len

            iteration = 0

    # Iterating from 0 to (string pool length times maximum domain length) with a single iteration variable.
    # This allows us to track our progress correctly, without defining any additional variables, loops or conditionals.
            while (iteration < string_pool_len ** max_len):

                input = intToBaseInfString(iteration, string_pool_len, max_len, string_pool, 0)
                iteration += 1
                
                input = ''.join(input) + '.' + tld
                if ping(input) is not None:
                    insertData(input)
                    logger.info(input + ' is valid')
                    i = i + 1
            i = 0

dbConnTld.close()
