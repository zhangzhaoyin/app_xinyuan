import smtplib
from email.mime.text import MIMEText
import configparser
mailto_list=["zhiyum@princetechs.com","shushiz@princetechs.com","zhaoyinz@princetechs.com"]
mail_host="smtp.exmail.qq.com"  #设置服务器
mail_user="zhaoyinz@princetechs.com"    #用户名
mail_pass="321zzy"   #口令
mail_postfix="princetechs.com"  #发件箱的后缀

class sendEmail():
    def __init__(self):
        # self.data = '../sendEmail.conf'
        self.error1 = None
        self.error2 = None

    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('../sendEmail.conf', 'utf8')
        self.recipients = config.get('recipients', 'recipient').split(',')
        self.error1 = config.get('content', 'error1')
        self.error2 = config.get('content', 'error2')
        # print (self.recipients.split(','))

    def send_mail(self,to_list,content):  #to_list：收件人；sub：主题；content：邮件内容
        me="程序自动发送"+"<"+mail_user+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
        msg = MIMEText(content,_subtype='html',_charset='gb2312')    #创建一个实例，这里设置为html格式邮件
        msg['Subject'] = '报警邮件'   #设置主题
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            s = smtplib.SMTP()
            s.connect(mail_host)  #连接smtp服务器
            s.login(mail_user,mail_pass)  #登陆服务器
            s.sendmail(me, to_list, msg.as_string())  #发送邮件
            s.close()
            return True
        except Exception as e:
            print (str(e))
            return False



if __name__ == '__main__':
    s = sendEmail()
    s.readConfig()
    s.send_mail(mailto_list,s.error1)