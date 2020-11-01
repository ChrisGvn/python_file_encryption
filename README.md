<h2>Encrypting/Decrypting config files with Python</h2>

<h3>The need for encryption</h3>
<p style="text-align:justify;">After some labbing on GNS3, automating virtual networking equipment with Netmiko and tidying up my configuration files, I came up with one question at the end of a day: "Is keeping my configurations as plain text files a good idea?". It doesn't sound like one, especially on a production enviroment.</p>

<h3>Notes on using the Python Cryptography package</h3>
<p><a href="https://cryptography.io/en/latest/">Cryptography</a> provided an easy and direct solution to my issue, however I needed to divert from the tutorials to achieve what I needed.</p>

#### i) Custom password instead of a Fernet generated key
I absolutely did not want to use (or having to store) a file containing my 32-byte encryption key. What if I accidentaly delete it, or worse, what if it gets in the wrong hands? I needed a user-generated key.

First thing to note is how exactly is a Fernet key generated:

```python
def generate_key(cls):
        return base64.urlsafe_b64encode(os.urandom(32))
```
There it is. A random 32-byte number, encoded in Base64. But remember, we need a password we can remember, not a random set of letters, symbols and numbers.
And how can a user-given passphrase be turned into a 32-byte, Base64 key? The PBKDF2HMAC function helps us with that.


Initializing. Notice the `length` value size.
```python
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), 
                length=32, 
                salt=userinput, 
                iterations=100000)
```

After that, we feed the user input into the function and encode the result to Base64 format.
```python
pre_key = kdf.derive(userinput) 
key = base64.urlsafe_b64encode(pre_key) 

#OR

key = base64.urlsafe_b64encode(kdf.derive(userinput)) 
```
And that is it. We are ready to use our user generated key with Fernet: `f = Fernet(key)`


#### ii) The Salt

Because I need the encryprion to be reversible and I don't intend to store a key file, generating a salt randomly with a line 
like `salt = os.urandom(16)` is not wise. 
This is why back in the PBKDF2HMAC init, I fed the user's input to the salt variable: `salt=userinput`. 

Of course, this is not a good practice and is being done for the sake of experimenting in a home set lab. Maybe a good idea would be to ask the user for a second password.
