from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time, datetime, requests
from timeit import default_timer as timer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'Hello, World!'}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/mockfile':
            self.handle_mockfile()
        elif self.path == '/mockfile_by_proxy':
            self.handle_mockfile_by_proxy()
        else:
            self.send_error(404, 'Endpoint non trouvé')

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            self.send_response(200)
            self.end_headers()
            response = {'message': 'Données reçues avec succès'}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, 'Endpoint non trouvé')

    def handle_mockfile(self):
        try:
            start_time = timer()

            stars = ''
            for x in range(0, 357000):
                stars += "*"

            dt = datetime.datetime.utcnow()
            dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            json_data = json.dumps(dt_str)

            data = {
                "value": stars,
                "creation-date": json_data,
                "execution_time": 0,
            }

            end_time = timer()
            execution_time = end_time - start_time

            data.update({"execution_time": execution_time})

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            print(f"Erreur lors de l'envoi de la réponse : {e}")

        

    def handle_mockfile_by_proxy(self):
        start_time = timer()
        #Récupérer l'hôte et le port du serveur
        # host = self.headers.get('Host')
        # # Construire l'URL complète
        # url = f"http://{host}/mockfile"
        # Récupérer l'hôte et le port du serveur
        host_header = self.headers.get('Host')
        
        # Séparer l'hôte et le port à partir de l'en-tête Host
        host, port = host_header.split(':')
        
        # Construire l'URL complète en utilisant le port spécifié
        url = f"http://127.0.0.1:5000/mockfile"
        print(url)
        #response = requests.get(url, allow_redirects=False, timeout=5)
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()  # Lève une exception si la réponse n'est pas un succès
        except requests.exceptions.Timeout:
            print("Délai d'attente dépassé pour l'URL", url)
        except requests.exceptions.RequestException as e:
            print("Erreur lors de la requête vers l'URL", url, ":", e)
        else:
            # Vérifier si la réponse est au format JSON
            if response.headers.get('Content-Type') == 'application/json':
                json_data = response.json()
                received_file = {
                    "data": json_data,
                    "duration": 0
                }
                end_time = timer()
                execution_time = end_time - start_time
                received_file["duration"] = execution_time

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(received_file).encode())
            else:
                self.send_error(500, 'La réponse n\'est pas au format JSON')


def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Serveur démarré sur le port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
