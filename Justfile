set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

up:
    docker compose up --build
down:
    docker compose down
ps:
    docker compose ps
