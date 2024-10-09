from flask import Flask, render_template, request, session, jsonify, redirect, url_for

import auswertung
import datenbank
from datenbank import *
import funktionen
import web_app

app = Flask(__name__)
app.secret_key = "geheim!"

print("hallo")

datenbank.db_tabellen()
datenbank.db_fill_tabellen()

@app.route('/')
def hello_world():
    session.clear()
    session["login_status"] = 0
    if not session["login_status"] == 0:
        session["login_status"] = 0
        print(session["login_status"])
    return render_template("index.html", navi=funktionen.navi(session["login_status"]))

@app.route('/regist', methods=['POST', 'GET'])
def regist():
    if request.method == "GET":
        return render_template("regist.html", navi=funktionen.navi(session["login_status"]))

    if request.method == "POST":
        register_daten = [request.form.get("vorname"), request.form.get("email"),
                          request.form.get("passwort"), request.form.get("level")]

        db_addNutzer(register_daten)
        return render_template("login.html", registerdaten=register_daten,
                               navi=funktionen.navi(session["login_status"]))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template("login.html", navi=funktionen.navi(session["login_status"]))

    if request.method == "POST":
        login_daten = [request.form.get("email").lower(), request.form.get("passwort")]
        """Prüft ob eingegebene E-Mail-Adresse mit einer beliebigen Tabelle übereinstimmt"""
        if funktionen.check_mail_nutzer(login_daten):
            if funktionen.check_passwort_nutzer(login_daten):
                session["login_status"] = 1
                session["nutzer_id"] = funktionen.datenwerte(db_get_nutzer_id(login_daten[0]))
                return redirect('/profil')
            else:
                print("Logindaten existieren nicht Registriere dich")
        else:
            return redirect('/profil')
        return redirect('/profil')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == "GET":
        return render_template("logout.html", navi=funktionen.navi(session["login_status"]))

    if request.method == "POST":
        session["login_status"] = 0
        return render_template("index.html", navi=funktionen.navi(session["login_status"]))

@app.route("/profil", methods=['GET', 'POST'])
def profil():
    nutzer = db_get_nutzer_by_id(session["nutzer_id"][0])
    if request.method == "GET":
        nutzer = db_get_nutzer_by_id(session["nutzer_id"][0])
        return render_template("profil.html", nutzer_daten=nutzer, navi=funktionen.navi(session["login_status"]),
                               nutzer_id=session["nutzer_id"])
    if request.method == "POST":
        passwort_bestaetigung = request.form['passwort_bestaetigung']
        passwort_nutzer = db_get_passwort_by_email(session["nutzer_id"][0])
        """Überprüfe, ob das eingegebene Passwort mit dem Passwort des aktuellen Nutzer übereinstimmt"""
        if passwort_nutzer[0][0] == passwort_bestaetigung:
            """aktualisiere Daten des Nutzer"""
            nutzer_daten = [request.form.get("vorname"), request.form.get("email"),
                            request.form.get("passwort")]
            db_update_nutzer_vorname(nutzer_daten[0],session["nutzer_id"][0])
            db_update_nutzer_email(nutzer_daten[1], session["nutzer_id"][0])
            db_update_nutzer_passwort(nutzer_daten[2], session["nutzer_id"][0])
            return redirect('/profil')
        return redirect('/profil')

@app.route("/fragen", methods=['GET'])
def fragen():
    if request.method == "GET":
        return render_template("fragen.html", navi=funktionen.navi(session["login_status"]))

@app.route("/ueber_uns", methods=['GET'])
def ueber_uns():
    if request.method == "GET":
        return render_template("ueber_uns.html", navi=funktionen.navi(session["login_status"]))


@app.route('/sprachniveau', methods=['POST', 'GET'])
def sprache():
    if request.method == "GET":
        return render_template("sprachniveau.html", navi=funktionen.navi(session["login_status"]))

@app.route("/fortschritt", methods=['GET'])
def fortschritt():
    if request.method == "GET":
        return render_template("fortschritt.html", navi=funktionen.navi(session["login_status"]))

