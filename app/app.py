from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos desde .env
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')  # Valor por defecto 3306 si no está definido
DB_NAME = os.getenv('DB_NAME')

# Convertir el puerto a entero
try:
    DB_PORT = int(DB_PORT)
except ValueError:
    raise ValueError("La variable DB_PORT debe ser un número entero válido.")

# Construir la URI de conexión
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Modelo de la orden
class Orden(db.Model):
    __tablename__ = "Ordenes"

    ID_Orden = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Cliente = db.Column(db.Integer, nullable=False)
    ID_Restaurante = db.Column(db.Integer, nullable=False)
    Fecha = db.Column(db.Date, nullable=False)
    Hora = db.Column(db.Time, nullable=False)
    Numero_Personas = db.Column(db.Integer, nullable=False)
    Estado = db.Column(db.Enum("Pendiente", "Confirmada", "Cancelada"), default="Pendiente")


# Ruta para leer una orden por ID
@app.route('/orders/<int:order_id>', methods=['GET'])
def read_order(order_id):
    try:
        order = Orden.query.get(order_id)

        if not order:
            return jsonify({"error": "Orden no encontrada"}), 404

        order_data = {
            "ID_Orden": order.ID_Orden,
            "ID_Cliente": order.ID_Cliente,
            "ID_Restaurante": order.ID_Restaurante,
            "Fecha": str(order.Fecha),
            "Hora": str(order.Hora),
            "Numero_Personas": order.Numero_Personas,
            "Estado": order.Estado
        }

        return jsonify(order_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
