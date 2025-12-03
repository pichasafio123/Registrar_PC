from flask import Flask, render_template, request, redirect, session, g
import sqlite3
import os

APP_DB = "inventario.db"
app = Flask(__name__)
app.secret_key = "super_secret_key_change_this"

# -------------------------
# CONEXIÓN A BASE DE DATOS
# -------------------------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(APP_DB)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db:
        db.close()

# -------------------------
# RUTAS
# -------------------------
@app.route("/")
def home():
    if "usuario" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM computadores")
    pcs = cur.fetchall()

    if session["rol"] == "admin":
        return render_template("index_privado.html", pcs=pcs)
    else:
        return render_template("index_publico.html", pcs=pcs)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        clave = request.form.get("password", "").strip()

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, usuario, contrasena, rol FROM usuarios WHERE usuario = ?", (usuario,))
        row = cur.fetchone()

        if not row:
            return render_template("login.html", error="Usuario no existe")

        id_u, nombre, username, stored_pass, rol = row

        if rol == "admin":
            if stored_pass == clave:
                session["usuario"] = username
                session["rol"] = rol
                return redirect("/")
            else:
                return render_template("login.html", error="Contraseña incorrecta")
        else:
            session["usuario"] = username
            session["rol"] = rol
            return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/detalle/<int:id>")
def detalle(id):
    if "usuario" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM computadores WHERE id = ?", (id,))
    pc = cur.fetchone()

    if not pc:
        return "Equipo no encontrado", 404

    return render_template("detalle.html", pc=pc)


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if "usuario" not in session or session["rol"] != "admin":
        return redirect("/login")

    if request.method == "POST":
        datos = (
            request.form["serial"],
            request.form["marca"],
            request.form["modelo"],
            request.form["procesador"],
            request.form["ram"],
            request.form["almacenamiento"]
        )

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO computadores (serial, marca, modelo, procesador, ram, almacenamiento)
            VALUES (?,?,?,?,?,?)
        """, datos)
        conn.commit()

        return redirect("/")

    return render_template("registrar.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if "usuario" not in session or session["rol"] != "admin":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        datos = (
            request.form["serial"],
            request.form["marca"],
            request.form["modelo"],
            request.form["procesador"],
            request.form["ram"],
            request.form["almacenamiento"],
            id
        )

        cur.execute("""
            UPDATE computadores SET serial=?, marca=?, modelo=?, procesador=?, ram=?, almacenamiento=?
            WHERE id=?
        """, datos)
        conn.commit()

        return redirect("/")

    cur.execute("SELECT * FROM computadores WHERE id = ?", (id,))
    pc = cur.fetchone()

    return render_template("editar.html", pc=pc)


@app.route("/eliminar/<int:id>")
def eliminar(id):
    if "usuario" not in session or session["rol"] != "admin":
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM computadores WHERE id = ?", (id,))
    conn.commit()

    return redirect("/")


# -------------------------
# EJECUTAR
# -------------------------
if __name__ == "__main__":
    if not os.path.exists(APP_DB):
        conn = sqlite3.connect(APP_DB)
        with open("inventario.sql", "r") as f:
            conn.executescript(f.read())
        conn.close()

    app.run(debug=True)
