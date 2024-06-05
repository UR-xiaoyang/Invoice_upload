import smtplib
from email.mime.text import MIMEText
from 用户.邮箱.smtp配置 import smtp配置


def SMTP(收件人, 邮件内容):
    try:
        # 创建连接
        smtp = smtplib.SMTP_SSL(smtp配置.SMTP服务器, smtp配置.SMTP端口)
        print("连接SMTP服务器成功")

        # 登录
        smtp.login(smtp配置.SMTP用户, smtp配置.SMTP密码)
        print("SMTP服务器登录成功")

        # 构造邮件内容并指定编码
        msg = MIMEText(邮件内容, 'plain', 'utf-8')
        msg['From'] = smtp配置.SMTP用户
        msg['To'] = 收件人
        msg['Subject'] = '邮件主题示例'  # 可以自定义邮件主题
        smtp.send_message(msg)
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(f"SMTP服务器异常: {e}")
    except Exception as e:
        print(f"其他异常: {e}")
    finally:
        # 检查连接状态再决定是否调用quit()
        if smtp and smtp.sock:  # 使用sock属性检查连接状态
            smtp.quit()
            print("SMTP连接已关闭")
        else:
            print("SMTP连接已关闭或未成功建立，无需再次关闭")


#SMTP("2422286329@qq.com", "测试邮件")
