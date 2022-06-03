from tarif_assurance import tarif


fichier = open("test_tarif_data.txt","r")

tableau = []
for ligne in fichier:
    tableau.append(ligne)

def test_tarif():
    for ligne in tableau:
        ligne = ligne.replace("\n","")
        ref = ligne.split(',')
        num = int(ref[0])
        age = int(ref[1])
        permis = int(ref[2])
        fidelite = int(ref[3])
        acc = int(ref[4])
        result = ref[5]
        assert tarif(age,permis,fidelite,acc) == result

fichier.close()

