CSRF_ENABLED = True
SECRET_KEY = "YESIDO"

import os
basedir = os.path.abspath(os.path.dirname(__file__))


#上传xls设置
UPLOAD_FOLDER = os.path.join(basedir, 'uploads/')
ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])

JIHUA = {
    'baidu':
    {
        'HY': '妇科计划',
        'PP': '品牌词',
        'RL': '人流',
        'YC': '引产',
        'YL': '药流',
        'YZ': '炎症',
        'SMZX': '私密整形',
        'XB': '性病',
        'BYBY': '不孕不育',
        'YJ': '月经',
        'FKJC': '检查',
        'JP': '公立医院竞品词',
        'ZY': '早孕',
        'GWY': '宫外孕',
        'GJ': '子宫、宫颈疾病',
        'SQH': '上取环',
        'QT': '其他',
        'ZXC': '中性医院词',
        'CX': '出血',
        'BD': '白带'
    },
    'sogou':
    {
        'HY': '妇科计划',
        'PP': '品牌词',
        'RL': '人流',
        'YC': '引产',
        'YL': '药流',
        'YZ': '炎症',
        'SMZX': '私密整形',
        'XB': '性病',
        'BYBY': '不孕不育',
        'YJ': '月经',
        'FKJC': '检查',
        'JP': '公立医院竞品词',
        'ZY': '早孕',
        'GWY': '宫外孕',
        'GJ': '子宫、宫颈疾病',
        'SQH': '上取环',
        'QT': '其他',
        'ZXC': '中性医院词',
        'CX': '出血',
        'BD': '白带'
    },
    'shenma':
    {
        'HY': '妇科计划',
        'PP': '品牌词',
        'RL': '人流',
        'YC': '引产',
        'YL': '药流',
        'YZ': '炎症',
        'SMZX': '私密整形',
        'XB': '性病',
        'BYBY': '不孕不育',
        'YJ': '月经',
        'FKJC': '检查',
        'JP': '公立医院竞品词',
        'ZY': '早孕',
        'GWY': '宫外孕',
        'GJ': '子宫、宫颈疾病',
        'SQH': '上取环',
        'QT': '其他',
        'ZXC': '中性医院词',
        'CX': '出血',
        'BD': '白带'
    },
    '360':
    {
        'HY': '妇科计划',
        'PP': '品牌词',
        'RL': '人流',
        'YC': '引产',
        'YL': '药流',
        'YZ': '炎症',
        'SMZX': '私密整形',
        'XB': '性病',
        'BYBY': '不孕不育',
        'YJ': '月经',
        'FKJC': '检查',
        'JP': '公立医院竞品词',
        'ZY': '早孕',
        'GWY': '宫外孕',
        'GJ': '子宫、宫颈疾病',
        'SQH': '上取环',
        'QT': '其他',
        'ZXC': '中性医院词',
        'CX': '出血',
        'BD': '白带'
    }
}