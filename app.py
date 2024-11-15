from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://parcialinf530adriannina_user:DbCWptXmNf5hdd4sJzZx1p0CdmEtH8Xq@dpg-csrkept2ng1s738aca9g-a/parcialinf530adriannina'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo Vehiculo sin campo 'id' y con 'placa' como clave primaria
class Vehiculo(db.Model):
    placa = db.Column(db.String(20), primary_key=True)
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

# Leer un vehículo por placa
@app.route('/vehiculos/<string:placa>', methods=['GET'])
def get_vehiculo(placa):
    vehiculo = Vehiculo.query.filter_by(placa=placa).first()
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    return jsonify({
        'placa': vehiculo.placa,
        'color': vehiculo.color,
        'modelo': vehiculo.modelo,
        'marca': vehiculo.marca
    })

# Actualizar un vehículo por placa
@app.route('/vehiculos/<string:placa>', methods=['PUT'])
def update_vehiculo(placa):
    vehiculo = Vehiculo.query.filter_by(placa=placa).first()
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    data = request.json
    vehiculo.color = data.get('color', vehiculo.color)
    vehiculo.modelo = data.get('modelo', vehiculo.modelo)
    vehiculo.marca = data.get('marca', vehiculo.marca)
    db.session.commit()
    return jsonify({'message': 'Vehículo actualizado exitosamente'})

# Eliminar un vehículo por placa
@app.route('/vehiculos/<string:placa>', methods=['DELETE'])
def delete_vehiculo(placa):
    vehiculo = Vehiculo.query.filter_by(placa=placa).first()
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404
    db.session.delete(vehiculo)
    db.session.commit()
    return jsonify({'message': 'Vehículo eliminado exitosamente'})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
