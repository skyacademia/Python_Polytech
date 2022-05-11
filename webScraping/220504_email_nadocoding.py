import smtplib

with smtplib.SMTP("smtp.gmail.com",587) as smtp:
    smtp.helo()
    smtp.starttls()
    smtp.login("nc40403@naver.com")

    subject = "Title"
    body = "text"
    msg = f"Subject:{subject}\n{body}"
    smtp.sendmail("nc40403@naver.com","nc40403@gmail.com",msg) # sendmail(발신자,수신자,일정한 형식의 메시지)