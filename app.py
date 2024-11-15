from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/parcialinf530'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo Vehiculo
class Vehiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(20), nullable=False, unique=True)
    color = db.Column(db.String(20), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)

# Crear la base de datos y las tablas al iniciar la aplicación
with app.app_context():
    db.create_all()

# **Ruta de Inicio**
@app.route('/')
def home():
    return jsonify({'message': 'Bienvenido a la API de Vehículos'})

# **Rutas del CRUD**

# Leer todos los vehículos
@app.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    vehiculos = Vehiculo.query.all()
    return jsonify([{
        'id': v.id,
        'placa': v.placa,
        'color': v.color,
        'modelo': v.modelo,
        'marca': v.marca
    } for v in vehiculos])

# Crear un nuevo vehículo
@app.route('/vehiculos', methods=['POST'])
def add_vehiculo():
    data = request.json
    nuevo_vehiculo = Vehiculo(
        placa=data['placa'],
        color=data['color'],
        modelo=data['modelo'],
        marca=data['marca']
    )
    db.session.add(nuevo_vehiculo)
    db.session.commit()
    return jsonify({
        'message': 'Vehículo agregado exitosamente',
        'vehiculo': {
            'placa': nuevo_vehiculo.placa,
            'color': nuevo_vehiculo.color,
            'modelo': nuevo_vehiculo.modelo,
            'marca': nuevo_vehiculo.marca
        }
    }), 201


# Leer un vehículo por ID
@app.route('/vehiculos/<int:id>', methods=['GET'])
def get_vehiculo(id):
    vehiculo = Vehiculo.query.get(id)
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    return jsonify({
        'id': vehiculo.id,
        'placa': vehiculo.placa,
        'color': vehiculo.color,
        'modelo': vehiculo.modelo,
        'marca': vehiculo.marca
    })

# Actualizar un vehículo
@app.route('/vehiculos/<int:id>', methods=['PUT'])
def update_vehiculo(id):
    vehiculo = Vehiculo.query.get(id)
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    data = request.json
    vehiculo.placa = data.get('placa', vehiculo.placa)
    vehiculo.color = data.get('color', vehiculo.color)
    vehiculo.modelo = data.get('modelo', vehiculo.modelo)
    vehiculo.marca = data.get('marca', vehiculo.marca)
    db.session.commit()
    return jsonify({'message': 'Vehículo actualizado exitosamente'})

# Eliminar un vehículo
@app.route('/vehiculos/<int:id>', methods=['DELETE'])
def delete_vehiculo(id):
    vehiculo = Vehiculo.query.get(id)
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    db.session.delete(vehiculo)
    db.session.commit()
    return jsonify({'message': 'Vehículo eliminado exitosamente'})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
