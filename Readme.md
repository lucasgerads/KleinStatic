This is a simple static site generator. Just add markdown files to the data directory and a static site is created inside the static folder. 

clone repository

    git clone https://github.com/lucasgerads/KleinStatic.git

move into directory 

    cd KleinStatic/

create virtual envirnmont

    python -m venv venv

activate virtual envirnmont

    source venv/bin/activate

install requirements

    pip install -r requirements.txt

start server

    python server.py