from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Armazenamento em memória (Simula um "banco de dados" simples)
# Este dicionário guarda a última senha e a última vaga/guichê chamados.
estado_guiche = {
    'senha': '---',
    'vaga': '---'
}

@app.route('/')
def index():
    """Rota inicial que mostra o painel do atendente."""
    return render_template('atendente.html')

@app.route('/monitor')
def monitor():
    """Rota para o painel de exibição (a TV/Monitor)."""
    return render_template('monitor.html')

@app.route('/chamar', methods=['POST'])
def chamar_senha():
    """Rota que o atendente usa para enviar a nova senha."""
    data = request.json
    
    # Atualiza o estado
    estado_guiche['senha'] = data.get('senha', estado_guiche['senha'])
    estado_guiche['vaga'] = data.get('vaga', estado_guiche['vaga'])
    
    print(f"NOVA CHAMADA: Senha {estado_guiche['senha']} -> Vaga {estado_guiche['vaga']}")
    
    # Retorna o estado atual como confirmação
    return jsonify(estado_guiche)

@app.route('/status', methods=['GET'])
def get_status():
    """Rota que o monitor usa para buscar o estado atual (Polling)."""
    return jsonify(estado_guiche)

if __name__ == '__main__':
    # Para executar, use: python app.py
    # O debug=True permite que o código seja recarregado automaticamente ao salvar
    app.run(host='0.0.0.0', port=5000, debug=True)
