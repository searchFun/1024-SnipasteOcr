image_hashIndex = 0


def send(to: list, title, cc=None, inspector=True, body="", attachments=None):
    import win32com.client as win32
    outlook = win32.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)
    # 设置收件人
    if to is None:
        raise Exception("收件人不能为空!")
    mail.To = __combine__(to)
    # 设置抄送人
    if cc is not None:
        mail.CC = __combine__(cc)
    # 设置邮件主题
    if title is None:
        raise Exception("邮件主题不能为空!")
    mail.Subject = title
    # 是否附带签名
    # 带默认签名
    import re
    if inspector is True:
        mail.GetInspector()
        bodystart = re.search("<body.*?>", mail.HTMLBody)  # 找到签名里面的body头，签名是html格式的
        mail.HTMLBody = re.sub(bodystart.group(), bodystart.group() + body, mail.HTMLBody)
    # 不带签名
    else:
        bodystart = re.search("<BODY.*?>", mail.HTMLBody)  # 找到签名里面的body头，签名是html格式的
        mail.HTMLBody = re.sub(bodystart.group(), bodystart.group() + body, mail.HTMLBody)

    if attachments is not None:
        for attachment in attachments:
            attach = mail.Attachments.Add(attachment['path'])
            if attachment['bodyImage'] is True:
                attach.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                                                        attachment['name'])
    mail.Send()
    print("发送完成")


def draft(to: list, title, cc=None, inspector=True, body="", attachments=None):
    import win32com.client as win32
    outlook = win32.Dispatch('Outlook.Application')
    mail = outlook.CreateItem(0)
    # 设置收件人
    if to is None:
        raise Exception("收件人不能为空!")
    mail.To = __combine__(to)
    # 设置抄送人
    if cc is not None:
        mail.CC = __combine__(cc)
    # 设置邮件主题
    if title is None:
        raise Exception("邮件主题不能为空!")
    mail.Subject = title
    # 是否附带签名
    # 带默认签名
    import re
    if inspector is True:
        mail.GetInspector()
        bodystart = re.search("<body.*?>", mail.HTMLBody)  # 找到签名里面的body头，签名是html格式的
        mail.HTMLBody = re.sub(bodystart.group(), bodystart.group() + body, mail.HTMLBody)
    # 不带签名
    else:
        bodystart = re.search("<BODY.*?>", mail.HTMLBody)  # 找到签名里面的body头，签名是html格式的
        mail.HTMLBody = re.sub(bodystart.group(), bodystart.group() + body, mail.HTMLBody)

    if attachments is not None:
        for attachment in attachments:
            attach = mail.Attachments.Add(attachment['path'])
            if attachment['bodyImage'] is True:
                attach.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                                                    get_image_hash())
    # mail.Display()
    mail.Save()
    print("保存至Draft成功！")


def get_image_hash():
    global image_hashIndex
    image_hashIndex = image_hashIndex + 1
    return "image" + str(image_hashIndex)


def __combine__(items: list):
    string = ""
    for item in items:
        string = string + item + ";"
    return string
