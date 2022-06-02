from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import time
import logging
#import pytest
    
driver = webdriver.Chrome('chromedriver')
#driver = webdriver.Firefox()
#driver = webdriver.Edge(executable_path=r'msedgedriver.exe')
#driver = webdriver.Edge()
driver.implicitly_wait(4) # seconds

mylog = logging

mylog.basicConfig(filename='mylog.txt', encoding='utf-8', level=mylog.INFO, format='%(levelname)s %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

mylog.info("-------------------------------------- \n>>>Debut de test Dolibarr<<<")

# mylog.debug('This is a debug message')
# mylog.info('This is an info message')
# mylog.warning('This is a warning message')
# mylog.error('This is an error message')
# mylog.critical('This is a critical message')


# Login
def login_dolibarr(user,mdp):
    driver.get('https://testerp.springit.online/')
    # driver.set_window_size(1500, 1206)
    driver.maximize_window()
    #Attente chargement ou 5s
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'username')))
    if driver.find_element(By.ID, 'username').is_displayed:
        driver.find_element(By.ID, 'username').send_keys(user)
    driver.find_element(By.ID, 'password').send_keys(mdp, Keys.RETURN)
    # On recupère qui est connecté
    how_logged = driver.find_element(By.CSS_SELECTOR, ".atoploginusername").text
    assert how_logged == user
    mylog.info('Connecté en tant que : ' + how_logged)  # ==>adminPOE

#création du brouillon de facture
def facture_brouillon(tiers,delai_reglement,moyen_paiment,date_fact):
    mylog.info('Création du brouillon:')
    # aller vers facturation puis nouvelle facture
    driver.find_element(By.CSS_SELECTOR, ".billing").click()
    driver.find_element(By.LINK_TEXT, "Nouvelle facture").click()
    # remplissage option du brouillon

    # selection tiers via li
    #driver.find_element(By.ID, "select2-socid-container").click()
    #driver.find_element(By.CSS_SELECTOR, ".select2-search__field").send_keys(Keys.DOWN, Keys.ENTER)
    
    # select avec fonction select du selecteur de tiers caché
    # ----- Attention ca bug sous driver firefox -----
    tselection = Select(driver.find_element(By.ID, "socid"))
    tselection.select_by_visible_text(tiers)

    # selection recpetion
    # rselection = Select(driver.find_element(By.ID, "cond_reglement_id"))
    # rselection.select_by_visible_text(delai_reglement)
    
    driver.find_element(By.ID, "select2-cond_reglement_id-container").click()
    driver.find_element(By.CSS_SELECTOR, ".select2-search__field").send_keys(delai_reglement,Keys.ENTER)


    # selection mode reglement
    rselection = Select(driver.find_element(By.ID, "selectmode_reglement_id"))
    rselection.select_by_visible_text(moyen_paiment)
    
    # selection de la date de facturation
    driver.find_element(By.ID, "re").send_keys(date_fact)

    # validation du setup du brouillon
    driver.find_element(By.NAME, "bouton").click()

    #verification sur le brouillon des champs saisi lors de la création
    mylog.info('Vérification du brouillon : ')
    # verifie condition de reglement
    testE = driver.find_element(By.XPATH,"//table[@class='border tableforfield']/tbody[1]/tr[4]/td[2]").text
    assert testE == delai_reglement
    mylog.info('Condition de reglement : ' + testE)
    # verifie moyen de reglement
    testE = driver.find_element(By.XPATH,"//table[@class='border tableforfield']/tbody[1]/tr[6]/td[2]").text
    assert testE == moyen_paiment
    mylog.info('Moyen de reglement : ' + testE)
    # verification date de facturation
    testE = driver.find_element(By.XPATH,"//table[@class='border tableforfield']/tbody[1]/tr[3]/td[2]").text
    assert testE == date_fact
    mylog.info('Date de facturation : ' + testE)
    # verification du tiers facturé
    testE = driver.find_element(By.CSS_SELECTOR,".refurl").text
    assert testE == tiers
    mylog.info('Tiers facturé : ' + testE)



# fonction avec paramètre utiliser pour créer une ligne dans la facture
def ligne_cmd(num,type,prixHT,quantite,tva,description):
    # choix du type de la ligne
    driver.find_element(By.ID, "select2-select_type-container").click()
    driver.find_element(By.CSS_SELECTOR, "input.select2-search__field").send_keys(type,Keys.RETURN)
    # remplissage texte dans frame
    eframe = driver.find_element(By.CSS_SELECTOR, "iframe.cke_wysiwyg_frame")
    driver.switch_to.frame(eframe)
    driver.find_element(By.XPATH, "/html/body").send_keys(description)
    # # Retour a la frame par default
    driver.switch_to.default_content()
    # remplissage autre champs de la ligne
    driver.find_element(By.ID, "price_ht").send_keys(prixHT)
    qte = driver.find_element(By.ID, "qty")
    qte.clear()
    qte.send_keys(quantite)
    # choix tva
    driver.find_element(By.ID, "tva_tx").send_keys(tva,Keys.ENTER)
    # ajout ligne
    driver.find_element(By.ID, "addline").click()
    # test total HT de la ligne
    totHTligne = driver.find_element(By.XPATH, "//table[@id='tablelines']/tbody[1]/tr["+num+"]//td[@class='linecolht nowrap right']/span")
    # Attention, là on converti a la voléé un web element en string puis en float (c'est pas tres bien mais python il dit oui)
    totHTligne = float(totHTligne.text.replace(",","."))
    # result = (int(quantite)*float(prixHT.replace(",",".")))
    result = (int(quantite)*float(prixHT))
    # verification que le total HT indiqué sur la ligne correspond bien a la quantite * prixHT
    assert totHTligne == result
    mylog.info('Total HT ligne : ' + num + ' = ' + str(totHTligne))
    # on renvoi a l'appelant le total quantit * prixHT de la ligne
    return result

