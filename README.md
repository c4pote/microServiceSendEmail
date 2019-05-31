# MicroService Send Email

### Criado para ser agendado via cron do linux ou agendador de tarefa no windows.

### Ajuste as configurações de email e do banco de dados no arquivo settings.py antes de iniciar.


Esse projeto foi utilizado para disparar um email para clientes que possuem parcelas em atraso.

Ele se conecta ao Postgres, obtem parcelas em atraso, e envia um email de notificação
