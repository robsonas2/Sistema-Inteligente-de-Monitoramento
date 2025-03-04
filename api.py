from flask import Flask, request, jsonify, render_template

import mysql.connector

app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    "host": "robsonas.mysql.pythonanywhere-services.com",
    "user": "robsonas",
    "password": "aparecido",
    "database": "robsonas$automa"
}

@app.route('/inserir', methods=['POST'])
def inserir_dados():
    try:
        # Recebe os dados JSON da requisição
        dados = request.json
        refrigerador = dados.get("refrigerador")
        correnteEletrica = dados.get("correnteEletrica")


        if correnteEletrica is None:
            return jsonify({"erro": "Dados inválidos"}), 400

        # Conectar ao MySQL e inserir dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sensores (refrigerador, correnteEletrica) VALUES (%s, %s)", (int(refrigerador), float(correnteEletrica)))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Dados inseridos com sucesso!"}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota principal para exibir os dados
@app.route('/')
def refrigerador_1():
    # Conectar ao banco de dados MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Consultar os dados da tabela
    cursor.execute("SELECT * FROM sensores")
    sensores = cursor.fetchall()

    # Fechar a conexão com o banco
    cursor.close()
    conn.close()

    # Renderizar a página com os dados
    return render_template('refrigerador_1.html', sensores=sensores)

if __name__ == '__main__':
    app.run()



