pip3 install -r requirements.txt
pip3 install -e /app

cd ././src/endpoint/migrations/
alembic upgrade head
cd /app

# Replace Bash process with Python process. As PID1 Python will receive all signals
exec run_endpoint
