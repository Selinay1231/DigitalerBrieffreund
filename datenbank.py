import psycopg2
import os


host = "localhost"
database = "postgres"
user = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]

def doSQL(sql):
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    try:
        output = cur.fetchall()
    except:
        output = None

    cur.close()
    conn.close()
    return output

def db_tabellen():
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS nutzer CASCADE;'
            "CREATE TABLE nutzer ("
            "vorname varchar NOT NULL,"
            "email varchar PRIMARY KEY NOT NULL,"
            "passwort varchar NOT NULL,"
            "sprachlevel varchar NOT NULL);"
            
            'DROP TABLE IF EXISTS chatbot CASCADE;'
            "CREATE TABLE chatbot ("
            "vorname varchar NOT NULL,"
            "nachname varchar PRIMARY KEY NOT NULL,"
            "alter varchar NOT NULL,"
            "position varchar NOT NULL,"
            "beschreibung varchar NOT NULL);"
            )
    conn.commit()
    cur.close()
    conn.close()


def db_addChatbot(data):
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    """Fügt einen neuen Chatbot hinzu"""
    cur = conn.cursor()

    cur.execute("INSERT INTO public.chatbot ( vorname, nachname, alter, position, beschreibung) "
                "VALUES (%s,%s,%s,%s,%s)",
                (data[0], data[1], data[2], data[3], data[4]))

    conn.commit()

    cur.close()
    conn.close()
    return

def db_addNutzer(data):
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    """Fügt einen neuen Nutzer hinzu"""
    cur = conn.cursor()

    cur.execute("INSERT INTO public.nutzer ( vorname, email, passwort, sprachlevel) "
                "VALUES (%s,%s,%s,%s)",
                (data[0], data[1], data[2], data[3]))

    conn.commit()

    cur.close()
    conn.close()
    return

def db_fill_tabellen():
    db_addNutzer(['Alina', 'bormann@uni.de', 'passwort', 'A1'])
    db_addNutzer(['Lina', 'mann@uni.de', 'passwort', 'B1'])
    db_addChatbot(['Amy', 'Johnson', '14', 'New York, USA', 'Amy lebt mit ihren Eltern und ihrem jüngeren Bruder in New York. nd liebt es, zu singen und Fantasy-Romane zu lesen. Ihr größter Traum ist es, eine bekannte Künstlerin zu werden. Gemeinsam könnt ihr einfache Begrüßungen üben, den Alltag auf Englisch beschreiben und über eure Hobbies sprechen. Stärke dein Selbstvertrauen und erfahre mehr über amerikanische Kultur. Werde ihr Digitaler Brieffreund und habt Spaß beim gemeinsamen Lernen! ' ])
    db_addChatbot(['Bobby', 'Smith', '16', 'London, England', 'Bobby ist dein perfekter digitaler Brieffreund! Er liebt es, über Fußball, Videospiele und das Leben in London zu sprechen. Nutze die Gelegenheit, um deinen Wortschatz rund um Freizeitaktivitäten zu erweitern und einfache Gespräche über alltägliche Themen zu führen. Tauche in Bobbys Welt ein und verbessere spielerisch dein Englisch – er freut sich auf den Austausch mit dir!'])
def db_get_nutzer_email():
    return doSQL('SELECT email FROM public.nutzer;')

def db_get_passwort_by_email(email):
    return doSQL("SELECT passwort FROM public.nutzer WHERE public.nutzer.email='" + email + "';")

def db_get_nutzer_id(wert):
    return doSQL("SELECT email FROM public.nutzer WHERE email='" + wert + "';")

def db_get_nutzer_by_id(wert):
    """Daten eines einzelnen Nutzer, aufgrund der übergebenen E-Mail-Adresse zurückgeben"""
    return doSQL("SELECT * FROM public.nutzer where email='" + wert + "';")

def db_get_all_chatbots():
    return doSQL("SELECT * FROM public.chatbot;")

def db_get_level_by_nutzerid(wert):
    return doSQL("SELECT sprachlevel FROM public.nutzer where email='" + wert + "';")

def db_delete_nutzer(nutzerid):
    return doSQL("DELETE FROM public.nutzer where email='" + nutzerid + "';")


def db_update_nutzer_vorname(name, nutzerid):
    return doSQL("UPDATE public.nutzer SET vorname = '" + name + "' WHERE email = '" + nutzerid + "';")


def db_update_nutzer_email(email, nutzerid):
    return doSQL("UPDATE public.nutzer SET email = '" + email + "' WHERE email = '" + nutzerid + "';")

def db_update_nutzer_passwort(passwort, nutzerid):
    return doSQL("UPDATE public.nutzer SET passwort = '" + passwort + "' WHERE email = '" + nutzerid + "';")
def db_update_nutzer_level(sprachlevel, nutzerid):
      return doSQL("UPDATE public.nutzer SET sprachlevel = '" + sprachlevel + "' WHERE email = '" + nutzerid + "';")


