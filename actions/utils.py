import re

def isHangul(text):
    if re.search('[가-힣]',text) is not None:
        return True
    else:
        return False

