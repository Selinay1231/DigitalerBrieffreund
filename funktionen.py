from datenbank import *

def navi(session=None):
    liste_login = ["Mein Profil", "Sprachniveau", "Chat", "Fortschritt", "Ausloggen"]
    liste_logout = ["Startseite", "Einloggen", "Neu anmelden", "FAQ", "Über Uns"]

    if session == 0:
        return liste_logout

    elif session == 1:
        return liste_login

    else:
        return print("Fehler")

def check_mail_nutzer(logindaten):
    """Liste der E-Mail-Adressen der Studenten"""
    datensatz_mail = datenwerte(db_get_nutzer_email())
    nutzer_mail = logindaten[0]
    """vergleicht jeden Wert der Liste mit der eingegebenen E-Mail-Adresse"""
    for wert in datensatz_mail:
        """Übereinstimmung gefunden; dann Funktionsaufruf zum Passwort prüfen"""
        if wert == nutzer_mail:
            return True
    return False

def check_passwort_nutzer(logindaten):
    """zugehörige Passwort der E-Mail-Adresse des Studenten abrufen"""
    pw_by_mail = db_get_passwort_by_email(logindaten[0])[0][0]
    """zugehöriges Passwort mit dem eingegebenen Passwort des Login-Formular vergleichen"""
    passwort = logindaten[1]
    if pw_by_mail == passwort:
        return True

def datenwerte(inhalt):
    """ersten Wert aus jeder Zeile des Datenbankergebnisses abrufen und als Liste zurückgeben"""
    liste = []
    for wert in inhalt:
        liste.append(wert[0])
    return liste

