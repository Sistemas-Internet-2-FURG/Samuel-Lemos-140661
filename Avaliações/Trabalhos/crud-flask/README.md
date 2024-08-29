### Como rodar o projeto:

Primeiramente, na raiz do projeto crie um arquivo ".env" identico ao arquivo ".env.example" e no campo "DATABASE_URL" coloque seu endereço de conexão com o banco de dados remoto no formato: 

       postgresql+psycopg2://username:password@host:port/database

Abra o terminal e digite o comando na raiz do projeto:

        pip install -r requirements.txt

Após isso, acesse a pasta "app" através do comando:

        cd app

Agora é só executar o arquivo "app.py" através do comando:

        python app.py