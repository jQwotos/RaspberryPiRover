import datetime, hashlib

def make_hash():
    date = datetime.datetime.now()
    return hashlib.sha256((str(date.year + date.month + date.day + date.hour + date.minute + magicalNumber) + uberSecretPassword).encode()).hexdigest()

def check_secure(s):
    try:
        command = s.split(":|:")[0]
        sentHash = s.split(":|:")[1]
        myHash = Security.make_hash()

        if sentHash == myHash:
            print("COMMAND:%s" % command)
            return command
        else:
            print('Unauthenticated user trying to send commands!')
    except:
        print("Who sent me a bad packet!")

def make_secure(s):
    return "%s:|:%s" % (s, make_hash)
