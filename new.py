import bcrypt






def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    return hashed_password


def hash_password_check(password,hashed_password):
    return bcrypt.checkpw(password.encode('utf8'),hashed_password)


print(hash_password('salam'))
print(bcrypt.gensalt())