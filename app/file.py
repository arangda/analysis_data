import os
import re
import time

import pandas as pd
from flask import request, flash
import numpy as np

from app import app
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

class file(object):

    def __init__(self):
        # 下面列表和uploads中的子目录，及上传表单name值相关
        self.dirs = ['swt', 'baidu', 'sogou', 'shenma', '360']
        self.date = time.strftime("%Y-%m-%d",time.localtime())
        self.read_swt = self.read_swts()
        self.error_exist = '<em>文件不存在,请先上传文件</em>'
        self.timelist = []

    def allowed_file(self,filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def upload(self, dirs):
        for dr in dirs:
            newdir = os.path.join(UPLOAD_FOLDER, dr+'/')
            if os.path.isdir(newdir):
                file = request.files.get(dr)
                if file and self.allowed_file(file.filename):
                    if dr == 'swt' and file.filename.rsplit('.', 1)[1] != 'xls':
                        # flash("商务通表的后缀要为xls")
                        pass
                    elif dr != 'swt' and file.filename.rsplit('.', 1)[1] != 'csv':
                        # flash("搜索引擎表的后缀要为csv")
                        pass
                    else:
                        filename = dr + '.' + file.filename.rsplit('.', 1)[1]
                        file.save(os.path.join(newdir, filename))
                        self.is_right(newdir, filename, dr)

            else:
                os.mkdir(newdir)
        if len(set(self.timelist)) > 1:
            flash("各个表可能不是同一天的")

    def is_right(self,fdir,fname,dir):
        t = '00-00-00'
        fpath = os.path.join(fdir, fname)
        if dir == 'swt':
            df = pd.read_excel(fpath)
            stand = ['编号', '开始访问时间', '客人讯息数', '初次访问网址', '名称', '对话类型', '对话类别', '关键词', 'IP定位', 'IP']
            isright = set(stand).issubset(set(df.iloc[1].tolist()))
            if not isright:
                flash("你确定上传的表是商务通表吗？")
                os.remove(fpath)
            else:
                ptime = time.strptime(df.ix[2][1],"%Y/%m/%d %H:%M:%S")
                t = time.strftime("%Y-%m-%d",ptime)
                self.timelist.append(t)
        if dir == 'baidu':
            df = pd.read_csv(fpath,encoding="GB2312",skiprows=7)
            stand =['账户', '日期', '推广计划', '展现', '点击', '消费', '平均点击价格', '点击率', '网页转化', '电话转化', '商桥转化', '推广计划ID']
            isright = set(stand).issubset(set(df.columns.values.tolist()))
            if not isright:
                flash("你确定上传的表是百度报表吗？")
                os.remove(fpath)
            else:
                ptime = time.strptime(df.ix[0][1],"%Y-%m-%d")
                t = time.strftime("%Y-%m-%d",ptime)
                self.timelist.append(t)
        if dir == 'sogou':
            df = pd.read_csv(fpath,encoding="GB2312",skiprows=[1])
            stand =['编号', '日期', '账户', '推广计划', '消耗', '点击数', '展示数', '点击率', '点击均价', '有消耗词量']
            isright = set(stand).issubset(set(df.columns.values.tolist()))
            if not isright:
                flash("你确定上传的表是搜狗报表吗？")
                os.remove(fpath)
            else:
                ptime = time.strptime(df.ix[0][1].split("至")[0],"%Y-%m-%d")
                t = time.strftime("%Y-%m-%d",ptime)
                self.timelist.append(t)
        if dir == 'shenma':
            df = pd.read_csv(fpath,encoding="GB2312")
            stand =['时间', '账户', '推广计划', '展现量', '点击量', '消费', '点击率', '平均点击价格']
            isright = set(stand).issubset(set(df.columns.values.tolist()))
            if not isright:
                flash("你确定上传的表是神马报表吗？")
                os.remove(fpath)
            else:
                ptime = time.strptime(df.ix[0][0],"%Y/%m/%d")
                t = time.strftime("%Y-%m-%d",ptime)
                self.timelist.append(t)

        if dir == '360':
            df = pd.read_csv(fpath,encoding="GB2312")
            stand =['日期', '推广账户', '产品线', '推广计划', '展示次数', '点击次数', '点击率', '总费用', '平均每次点击费用']
            isright = set(stand).issubset(set(df.columns.values.tolist()))
            if not isright:
                flash("你确定上传的表是360报表吗？")
                os.remove(fpath)
            else:
                ptime = time.strptime(df.ix[0][0].split("至")[0].strip(),"%Y-%m-%d")
                t = time.strftime("%Y-%m-%d",ptime)
                self.timelist.append(t)

        filename = dir + '_' + t + '.' + fname.rsplit('.', 1)[1]
        newfpath = os.path.join(fdir,filename)
        os.rename(fpath,newfpath)

    def walk(self, dirs):
        dt = {}
        for dr in dirs:
            newdir = os.path.join(UPLOAD_FOLDER, dr+'/')
            if os.path.isdir(newdir):
                #此处子判断觉得也许可以更好解决
                if os.listdir(newdir):
                    dt[dr] = os.listdir(newdir)
                else:
                    dt[dr] = [self.error_exist]
            else:
                os.mkdir(newdir)
        return dt
    #读取每个文件前先判断是否存在
    def if_file(self,name):
        filepath = UPLOAD_FOLDER + name+'/'
        if os.listdir(filepath):
            file = UPLOAD_FOLDER + name+'/' + os.listdir(filepath)[0]
            return {"filepath":file}
        else:
            return {"error":"不存在这个文件"}
    def read_swts(self):
        res = self.if_file('swt')
        if 'filepath' in res:
            df = pd.read_excel(res['filepath'], sheet_name=0, usecols="D,E,F,G", skiprows=[0, 1, 2], names=['D', 'E', 'F', 'G'])
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
            return newdf
        else:
            return res


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
        res = self.if_file('baidu')
        df = pd.read_csv(res['filepath'], encoding="GB2312", skiprows=7, usecols=[0,2,3,4,5])
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
        res = self.if_file('sogou')
        df = pd.read_csv(res['filepath'], encoding="GB2312", skiprows=[1], usecols=[2,3,4,5,6],names=['账户','计划','消费', '点击','展现'])
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
        print(newdf.info())
        newdf = newdf.fillna(0)
        return newdf

    def read_shenma(self):
        res = self.if_file('shenma')
        df = pd.read_csv(res['filepath'], encoding="GB2312", skiprows=0, usecols=[1,2,3,4,5],names=['账户','计划','展现','点击','消费'])
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
        res = self.if_file('360')
        df = pd.read_csv(res['filepath'], encoding="GB2312", skiprows=0, usecols=[1,3,4,5,7],names=['账户','计划','展现','点击','消费'])
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
    #fm = f.read_swt
    #print(fm)
    f.upload(['baidu'])
