from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos en memoria (simple)
tareas = []
contador_id = 1

@app.route('/')
def home():
    return jsonify({"mensaje": "¡Bienvenido a la API de Tareas!"})

@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    """Obtiene todas las tareas"""
    return jsonify({"tareas": tareas})

@app.route('/tareas', methods=['POST'])
def crear_tarea():
    """Crea una nueva tarea"""
    global contador_id
    data = request.get_json()
    
    if not data or 'titulo' not in data:
        return jsonify({"error": "El título es requerido"}), 400
    
    nueva_tarea = {
        "id": contador_id,
        "titulo": data['titulo'],
        "completada": False
    }
    tareas.append(nueva_tarea)
    contador_id += 1
    
    return jsonify(nueva_tarea), 201

@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    """Elimina una tarea por su ID"""
    global tareas
    tareas = [t for t in tareas if t['id'] != tarea_id]
    return jsonify({"mensaje": "Tarea eliminada"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

### **3.2 Crear: requirements.txt**

