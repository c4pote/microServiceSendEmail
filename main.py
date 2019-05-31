#Importando Configurações
from settings import Settings

#Importando Postgres
from postgres import ConPostgres

# Import para recursos de Email.
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Configurações 
settings = Settings.config()
##Email
smtp = settings[0]
smtp_port = settings[1]
sender_email = settings[2]
password = settings[3]

##Postgres
pg_host = settings[4]
pg_database = settings[5]
pg_user = settings[6]
pg_password = settings[7]

#Configurações da regra de negocio
send_limit = 400

def send(receiver_email, titulo, mensagem):
    receiver_email = receiver_email.split(',')

    message = MIMEMultipart("alternative")
    message["Subject"] = titulo
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)

    # Create the plain-text and HTML version of your message
    #text = """\
    #Prezado(a),
    #
    #Em nosso sistema consta, em sua conta, a(s) seguinte(s) parcela(s) vencida(s) há mais de {} dias. Sendo assim, solicitamos a regularização imediata do(s) mesmo(s).
    #
    #Caso o pagamento já tenha sido efetuado, por favor, entre em contato conosco através das seguintes opções:
    #Telefones:(11) 2172-0405 / (11) 2060-0405
    #Email: cobranca@jati.com.br
    #Atenciosamente.""".format(day_arrear)
    html = mensagem

    # Turn these into plain/html MIMEText objects
    #part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    #message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp, smtp_port)
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

#Chama função que preenche a tabela com as parcelas que precisam ser cobradas
def newInstallmentsArrears(con):
    sql ="""SELECT atraso_parcelas_aviso({})""".format(send_limit)
    rs=con.manipulate(sql)

def registerSend(id, con):
    sql = """UPDATE fin_cobranca_atraso SET status = 1 WHERE \
    fin_cobranca_atraso.id = {}""".format(id)
    try:
        if con.manipulate(sql):
            print('Sending Register Successfully')
        else:
            print(sql)
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error while connection to PostgreSQL", error)

def sendNotification(con):
    sql = """SELECT a.id, a.data, a.titulo, a.conteudo, a.email, a.status \
    FROM fin_cobranca_atraso a \
    WHERE a.status = 0 limit {}""".format(send_limit)
    rs=con.consult(sql)
    for row in rs:
        id = row[0]
        titulo = row[2]
        conteudo = row[3].replace(',','<BR>')
        email = row[4]

        html = """\
        <html>
          <body>
            <p>Prezado(a),<br>
               Em nosso sistema consta, em sua conta, a(s) seguinte(s) parcela(s) vencida(s) há mais de 1 dia, Sendo assim, solicitamos a regularização imediata do(s) mesmo(s).
               <p style="padding-left: 20px"><b>Parcela(s):</b><br><div style="padding: 0px 0px 5px 40px">{}</div></p><br>
               Caso o pagamento já tenha sido efetuado, por favor, 
               entre em contato conosco através das seguintes opções:</p>

               <p>Telefones:(11) 2172-0405 / (11) 2060-0405</p>

               <p> Email: cobranca@jati.com.br</p>
              <p>
               Atenciosamente.
            </p>
          </body>
        </html>
        """.format(conteudo)
    
        try:
            send(email, titulo, html)
        except:
            print("Send Error")
        else:           
            registerSend(id, con)
            print('Send Success')

#Iniciando Conexão com banco de dados
#Start Connection BD
con = ConPostgres(pg_host, pg_database, pg_user, pg_password)

#Obtendo novas parcelas para alertar
#Getting new installments to notify
newInstallmentsArrears(con)

#Enviando notificação de parcelas em atraso 
#Sending notification of overdue installments
try:  
    sendNotification(con)
except:
    print('Error not found')
else:
    print('Late Payment Notification Made Successfully')
finally:
    if(con):
        con.disconnect()
        print("PostgreSQL conncetion is closed")

