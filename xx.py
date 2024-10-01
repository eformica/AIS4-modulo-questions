import subprocess

# Executar o comando 'ls -la' em segundo plano
processo = subprocess.Popen(['python', 'application/listener_runner.py', 'teste'], start_new_session=True)
