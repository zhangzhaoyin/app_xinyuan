import configparser
config = configparser.ConfigParser()
config.read('sendEmail.conf')

config.add_section('recipients')
config.set('recipients','recipient','zhiyum@princetechs.com,shushiz@princetechs.com')

config.add_section('content')
config.set('content','error1','错误提示:文件不是utf8')
config.set('content','error2','错误提示:更新失败')


config.write(open('sendEmail.conf','w',encoding='utf8'))