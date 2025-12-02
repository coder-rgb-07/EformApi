from extract_msg import Message
import base64
import re
from bs4 import BeautifulSoup

def convert_msg_to_html(msg_path, output_html_path):
    # 解析MSG文件
    msg = Message(msg_path)
    
    # 提取HTML正文
    html_body = msg.htmlBody
    
    if not html_body:
        raise ValueError("该MSG文件没有HTML格式正文")
    
    # 创建CID到图片数据的映射
    cid_map = {}
    for attachment in msg.attachments:
        if attachment.cid and attachment.data:
            # 生成Base64编码的data URI
            base64_data = base64.b64encode(attachment.data).decode('utf-8')
            cid_map[attachment.cid.lower()] = f"data:{attachment.type};base64,{base64_data}"
    
    # 使用BeautifulSoup处理HTML
    soup = BeautifulSoup(html_body, 'html.parser')
    
    # 替换所有图片的CID引用为data URI
    for img in soup.find_all('img', src=True):
        cid_match = re.match(r'cid:(.+)', img['src'], re.IGNORECASE)
        if cid_match:
            cid = cid_match.group(1).lower()
            if cid in cid_map:
                img['src'] = cid_map[cid]
    
    # 生成最终HTML
    final_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Converted Email</title>
</head>
<body>
{soup.prettify()}
</body>
</html>"""
    
    # 保存到文件
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

# 使用示例
convert_msg_to_html('FWDEmailBody.msg', 'FWDEmailBody.html')