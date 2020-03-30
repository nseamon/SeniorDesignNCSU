KEY_WORDS = [ "Merck", "Pharama", "pharmaceuticals", "Vaccine", "Merck & Co.", "Drugs"]

MERCK_DRUGS = [ "Antivenin", "Asmanex", "Twisthaler", "BCG", "Vaccine", "Belsomra", "Bridion", 
                "Cancidas", "Celestone Soluspan", "Celestone", "Clarinex", "Cozaar", "Crixivan",
                "Cubicin", "Delstrigo", "Dificid", "Diprolene", "Diulera", "Elocon", "Emend", 
                "Entereg", "Ervebo", "Follistim", "Fosamax", "Ganirelix", "Gardasil", "HYZAAR", 
                "Integrilin", "Intron", "Invanz", "Isentress", "Janumet", "Januvia", "Keytruda", 
                "Lotrisone", "Maxalt", "M-M-R", "MMR", "Nasonex", "Nexplanon", "Noxafil", "NuvaRing",
                "Ontruzant", "Pegintron", "Pifeltro", "Pregnyl", "Prevymis", "Prixmaxin", "Prinivil", 
                "Propecia", "ProQuad", "Proscar", "Proventil", "Rebetol", "Recarbrio", "Recombivax",
                "Remerson", "Remeron", "Renflexis", "RotaTeq", "Segluromet", "Sinemet", "Singulair", 
                "Sivextro", "Steglatro", "Steglujan", "Stromectol","Sylatron", "Temodar", "Trusopt", 
                "VAQTA", "Varivax", "Vytorin", "Zepatier", "Zebraxa", "Zetia", "Zocor", "Zolinza", 
                "Zostavax"
            ]



def filterText(text):
    """
    Returns boolean value for relation to Merck, Merck products or Merck's intrests

    :param: text to filter
    :return: boolean fitler value
    """

    text = text.lower()
    
    for word in KEY_WORDS:
        if word.lower() in text:
            return True
    
    for drug in MERCK_DRUGS:
        if drug.lower() in text:
            return True
    
    return False