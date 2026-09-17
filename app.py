from flask import Flask, render_template, request
import sqlite3

from datetime import date

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def pocetna():
     upozorenje = []
     danas = date.today()
     poruka = ""
     proizvodi = []
     conn = sqlite3.connect("proizvodi.db")
     cursor = conn.cursor()
     cursor.execute("""
     CREATE TABLE IF NOT EXISTS proizvodi (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     naziv_proizvoda TEXT,
     broj_komada INTEGER,
     rok_trajanja TEXT
     )
     """)
     conn.close()
     
     if request.method == "POST":
          akcija = request.form.get("akcija")

          if akcija == "dodaj":
               naziv_proizvoda = request.form.get("naziv_proizvoda")
               broj_komada = request.form.get("broj_komada")
               rok_trajanja = request.form.get("rok_trajanja")
               conn = sqlite3.connect("proizvodi.db")
               cursor = conn.cursor()
               
               cursor.execute ("""
               SELECT * FROM proizvodi
               WHERE naziv_proizvoda LIKE ?
               """, (naziv_proizvoda,))
               postojeci_proizvod = cursor.fetchall()
               if postojeci_proizvod != []:
                    poruka = "Proizvod vec postoji"
               else:
                    cursor.execute ("""
                    INSERT INTO proizvodi (naziv_proizvoda, broj_komada, rok_trajanja)
                    VALUES(?, ?, ?)
                    """, (naziv_proizvoda, broj_komada, rok_trajanja))
                    poruka = "Proizvod je uspjesno dodat"
               conn.commit()
               conn.close()
               

          if akcija == "prikazi":
               conn = sqlite3.connect("proizvodi.db")
               cursor = conn.cursor()
               cursor.execute("""
               SELECT * FROM proizvodi
               """)
               proizvodi = cursor.fetchall()
               conn.close()
          if akcija == "pretrazi":
               pronadji_proizvod = request.form.get("pronadji_proizvod")
               pretraga = f"%{pronadji_proizvod}%"
               conn = sqlite3.connect("proizvodi.db")
               cursor = conn.cursor()
               cursor.execute("""
               SELECT * FROM proizvodi
               WHERE naziv_proizvoda LIKE ?
               """, (pretraga,))
               proizvodi = cursor.fetchall()
               if proizvodi == []:
                    poruka = "Proizvod nije pronadjen"
               conn.close()

          if akcija == "izmjeni":
               unesite_naziv = request.form.get("unesite_naziv")
               novi_naziv_proizvoda = request.form.get("naziv_proizvoda") 
               broj_komada = request.form.get("broj_komada")
               rok_trajanja = request.form.get("rok_trajanja")

               conn = sqlite3.connect("proizvodi.db")
               cursor = conn.cursor()
               cursor.execute ("""
               UPDATE proizvodi
               SET  naziv_proizvoda = ?,
                    broj_komada = ?,
                    rok_trajanja = ?
                    WHERE naziv_proizvoda = ?
                    """, (novi_naziv_proizvoda, broj_komada, rok_trajanja, unesite_naziv))
               izmjenjeno = cursor.rowcount
               if izmjenjeno == 1:
                    poruka = "Proizvod je uspjesno izmjenjen"
               else:
                    poruka = "Proizvod nije pronadjen"
               conn.commit()
               conn.close()
              

          if akcija == "obrisi":
               id_proizvoda = request.form.get("id_proizvoda")
               conn = sqlite3.connect("proizvodi.db")
               cursor = conn.cursor()
               cursor.execute ("""
               DELETE FROM proizvodi
               WHERE id = ?
               """, (id_proizvoda,))
               obrisano = cursor.rowcount
               if obrisano == 1:
                    poruka = "Proizvod je uspjesno obrisan"
               else:
                    poruka = "Proizvod nije obrisan"
               conn.commit()
               conn.close()
     
          conn = sqlite3.connect("proizvodi.db")
          cursor = conn.cursor()
          cursor.execute ("""
          SELECT * FROM proizvodi
          """)
          proizvodi = cursor.fetchall()
          for proizvod in proizvodi:
               rok = proizvod[3]
               rok_datum = date.fromisoformat(rok)
               preostalo_dana = (rok_datum - danas).days

               if rok_datum < danas:
                    upozorenje.append(f"{proizvod[1]} je istekao rok ")
               elif preostalo_dana <= 7:
                    upozorenje.append(f"{proizvod[1]} istice za {preostalo_dana} dana")
          conn.close()
     return render_template("index.html", poruka=poruka, proizvodi=proizvodi, upozorenje=upozorenje, danas=danas)

if __name__ == "__main__":
     app.run(debug=True)