# fonction créant plusieur ligne dans la facture a partir d'une fichier CSV
def ligne_from_csv(nom_fichier):
    #list_ligne vide qui va contenir tt les ligne(string) de notre fichier
    list_ligne = []
    #on ouvre le fichier donné en paramètre (en lecture seule)
    fichier = open(nom_fichier,"r")
    # on parcourt le fichier et mets chaque ligne dans notre list_ligne (liste des lignes)
    for ligne in fichier:
        list_ligne.append(ligne)
    # on initialise les numero de ligne et le totalHT des lignes qu'on va saisir
    num = 0
    totalHT = 0
    #on parcours les ligne de la list et isole chaque paramètre (spearé par ';')
    for ligne in list_ligne:
        num += 1
        #on retire le \n de la ligne
        ligne = ligne.replace("\n","")
        # on decoupe la ligne avec les ';' pour avoir tout les elements dans une liste
        ref = ligne.split(';')
        type = ref[0]
        prixHT = ref[1]
        quantite = ref[2]
        tva = ref[3]
        description = ref[4]
        #on retire le \n de la string issu du changement de ligne dans le fichier -> plus utile vu qu'on retire le \n en amont du split
        # description = description[0:(len(description)-1)]
        # on appel la fonction qui crée une ligne et addition le total HT de la ligne pour avoir le totalHT de tte les lignes
        totalHT += ligne_cmd(str(num),type,prixHT,quantite,tva,description)
    fichier.close()
    mylog.info('Total HT des lignes calculé : ' + str(totalHT))
    #on renvoi a l'appelant le total HT de tte les lignes
    return totalHT
    

# fonction créant la facture (a l'aide de la fonction ligne_from_csv pour créer plusieur ligne a partir d'une fichier)
def facture():
    #appel fonction pr créer une ligne par ligne du list_ligne csv (avec recuperation du totalHT calculé par la fonction)
    totalHT = ligne_from_csv("table_factures.csv")
 

    # on recupère dans totht_fact le total HT de la facture
    totht_fact = driver.find_element(By.CSS_SELECTOR, "tr:nth-of-type(1) > .amountcard.nowrap").text
    # on retire les deux derniere character ' €' + change ',' par '.' de not totht_fact et converti en float
    totht_fact = float(totht_fact[0:(len(totht_fact)-2)].replace(",","."))

    mylog.info('Total HT des lignes affiché : ' + str(totht_fact))
    assert totht_fact == totalHT

    # valide brouillon
    #driver.find_element(By.CSS_SELECTOR, ".butAction:nth-child(1)").click()
    #driver.find_element(By.CSS_SELECTOR, ".ui-button:nth-child(1)").click()
    #assert driver.find_element(By.CSS_SELECTOR, ".minwidth300imp").text == "Test body"

def divers():
    #test du find_elementS qui peut recupéré dans une liste plusieur element avec localisateur identique
    ListeTotHT = driver.find_elements(By.CSS_SELECTOR,".linecolht")
    i = 0
    for element in ListeTotHT:
        i+=1
        print("element ", i , ":", element.text)
    print("nombre d'element avec la classe .linecolht",len(ListeTotHT))
    # print(ListeTotHT[0].text)
    # print(ListeTotHT[1].text)
    # print(ListeTotHT[2].text)
    # print(ListeTotHT[3].text)
    print('Liste des elements avec classe linecolht',ListeTotHT)

# fonction qui supprime le brouillon de la facture avant de terminer le script   
def del_fact():
    driver.find_element(By.CSS_SELECTOR, ".butActionDelete").click()
    driver.find_element(By.CSS_SELECTOR, ".ui-dialog-buttonset .ui-widget:nth-of-type(1)").click()

# fonction qui recherche une facture en paramètre et l'affiche
def found_fact(ref):
    # affiche liste
    driver.find_element(By.LINK_TEXT, "Liste").click()
    # saisi la ref dans le champ de recherche
    driver.find_element(By.XPATH, "//input[@name='search_ref']").send_keys(ref,Keys.RETURN)
    # click sur le lien dans la liste (la ref recherché doit exister)
    driver.find_element(By.LINK_TEXT, ref).click()
    

#main
def test_facturation():
    login_dolibarr('adminPOE','admin')
    facture_brouillon("Jean","30 jours fin de mois","Chèque","15/05/2022")
    facture()
    divers()
    time.sleep(3)
    del_fact()
    found_fact("(PROV1414)")
    time.sleep(3)
    driver.quit()
test_facturation()
