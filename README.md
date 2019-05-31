# MicroService Send Email

### Criado para ser agendado via cron do linux ou agendador de tarefa no windows.

### Ajuste as configurações de email e do banco de dados no arquivo settings.py antes de iniciar.


Esse projeto foi utilizado para disparar um email para clientes que possuem parcelas em atraso.

Ele se conecta ao Postgres, obtem parcelas em atraso, e envia um email de notificação


'''
CREATE TABLE fin_cobranca_atraso
(
  id serial NOT NULL, -- 
  data timestamp without time zone,
  titulo text,
  conteudo text,
  email character varying(300),
  status integer NOT NULL DEFAULT 0,
  idcliente integer,
  idparcelas integer[],
  CONSTRAINT fin_cobranca_atraso_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE fin_cobranca_atraso
  OWNER TO postgres;
COMMENT ON TABLE fin_cobranca_atraso
  IS 'Tabela que precisa ser alimentada para registro de cobrancas de atrasos por email';
COMMENT ON COLUMN fin_cobranca_atraso.id IS '
';
'''
