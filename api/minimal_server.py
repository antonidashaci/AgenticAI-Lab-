"""
Minimal HTTP Server for AgenticAI Lab
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class AgenticAIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3001')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3001')
        self.end_headers()
        
        if self.path == '/health':
            response = {"status": "healthy", "version": "0.1.0"}
        elif self.path == '/api/v1/agents':
            response = {
                "agents": [
                    {"id": "mistral", "name": "Mistral 7B", "status": "ready"},
                    {"id": "codellama", "name": "Code Llama 13B", "status": "ready"}
                ]
            }
        elif self.path == '/api/v1/jobs':
            response = {
                "jobs": [
                    {"id": "job_test1", "type": "content_creation", "status": "completed"},
                    {"id": "job_test2", "type": "content_creation", "status": "processing"}
                ]
            }
        else:
            response = {"message": "AgenticAI Minimal Server", "version": "0.1.0"}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        if self.path == '/api/v1/jobs':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                job_data = json.loads(post_data.decode('utf-8'))
                prompt = job_data.get('prompt', 'Default prompt')
                
                # Simulate AI response
                response = {
                    "id": "job_12345",
                    "status": "completed",
                    "type": "content_creation",
                    "message": "Job completed successfully!",
                    "content": f"AI Response to: {prompt}\n\nThis is a simulated AI-generated content about your topic. The system would normally connect to Ollama/Mistral to generate real content, but this is a test response to verify the connection works.",
                    "model": "test-mode"
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', 'http://localhost:3001')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', 'http://localhost:3001')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8001), AgenticAIHandler)
    print("AgenticAI Minimal Server starting...")
    print("Frontend: http://localhost:3001")
    print("Backend: http://localhost:8001")
    print("Health: http://localhost:8001/health")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
