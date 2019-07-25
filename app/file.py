import os
import re
import time

import pandas as pd
from flask import request, flash
import numpy as np

from app import app
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from pandas.api.types import is_numeric_dtype

class file(object):

    def __init__(self):
        self.date = time.strftime("%Y-%m-%d",time.localtime())
        self.read_swt = self.read()

    def allowed_file(self,filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def upload(self, dirs):
        for dr in dirs:
            newdir = os.path.join(app.config['UPLOAD_FOLDER'], dr+'/')
            if os.path.isdir(newdir):
                file = request.files.get(dr)
                if file and self.allowed_file(file.filename):
                    filename = dr + '_' + self.date + '.' + file.filename.rsplit('.', 1)[1]
                    file.save(os.path.join(newdir, filename))
            else:
                os.mkdir(newdir)

    def walk(self, dirs):
        dt = {}
        for dr in dirs:
            newdir = os.path.join(app.config['UPLOAD_FOLDER'], dr+'/')
            if os.path.isdir(newdir):
                dt[dr] = os.listdir(newdir)
            else:
                os.mkdir(newdir)
        return dt
    def if_file(self,name):
        #
        filepath = UPLOAD_FOLDER + name+'/'
        if os.listdir(filepath):
            return UPLOAD_FOLDER + name+'/' + os.listdir(filepath)[0]
        else:
            #flash(name + '文件找不到')
            return "none"
        #return filepath
    def read(self):
        oldfile = self.if_file('swt')
        if oldfile != "none":
            xlsx = pd.ExcelFile(oldfile)
            df = pd.read_excel(xlsx, 'sheet1', usecols="D,E,F,G", skiprows=[0, 1, 2], names=['D', 'E', 'F', 'G'])
            df['engine'] = df.apply(self.what_engine, axis=1)
            df['zhuan'] = df.apply(self.is_zhuan, axis=1)
            df['account'] = df.apply(self.what_account, axis=1)
            #newdf = df.groupby('engine').agg({'D':'size','zhuan':'sum'})
            newdf = df.groupby('account').agg({'D': 'size', 'zhuan': 'sum'})
            account = ['xa-lhszyy','xa-qlx','xa-lhyy','xa-lhxm','xa-lhyy66','xa-lhqg','cm_029866a@sohu.com','cm_120sxnk@sohu.com','cm_nkywyy@sohu.com','xa-zhifk','xa-shengfk','xa-shengzhi','莲湖生殖妇科1','莲湖生殖妇科','美柚']
            for ac in account:
                if ac not in newdf.index:
                    newdf.loc[ac] = [0,0]
            newdf.loc['商务通汇总'] = newdf[['D','zhuan']].apply(lambda x: x.sum())
            print(newdf)
            return newdf
        else:
            return "no"

    def is_zhuan(self,data):
        zc = str(data['G'])
        if '转' in zc:
            return 1
    def what_engine(self, data):
        eg = str(data['D'])
        if 'ada.baidu.com' in eg:
            return '百度'
        elif 'sg5g.' in eg or 'sogou.com' in eg:
            return '搜狗'
        elif 'smfuke.' in eg:
            return '神马'
        elif 'A360' in eg or 'B360' in eg:
            return '360'
        elif 'meiyou' in eg:
            return '美柚'
        else:
            return 'nan'
    def what_account(self, data):
        eg = str(data['D'])
        if '&A-' in eg:
            return 'xa-lhszyy'
        if '&B-' in eg:
            return 'xa-qlx'
        if '&C-' in eg:
            return 'xa-lhyy'
        if 'bd-yd&D-' in eg:
            return 'xa-lhxm'
        if '&E-' in eg:
            return 'xa-lhyy66'
        if '&F-' in eg:
            return 'xa-lhqg'
        if 'sg5g.02989391155.com' in eg or 'sogou.com' in eg:
            return 'cm_029866a@sohu.com'
        if 'sg5g.xaszfkyy.com' in eg:
            return 'cm_120sxnk@sohu.com'
        if 'sg5g.xaszyyfk.com' in eg:
            return 'cm_nkywyy@sohu.com'
        if 'smfuke.sxmnzkyy.com' in eg:
            return 'xa-zhifk'
        if 'smfuke.ywzxyy120.com' in eg:
            return 'xa-shengfk'
        if 'smfuke.nkywyy120.com' in eg:
            return 'xa-shengzhi'
        if 'B360' in eg:
            return '莲湖生殖妇科1'
        if 'A360' in eg:
            return '莲湖生殖妇科'
        if 'meiyou.' in eg:
            return '美柚'

    def read_baidu(self):
        oldfile = UPLOAD_FOLDER + 'baidu/' + 'baidu.csv'
        #xlsx = pd.ExcelFile(oldfile)
        df = pd.read_csv(oldfile, encoding="GB2312", skiprows=7, usecols=[0,2,3,4,5])
        df['展现'] = pd.to_numeric(df['展现'], errors='coerce')
        df['点击'] = pd.to_numeric(df['点击'], errors='coerce')
        df['消费'] = pd.to_numeric(df['消费'], errors='coerce')
        print("****百度****")
        newdf = df.groupby('账户',as_index=False).agg({'展现':np.sum,'点击':np.sum,'消费':np.sum})
        newdf[['对话', '转出']] = newdf.apply(self.newcols, args=('账户',), axis=1)
        newdf.loc['百度汇总'] = newdf[['展现', '点击','消费','对话', '转出']].apply(lambda x: x.sum())
        newdf = newdf.fillna(0)
        return newdf

    def read_sogou(self):
        oldfile = UPLOAD_FOLDER + 'sogou/' + 'sogou.csv'
        df = pd.read_csv(oldfile, encoding="GB2312", skiprows=[1], usecols=[2,3,4,5,6],names=['账户','计划','消费', '点击','展现'])
        df = df[~df['账户'].str.contains('账户')]
        df = df[~df['账户'].str.contains('--')]
        #print(df)
        df['展现'] = pd.to_numeric(df['展现'], errors='coerce')
        df['点击'] = pd.to_numeric(df['点击'], errors='coerce')
        df['消费'] = pd.to_numeric(df['消费'], errors='coerce')
        #print("****搜狗****")
        newdf = df.groupby('账户',as_index=False).agg({'展现':np.sum,'点击':np.sum,'消费':np.sum})
        newdf[['对话', '转出']] = newdf.apply(self.newcols, args=('账户',), axis=1)
        newdf.loc['搜狗汇总'] = newdf[['展现', '点击','消费','对话', '转出']].apply(lambda x: x.sum())
        newdf = newdf.fillna(0)
        print(newdf)
        return newdf

    def read_shenma(self):
        oldfile = UPLOAD_FOLDER + 'shenma/' + 'shenma.csv'
        df = pd.read_csv(oldfile, encoding="GB2312", skiprows=0, usecols=[1,2,3,4,5],names=['账户','计划','展现','点击','消费'])
        df = df[~df['账户'].str.contains('账户')]
        df['展现'] = pd.to_numeric(df['展现'], errors='coerce')
        df['点击'] = pd.to_numeric(df['点击'], errors='coerce')
        df['消费'] = pd.to_numeric(df['消费'], errors='coerce')
        print("****神马****")
        newdf = df.groupby('账户',as_index=False).agg({'展现':np.sum,'点击':np.sum,'消费':np.sum})

        newdf[['对话', '转出']] = newdf.apply(self.newcols,  args=('账户',), axis=1)
        newdf.loc['神马汇总'] = newdf[['展现', '点击','消费','对话', '转出']].apply(lambda x: x.sum())
        newdf = newdf.fillna(0)
        print(newdf)
        return newdf

    def read_360(self):
        oldfile = UPLOAD_FOLDER + '360/' + '360.csv'
        df = pd.read_csv(oldfile, encoding="GB2312", skiprows=0, usecols=[1,3,4,5,7],names=['账户','计划','展现','点击','消费'])
        df = df[~df['账户'].str.contains('推广账户')]
        df['展现'] = pd.to_numeric(df['展现'], errors='coerce')
        df['点击'] = pd.to_numeric(df['点击'], errors='coerce')
        df['消费'] = pd.to_numeric(df['消费'], errors='coerce')
        print("****360****")
        newdf = df.groupby('账户', as_index=False).agg({'展现':np.sum,'点击':np.sum,'消费':np.sum})
        newdf[['对话','转出']] = newdf.apply(self.newcols, args=('账户',), axis=1)
        newdf.loc['360汇总'] = newdf[['展现', '点击','消费','对话', '转出']].apply(lambda x: x.sum())
        newdf = newdf.fillna('0')
        print(newdf)
        return newdf

    def newcols(self,hang,index):
        swt = self.read_swt
        return swt.loc[hang[index]]



if __name__ == '__main__':
    f = file()
    #baidu = f.read_baidu()
    #sogou = f.read_sogou()
    #shenma = f.read_shenma()
    #d360 = f.read_360()
    #hz = pd.DataFrame([baidu.loc['百度汇总'],sogou.loc['搜狗汇总'],shenma.loc['神马汇总'],d360.loc['360汇总']])
    #hz.loc['大汇总'] = hz[['展现', '点击', '消费', '对话', '转出']].apply(lambda x: x.sum())
    #hz = hz.fillna('0')
    #print(hz)
    fm = f.if_file('swt')
    print(fm)
