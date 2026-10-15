from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="Hortasmart_isabella"
    )


def consultar(sql, params=()):
    con = conectar()
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql, params)
    dados = cursor.fetchall()
    con.close()
    return dados


def executar(sql, params=()):
    con = conectar()
    cursor = con.cursor()
    cursor.execute(sql, params)
    con.commit()
    con.close()


@app.route("/")
def inicio():
    return app.send_static_file("index.html")


@app.route("/plantas", methods=["GET"])
def listar_plantas():
    return jsonify(consultar("SELECT * FROM plantas"))


@app.route("/plantas", methods=["POST"])
def adicionar_planta():
    nome = request.get_json()["nome"]
    executar("INSERT INTO plantas (nome) VALUES (%s)", (nome,))
    return "", 201


@app.route("/sensores", methods=["GET"])
def ver_sensor():
    dados = consultar("SELECT * FROM sensores WHERE id = 1")
    if len(dados) == 0:
        return jsonify({"umidade": 0, "agua": 0})
    return jsonify(dados[0])


@app.route("/sensores/umidade", methods=["PUT"])
def atualizar_umidade():
    valor = request.get_json()["valor"]
    executar("UPDATE sensores SET umidade = %s WHERE id = 1", (valor,))
    return "", 200


@app.route("/sensores/agua", methods=["PUT"])
def atualizar_agua():
    valor = request.get_json()["valor"]
    executar("UPDATE sensores SET agua = %s WHERE id = 1", (valor,))
    return "", 200


@app.route("/alertas", methods=["GET"])
def listar_alertas():
    return jsonify(consultar("SELECT * FROM alertas"))


@app.route("/alertas", methods=["POST"])
def adicionar_alerta():
    mensagem = request.get_json()["mensagem"]
    executar("INSERT INTO alertas (mensagem) VALUES (%s)", (mensagem,))
    return "", 201


@app.route("/alertas/<int:id>", methods=["DELETE"])
def remover_alerta(id):
    executar("DELETE FROM alertas WHERE id = %s", (id,))
    return "", 200


if __name__ == "__main__":
    app.run(debug=True)
