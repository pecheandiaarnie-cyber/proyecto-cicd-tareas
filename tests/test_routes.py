import pytest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, tareas

@pytest.fixture
def client():
    """Crea un cliente de prueba para la aplicación"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Limpiar tareas después de cada prueba
    tareas.clear()

def test_home(client):
    """Prueba la ruta principal"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Bienvenido' in response.data

def test_obtener_tareas_vacio(client):
    """Prueba obtener tareas cuando la lista está vacía"""
    response = client.get('/tareas')
    assert response.status_code == 200
    data = response.get_json()
    assert data['tareas'] == []

def test_crear_tarea(client):
    """Prueba crear una nueva tarea"""
    nueva_tarea = {"titulo": "Estudiar CI/CD"}
    response = client.post('/tareas', json=nueva_tarea)
    assert response.status_code == 201
    data = response.get_json()
    assert data['titulo'] == "Estudiar CI/CD"
    assert data['completada'] == False

def test_crear_tarea_sin_titulo(client):
    """Prueba crear una tarea sin título (debe fallar)"""
    response = client.post('/tareas', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_eliminar_tarea(client):
    """Prueba eliminar una tarea"""
    # Primero crear una tarea
    client.post('/tareas', json={"titulo": "Tarea temporal"})
    
    # Luego eliminarla
    response = client.delete('/tareas/1')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['mensaje'] == 'Tarea eliminada' 
    