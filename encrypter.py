import bcrypt

password = input().strip()
password = password.encode("utf-8")
hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashedPassword.decode("utf-8"))
input()
