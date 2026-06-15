from flask import Flask, render_template
import socket

app = Flask(__name__)

HOST = "192.168.1.22"
PORT = 12345


def leer_sensor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = s.recv(1024).decode().strip()

            print("RECIBIDO:", data)

            ejeX, ejeY = data.split(',')
            ejeX = float(ejeX.replace('X:', ''))
            ejeY = float(ejeY.replace('Y:', ''))

            return ejeX, ejeY

    except Exception as e:
        print("ERROR:", e)
        return 0, 0


def escalar(valor):
    valor = max(-10, min(10, valor))
    return min(3, int((valor + 10) / 5))
    
@app.route('/')
def index():
    ejeX, ejeY = leer_sensor()
    return render_template(
        'index.html',
        ejeX=ejeX,
        ejeY=ejeY
    )


@app.route('/matrix')
def matrix():
    ejeX, ejeY = leer_sensor()

    x = escalar(ejeX)
    y = escalar(ejeY)

    return render_template(
        'matrix.html',
        ejeX=ejeX,
        ejeY=ejeY,
        x=x,
        y=y
    )
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
