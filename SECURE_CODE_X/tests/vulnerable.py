import os
import pickle

def unsafe_function(user_input):
    # Vulnerability: Command Injection
    os.system("echo " + user_input)
    
    # Vulnerability: Insecure Deserialization
    data = pickle.loads(user_input)
    
    # Vulnerability: Hardcoded Credential
    api_key = "12345-SECRET-KEY"
    
    return data

if __name__ == "__main__":
    unsafe_function("test")
