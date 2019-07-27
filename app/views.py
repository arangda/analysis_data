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
    dt = f.walk(f.dirs)
    msg = "先上传商务通和各搜索引擎的导出数据"

    if request.method == 'POST':
        if request.form.get('analysis'):
            is_swt = True if dt['swt'][0] == f.error_exist else False
            if is_swt:
                msg = "没有商务通数据哦"
            else:
                return redirect(url_for('data'))
        elif request.form.get('upload'):
            f.upload(f.dirs)
            return redirect(url_for('index'))
    flash(msg)
    return render_template('index.html',
                           now=int(time.time()),
                           dt=dt
                           )




@app.route('/data', methods=['GET', 'POST'])
def data():
    f = file()
    dt = f.walk(f.dirs)
    is_swt = True if dt['swt'][0] == f.error_exist else False
    is_baidu = True if dt['baidu'][0] == f.error_exist else False
    is_sogou = True if dt['sogou'][0] == f.error_exist else False
    is_shenma = True if dt['shenma'][0] == f.error_exist else False
    is_360 = True if dt['360'][0] == f.error_exist else False
    #如果没有上传商务通表，则跳转首页
    if is_swt:
        return redirect(url_for('index'))
    else:
        dswt = f.read_swt
    #如果没有上传搜索引擎的表，则自定义一个dataframe
    if is_baidu:
        baidu = pd.DataFrame({'账户':'0','展现':0.0, '点击':0.0,'消费':0.0,'对话':0.0, '转出':0.0},index=['百度汇总'])
    else:
        baidu = f.read_baidu()

    if is_sogou:
        sogou = pd.DataFrame({'账户':'0','展现':0.0, '点击':0.0,'消费':0.0,'对话':0.0, '转出':0.0},index=['搜狗汇总'])
    else:
        sogou = f.read_sogou()

    if is_shenma:
        shenma = pd.DataFrame({'账户':'0','展现':0.0, '点击':0.0,'消费':0.0,'对话':0.0, '转出':0.0},index=['神马汇总'])
    else:
        shenma = f.read_shenma()

    if is_360:
        d360 = pd.DataFrame({'账户':'0','展现':0.0, '点击':0.0,'消费':0.0,'对话':0.0, '转出':0.0},index=['360汇总'])
    else:
        d360 = f.read_360()

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







