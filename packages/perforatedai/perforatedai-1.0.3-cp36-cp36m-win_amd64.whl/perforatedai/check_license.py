from base64 import b64decode
import rsa
import yaml
import os.path
import getpass
import sys
import datetime
from datetime import datetime as dtm

enteredPassword = ''
enteredEmail = ''

compilingDate = dtm.strptime('2025-1-16', '%Y-%m-%d')
#change back to 30 after the hackathon
expirationDays = 90


def read_license_file(license_file):
    global enteredPassword
    if(enteredPassword == ''):
        p = os.environ.get('PAIPASSWORD')
        if(not p):
            try:
                print('A license file was found in the working directory.  Enter your PAI password to continue')
                p = getpass.getpass(prompt='Password: ')
            except Exception as error:
                print('ERROR', error)
                sys.exit(1)
        enteredPassword = p
    with open(license_file,'r') as f:
        output = yaml.safe_load(f)
        output['password'] = enteredPassword
        return output
    
def read_token():
    global enteredPassword
    global enteredEmail
    if(enteredPassword == ''):
        e = os.environ.get('PAIEMAIL')
        p = os.environ.get('PAITOKEN')
        if(not (e and p)):
            print('No license file found in the working directory, enter your email address and token to continue or visit https://www.perforatedai.com/getstarted to generate a license file')
            print('email:')
            e = input()
            print('token:')
            p = input()
    return e, p

def valid_license(license_file):
    """
    Verify the license key with the email address, password of the user and the
    public RSA key.

    Args:
            license_file (str): path to license file 
            public_key (str): path to the public RSA key.

    Returns:
            bool: True if the license key is valid, otherwise False.
    """
    key = b64decode("LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1JSUJDZ0tDQVFFQXBqV2VvRGhaNzlXZXU2aGt0ampHbVZOZnZaWWdpbFFpYkgvZ3dZUmJwZnl6WmpPV3oyRysKQVpRMDlNTEJqcDBVZEhaWUlIeFowUmFxOGNzbWU0Ly92VnZMNWFSczRYeGtXaExTd1JiUTFEQ2wwRTlhWFJORQpBTEltbUtqNFBGeHN1ZWxrYm5MekdwNVlFS2V4WEx0Ri9vbmhja0FCTlBtRnJYaE45Qy92QzFjYXNOZmJ5U3hqCnF6VTJYYk1Nalg2REl0aEZNbWx6Q1dFRjlLa21yWW9XdmpCMVQ4TEdNcXpGTjB1dVhXenJscWtMTTNjTEJSZGoKeDVqYVpKSXV2bHFNRkdnaXFBVkJEbTBPeTNBUEIwQzQ3SFl2czdtKzdESldsckNUOHJidFA0RUJUQmNmR3c5NgplODlIay9ra2dMNDAzRkdWNjR6S2d1NkJoRXZTS1AzcjF3SURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K")

    publicKey = rsa.PublicKey.load_pkcs1(key)
    
    if os.path.isfile(license_file):
        license = read_license_file(license_file)
        payload = license['email'] + license['licenseDate'] + license['password']
        licenseString = license['license']
        licenseDate = license['licenseDate']
    else:
        payload, licenseString = read_token()
        licenseDate = str(compilingDate).split(' ')[0]
    try:
        rsa.verify(payload.encode(), b64decode(licenseString), publicKey)        
    except Exception as e:
        print('Exception during verification')
        print('Incorrect Password or Token') # I think this is what sends here
        return False
    now = datetime.datetime.now()
    if((now - dtm.strptime(licenseDate, '%Y-%m-%d')).days > expirationDays):
        print('Your Perforated AI license or token is expired, please request a new one.')
        return False
    if((now - dtm.strptime(licenseDate, '%Y-%m-%d')).days > (expirationDays-7)):
        print('\n\nYour Perforated AI license or token will expire in %d days, please request a new one.\n\n' % (expirationDays - (now - dtm.strptime(licenseDate, '%Y-%m-%d')).days))
    return True
    

        

    
    
