Para que o projeto funcione corretamente, é necessário configurar a conexão com o MySQL.
Você pode fazer isso de duas formas:

1. Alterando diretamente as variáveis no arquivo conn, preenchendo com suas credenciais do MySQL.
2. Criando um arquivo .env contendo essas mesmas variáveis, para manter os dados sensíveis fora do código.
Em caso de dúvida, deixarei abaixo um modelo de .env para facilitar a configuração.

DB_HOST= seu host no mySql
DB_USER= seu user no mySql
DB_PASSWORD= sua senha do mySql
DB_PORT="3306" ou a porta que você está usando
DB_AUTH_PLUGIN="mysql_native_password" ou o outro método de autenticação que você está usando
DB_TIMEOUT="3"
DB_USE_PURE="True"
DB_SSL_DISABLED="True"
DB_NAME= nome do seu banco de dados

Além disso, é importante ressaltar que o arquivo .env também deve incluir a chave de sessão do Flask, utilizada pelo framework para gerenciar sessões de forma segura.
SECRET_TOKEN= aqui insira uma senha aleátoria, de preferência com mais de 30 caracteres (alterando sequências alfabéticas e numéricas).
