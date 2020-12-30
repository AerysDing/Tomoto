from qiniu import Auth,put_data
from tomato import conf

def upload_to_qn(filepath,filename):
    qn_auth = Auth(conf.QN_ACCESSKEY,conf.QN_SECRETKEY)
    token = qn_auth.upload_token(conf.QN_BUCKET,filename,3600)
    #to upload
    put_data(token,filename,filepath)
    #joint url
    file_url = "%s/%s"%(conf.QN_BASE_URL,filename)
    return file_url

# upload_to_qn("222.jpg", "222.jpg")