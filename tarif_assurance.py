table_tarif = ['refus','rouge','orange','vert','bleu']
def tarif(age,permis,fidelite,acc):
    # initialise l'indice du tarif en fonction de l'age
    if age < 25:
        indice = 1
    else:
        indice = 2
    # on incremente l'indice si plus de 2 ans de permis
    if permis > 2:
        indice += 1
    # on decremente l'indice par le nombre d'accident
    indice -= acc
    # on incremente l'indice (autre que refus) si + 5 ans de fidélité
    if indice > 0:
        if fidelite > 5:
            indice += 1
    else:
        # si indice < = 0, on le passe a 0 pour eviter pb avec liste des couleurs
        indice = 0
    return table_tarif[indice]


def ask_age():
    age = input("Quel âge avez vous?")
    try:
        age = int(age)
        assert age >= 18 
    except ValueError: 
       print("Vous n'avais pas saisi un nombre.")
       return ask_age()
    except AssertionError:
       print("Vous n'êtes pas majeur.")
       return ask_age()
    else:
        return age


def ask_permis():
    age = input("Depuis combien d'année avez vous votre permis?")
    try:
        age = int(age)
    except ValueError: 
       print("Vous n'avais pas saisi un nombre.")
       return ask_permis()
    else:
        return age


def ask_fidelite():
    age = input("Depuis combien d'année avez vous une assurance chez nous?")
    try:
        age = int(age)
    except ValueError: 
       print("Vous n'avais pas saisi un nombre.")
       return ask_fidelite()
    else:
        return age


def ask_accident():
    acc = input("Combien d'accident avez vous provoqué?")
    try:
        acc = int(acc)
    except ValueError: 
       print("Vous n'avais pas saisi un nombre.")
       return ask_accident()
    else:
        return acc


def ihm_tarif():
    print(tarif(ask_age(),ask_permis(),ask_fidelite(),ask_accident()))


