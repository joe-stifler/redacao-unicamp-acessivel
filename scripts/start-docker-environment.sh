docker run -d -it -p 8501:8501 -v /home/joe/Documents/1-PROJECTS/redacao-unicamp-acessivel:/workspace --name redacao-unicamp-acessivel python:3.10

docker exec -w /workspace -it redacao-unicamp-acessivel bash
