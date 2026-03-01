from flask import render_template
from app import create_app

app = create_app()

@app.route('/')
def index():
    # Esta línea debe cargar la imagen del café
    return render_template('clientes/index.html')

if __name__ == '__main__':
    app.run(debug=True)