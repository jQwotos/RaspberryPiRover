import datetime, hashlib, secrets

def make_hash():
    date = datetime.datetime.now()
    return hashlib.sha256((str(date.year + date.month + date.day + date.hour + date.minute + secrets.magicalNumber) + secrets.uberSecretPassword).encode()).hexdigest()

def check_secure(s):
    try:
        s = s.split(":|:")
        command = s[0]
        sentHash = s[1]
        myHash = make_hash()
        print('1')

        if sentHash == myHash:
            print("COMMAND:%s" % command)
            return command
        else:
            print('Unauthenticated user trying to send commands!')
    except:
        print("Who sent me a bad packet!")

def make_secure(s):
    return "%s:|:%s" % (s, make_hash())
