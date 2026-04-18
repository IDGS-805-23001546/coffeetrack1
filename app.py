from flask import render_template
from app import create_app
from flask import current_app

app = create_app()

@app.route('/')
def index():
    current_app.logger.info("Entró al index")
    return render_template('clientes/index.html')

if __name__ == '__main__':
    app.run(debug=False)