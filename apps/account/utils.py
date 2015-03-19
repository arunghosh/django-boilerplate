import random
import hashlib


def get_random_token():
   bits = str(random.SystemRandom().getrandbits(512)) 
   return hashlib.sha256(bits.encode("utf-8")).hexdigest()

def create_hash(string):
   return hashlib.sha256(string.encode("utf-8")).hexdigest()
    
