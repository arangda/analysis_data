import asyncio
import sys
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import time
from flask import render_template, flash, redirect, g, url_for, session, request, jsonify


from app import app
import pandas as pd
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from .file import file

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    f = file()
    # 下面列表和uploads中的子目录，及上传表单name值相关
    dirs = ['swt', 'baidu', 'sogou', 'shenma', '360']
    dt = f.walk(dirs)
    if request.method == 'POST':
        f.upload(dirs)
        return redirect(url_for('index'))

    return render_template('index.html',
                           now=int(time.time()),
                           dt=dt
                           )




@app.route('/data', methods=['GET', 'POST'])
def data():
    f = file()
    baidu = f.read_baidu()
    sogou = f.read_sogou()
    shenma = f.read_shenma()
    d360 = f.read_360()
    dswt = f.read_swt
    hz = pd.DataFrame([baidu.loc['百度汇总'],sogou.loc['搜狗汇总'],shenma.loc['神马汇总'],d360.loc['360汇总']])
    hz.loc['大汇总'] = hz[['展现', '点击', '消费', '对话', '转出']].apply(lambda x: x.sum())
    hz = hz.fillna('0')
    return render_template('data.html',
                           now=int(time.time()),
                           baidu=[baidu.to_html(classes='data')],
                           sogou=[sogou.to_html(classes='data')],
                           shenma=[shenma.to_html(classes='data')],
                           d360=[d360.to_html(classes='data')],
                           dhz=[hz.to_html(classes='data')]
                           )
@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500







