from datenbank import *
def wort_zaehlen(antwort):
    if antwort is None:
        antwort = ""
    return len(antwort.split())

def test_loesungen():
    """"Richtige Antworten für den Multiple-Choice Frageblock definieren"""
    block1_richtige_antworten = {
        "question1": "1",
        "question2": "3",
        "question3": "1",
        "question4": "2",
        "question5": "3",
        "question6": "2"
    }
    return block1_richtige_antworten

def test_auswertung(antworten):
    block1_richtige_antworten = test_loesungen()
    print(block1_richtige_antworten)
    # Zählen der richtigen Antworten für Block 1 und Block 2
    block1_richtig = 0

    # Auswertung für Block 1
    for frage, richtige_antwort in block1_richtige_antworten.items():
        if frage in antworten and antworten[frage] == richtige_antwort:
            block1_richtig += 1
        print(frage, richtige_antwort)
    return block1_richtig

"""#lösungen in variable?
        # antworten des benutzer
        antworten = [request.form.get("block1_question1"), request.form.get("block1_question2"),
                    request.form.get("block2_question1"), request.form.get("block2_question2")]
        print(antworten)
        # auswertung
        block1_richtig, block2_richtig = auswertung.test_auswertung(antworten)
        # bestimmen des sprachlevel
        neues_sprachlevel = None
        if block1_richtig >= 2:
            neues_sprachlevel = 'A1'  # Upgrade zu A1, wenn 2 oder mehr in Block 1 richtig sind
        if block2_richtig >= 2:
            neues_sprachlevel = 'A2'  # Upgrade zu A2, wenn 2 oder mehr in Block 2 richtig sind
        print(neues_sprachlevel)
        if neues_sprachlevel:
            # Sprachlevel in der Datenbank aktualisieren (als Beispiel)
            db_update_nutzer_sprachlevel(session["nutzer_id"], neues_sprachlevel)
        # weiterleitung an profil mit übergabe des sprachlevel und empfohlenen Brieffreund
        return render_template("profil.html", navi=funktionen.navi(session["login_status"]), nutzer_id=session["nutzer_id"],
                               sprachlevel=neues_sprachlevel) """
