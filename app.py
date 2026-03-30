from flask import render_template
from app import create_app


#levantar app
app = create_app()

@app.route('/')
def index():
    return render_template('clientes/index.html')

if __name__ == '__main__':
    app.run(debug=True)