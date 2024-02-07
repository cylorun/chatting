PORT = 25565
HOSTNAME = f'https://ed36-153-92-137-203.ngrok-free.app/'
import requests

response = requests.get('http://localhost:4040/api/tunnels')
data = response.json()

for tunnel in data['tunnels']:
    if tunnel['proto'] == 'tcp':  # Assuming you're interested in TCP tunnels
        print("Public URL for TCP tunnel:", tunnel['public_url'])
