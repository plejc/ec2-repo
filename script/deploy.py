# deploy.py

from fabric import Connection

# Define your EC2 instance SSH details
EC2_HOST = '65.2.10.118'
EC2_USER = 'ec2-user'
EC2_KEY_PATH = 'D:/ec2-pem.pem'

# Define the directory where your Django project resides on the EC2 instance
PROJECT_DIR = '/home/ec2-user/ec2-repo'

# Define the command to restart the Django server
RESTART_COMMAND = 'sudo systemctl restart gunicorn'

def deploy():
    # Connect to the EC2 instance
    conn = Connection(host=EC2_HOST, user=EC2_USER, connect_kwargs={'key_filename': EC2_KEY_PATH})

    # Pull latest changes from Git repository
    print("Pulling latest changes from Git repository...")
    with conn.cd(PROJECT_DIR):
        conn.run('git pull')

    # Install/update dependencies (assuming you're using a virtual environment)
    print("Installing/updating dependencies...")
    with conn.cd(PROJECT_DIR):
        conn.run('source venv/bin/activate && pip install -r requirements.txt')

    # Collect static files and perform database migrations
    print("Collecting static files and performing migrations...")
    with conn.cd(PROJECT_DIR):
        conn.run('source venv/bin/activate && python manage.py collectstatic --noinput')
        conn.run('source venv/bin/activate && python manage.py migrate --noinput')

    # Restart the Django server to apply changes
    print("Restarting Django server...")
    with conn.cd(PROJECT_DIR):
        conn.sudo(RESTART_COMMAND)

    print("Deployment complete.")

if __name__ == '__main__':
    deploy()
