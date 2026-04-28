from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ.get("DB_NAME", "dimdim"),
        user=os.environ.get("DB_USER", "dimdim"),
        password=os.environ.get("DB_PASSWORD", "dimdim123")
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cpf VARCHAR(14) UNIQUE NOT NULL,
            email VARCHAR(100),
            saldo NUMERIC(10,2) DEFAULT 0.00,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/clientes", methods=["POST"])
def criar_cliente():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clientes (nome, cpf, email, saldo) VALUES (%s, %s, %s, %s) RETURNING id",
        (data["nome"], data["cpf"], data.get("email"), data.get("saldo", 0))
    )
    novo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": novo_id, "mensagem": "Cliente criado com sucesso!"}), 201

@app.route("/clientes", methods=["GET"])
def listar_clientes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, cpf, email, saldo, criado_em FROM clientes ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    clientes = [
        {"id": r[0], "nome": r[1], "cpf": r[2], "email": r[3], "saldo": float(r[4]), "criado_em": str(r[5])}
        for r in rows
    ]
    return jsonify(clientes)

@app.route("/clientes/<int:id>", methods=["GET"])
def buscar_cliente(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, cpf, email, saldo, criado_em FROM clientes WHERE id = %s", (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({"id": row[0], "nome": row[1], "cpf": row[2], "email": row[3], "saldo": float(row[4]), "criado_em": str(row[5])})

@app.route("/clientes/<int:id>", methods=["PUT"])
def atualizar_cliente(id):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE clientes SET nome = %s, email = %s, saldo = %s WHERE id = %s RETURNING id",
        (data["nome"], data.get("email"), data.get("saldo", 0), id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({"mensagem": "Cliente atualizado com sucesso!"})

@app.route("/clientes/<int:id>", methods=["DELETE"])
def deletar_cliente(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE id = %s RETURNING id", (id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({"mensagem": "Cliente deletado com sucesso!"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "app": "DimDim API"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)