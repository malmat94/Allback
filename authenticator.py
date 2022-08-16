import os

def authentic(user):

    admins = ["mateusz.malicki", "agata.chojnicka"]

    if user in admins:
        access = True

    else:
        access = False

    return access

# For testing
# user = os.getlogin()
# authentic(user)
