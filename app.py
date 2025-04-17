from flask import Flask, render_template, request 
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    custo_produto = float(request.form["custo_produto"])
    tipo_anuncio = request.form["tipo_anuncio"]
    frete_gratis = request.form["frete_gratis"]
    outras_despesas = request.form.get("outras_despesas", 0) or 0
    preco_venda = request.form.get("preco_venda")
    margem_desejada = request.form.get("margem_desejada")

    outras_despesas = float(outras_despesas)
    preco_venda = float(preco_venda) if preco_venda else None
    margem_desejada = float(margem_desejada) if margem_desejada else None

    taxa = 0.11 if tipo_anuncio == "classico" else 0.16
    custo_frete = 20.0 if frete_gratis == "sim" else 0.0

    resultado = {}
    if preco_venda:
        taxa_ml = preco_venda * taxa
        lucro = preco_venda - (custo_produto + outras_despesas + taxa_ml + custo_frete)
        margem = (lucro / preco_venda) * 100
        resultado["tipo"] = "lucro"
        resultado["lucro"] = lucro
        resultado["margem"] = margem
        resultado["preco_venda"] = preco_venda
    elif margem_desejada:
        custo_total = custo_produto + outras_despesas + custo_frete
        preco_necessario = custo_total / (1 - taxa - (margem_desejada / 100))
        resultado["tipo"] = "preco_minimo"
        resultado["preco_necessario"] = preco_necessario
        resultado["margem_desejada"] = margem_desejada
    else:
        resultado["tipo"] = "erro"

    return render_template("resultado.html", resultado=resultado)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
