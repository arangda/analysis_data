CSRF_ENABLED = True
SECRET_KEY = "YESIDO"

import os
basedir = os.path.abspath(os.path.dirname(__file__))


#上传xls设置
UPLOAD_FOLDER = os.path.join(basedir, 'uploads/')
ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])