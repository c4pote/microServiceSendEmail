class Settings:

    def __init__(seft):
        return self

    def config():
        #Configurações email de disparo das notificações
        smtp = "smtp-relay.gmail.com"
        smtp_port = 465
        sender_email = "seuemail@algumacoisa.com"
        password = "suasenha"

        #Configurações Postgres
        pg_host = "ipdobancodedados"
        pg_database = "database"
        pg_user = "postgres"
        pg_password = "suasenha"
        return [smtp, smtp_port, sender_email, password, pg_host, pg_database, pg_user, pg_password]
