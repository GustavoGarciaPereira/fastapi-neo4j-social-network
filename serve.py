import uvicorn
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

def start_frontend():
    """Inicia o servidor do frontend na porta 8080"""
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    os.chdir(frontend_dir)
    
    server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print("🚀 Frontend rodando em http://localhost:8080")
    server.serve_forever()

def start_backend():
    """Inicia o backend FastAPI na porta 8000"""
    print("🚀 Backend iniciando...")
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)

if __name__ == "__main__":
    # Verificar se a pasta frontend existe
    if not os.path.exists("frontend"):
        print("❌ Pasta 'frontend' não encontrada!")
        exit(1)
    
    print("🎉 Iniciando Frontend e Backend...")
    
    # Iniciar backend em thread separada
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Aguardar o backend iniciar
    time.sleep(3)
    
    # Iniciar frontend
    start_frontend()