@app.route('/leveltest', methods=['GET', 'POST'])
def test():
    if request.method == "GET":
        """ich brauche den Levelstatus des eingeloggten Nutzer"""
        sprachlevel = funktionen.datenwerte(db_get_level_by_nutzerid(session["nutzer_id"][0]))
        return render_template("leveltest.html", navi=funktionen.navi(session["login_status"]),
                               sprachlevel=sprachlevel[0])

    if request.method == "POST":
        frage_block = request.form.get("frage_block")
        if frage_block == "freitextantworten":
            antworten = {
                "block1_question1": request.form.get("block1_question1"),
                "block1_question2": request.form.get("block1_question2"),
                "block1_question3": request.form.get("block1_question3"),
                "block1_question4": request.form.get("block1_question4"),
                "block1_question5": request.form.get("block1_question5"),
                "block2_question1": request.form.get("block2_question1"),
                "block2_question2": request.form.get("block2_question2"),
                "block3_question1": request.form.get("block3_question1"),
                "block3_question2": request.form.get("block3_question2"),
                "block3_question3": request.form.get("block3_question3"),
                "block3_question4": request.form.get("block3_question4"),
                "block3_question5": request.form.get("block3_question5")
            }
            print(antworten)
            """Auswertung der Freitextantworten"""
            # Prüfen, ob alle Antworten in Block 1 mehr als 5 Wörter haben
            block1_freitext_valid = all(auswertung.wort_zaehlen(antworten[a]) > 5 for a in
                                        ["block1_question1", "block1_question2"])

            # Prüfen, ob alle Antworten in Block 2 mehr als 10 Wörter haben
            block2_freitext_valid = all(auswertung.wort_zaehlen(antworten[a]) > 10 for a in
                                        ["block2_question1", "block2_question2"])
            neues_sprachlevel = None
            # Wenn alle Freitextantworten in Block 1 mehr als 5 Wörter haben, Level A2
            """if block1_freitext_valid:
                neues_sprachlevel = 'A2'"""

            # Wenn alle Freitextantworten in Block 2 mehr als 10 Wörter haben, Level A3
            if block2_freitext_valid:
                neues_sprachlevel = 'B1'

            if neues_sprachlevel:
                db_update_nutzer_level(neues_sprachlevel, session["nutzer_id"][0])

        elif frage_block == "auswahl":
            """Auswertung der Multiple-Choice Fragen"""
            aktuelles_sprachlevel = funktionen.datenwerte(db_get_level_by_nutzerid(session["nutzer_id"][0]))
            antwort = {
                "question1": request.form.get("question1"),
                "question2": request.form.get("question2"),
                "question3": request.form.get("question3"),
                "question4": request.form.get("question4"),
                "question5": request.form.get("question5"),
                "question6": request.form.get("question6")
            }
            print("multiple",antwort)

            block1_richtig = auswertung.test_auswertung(antwort)
            neues_sprachlevel = None
            print(block1_richtig)
            if block1_richtig >= 3:
                neues_sprachlevel = 'A2'  # Upgrade zu A1, wenn 2 oder mehr in Block 1 richtig sind
            else:
                neues_sprachlevel = aktuelles_sprachlevel
            print("neues Level",neues_sprachlevel)

            if neues_sprachlevel:
                db_update_nutzer_level(neues_sprachlevel, session["nutzer_id"][0])

        elif frage_block == "lueckentext":
            aktuelles_sprachlevel = funktionen.datenwerte(db_get_level_by_nutzerid(session["nutzer_id"][0]))
            # Antwort aus dem Formular erhalten
            nutzer_antworten = [request.form.get("luecke1"), request.form.get("luecke2"),
                                request.form.get("luecke3"), request.form.get("luecke4"),
                                request.form.get("luecke5"), request.form.get("luecke6"),
                                request.form.get("luecke7"), request.form.get("luecke8"),
                                request.form.get("luecke9"), request.form.get("luecke10")]

            # Richtige Antworten definieren
            richtige_antworten = [
                'walking',  # 1 Lücke
                'b',        # 2 Lücke
                'c',        # 3 Lücke
                'tell',     # 4 Lücke
                'learning', # 5 Lücke
                'b',        # 6 Lücke
                'a',        # 7 Lücke
                'practice', # 8 Lücke
                'c',        # 9 Lücke
                'feel'      # 10 Lücke
            ]

            """Auswertung der Antworten"""
            punkte = 0
            """Vergleich der Nutzerantworten mit den Lösungen"""
            for i in range(len(richtige_antworten)):
                """Groß-/Kleinschreibung und überflüssige Leerzeichen außen vor"""
                nutzer_antwort = nutzer_antworten[i].strip().lower() if nutzer_antworten[i] else ""
                print(nutzer_antwort)
                loesung = richtige_antworten[i].lower()
                print(loesung)
                """ Vergleiche die Antworten und erhöhe den Punktestand, wenn sie übereinstimmen"""
                if nutzer_antwort == loesung:
                    punkte += 1
                    print("Punktezahl aktuell:",punkte)
            neues_sprachlevel = None
            if punkte >= 7:
                neues_sprachlevel = 'B2'
            else:
                neues_sprachlevel = aktuelles_sprachlevel

            if neues_sprachlevel:
                db_update_nutzer_level(neues_sprachlevel, session["nutzer_id"][0])

        return redirect('/profil')


@app.route('/bot', methods=['GET'])
def bot():
    if request.method == "GET":
        return render_template("bot.html", navi=funktionen.navi(session["login_status"]))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        pm = request.json['pm']
        print(f"Eingehende Nachricht: {user_message}")

        # Bot-Logik ausführen
        response = web_app.logic(user_message)
        print(f"Bot-Antwort: {response}")

        # Antworte dem Benutzer
        full_response = f"{response}"

        if any(term in response.lower() for term in
               ["sorry", "provide more", "not found", "does not mention", "does not reference", "no information",
                "not enough information", "unable to provide", "the guidelines do not"]):
            full_response = web_app.logic(pm + ' ' + user_message)

        full_response = full_response.replace("<", "").replace(">", "")
        return jsonify({'message': full_response})
    except Exception as e:
        print(f"Fehler bei der Chat-Verarbeitung: {e}")
        return jsonify({'message': 'Es gab einen Fehler bei der Verarbeitung Ihrer Nachricht.'})

if __name__ == '__main__':
    app.run()
