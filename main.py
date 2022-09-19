# -*- codeing = utf-8 -*-
# @Time : 2022/9/17 20：00
# @Author : 丁冠智
# @File : main.py
# @Software : PyCharm
import os
import re
import jieba
import jieba.analyse
import eventlet
import hashlib
import json
import sys
import time


# 分词
def splitWords(path):
    with open(path, 'r', encoding='UTF-8') as f1:
        f2 = f1.read()
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")  # 对无关字符进行过滤
    _string = pattern.sub("", f2)
    f1.close()
    length = len(list(jieba.lcut(_string)))     # length为分词后词的个数
    string = jieba.analyse.extract_tags(_string, topK=length)  # 提取主题词进行分组
    return string

# # 原分词方法
# def splitWords(text):
#     with open(text, 'r', encoding='UTF-8') as f1:
#         f2 = f1.read()
#     f1.close()
#     length = len(list(jieba.lcut(f2)))
#     string = jieba.analyse.extract_tags(f2, topK=length)
#     return string


# simhash算法
def getSimh(string):
    i = 0
    weight = len(string)  # 权重维度
    fv = [0] * 128  # 计算特征向量

    #hash计算
    for word in string:  # 计算各个特征向量的hash值
        m = hashlib.md5()  # 生成一个md5加密算法对象
        m.update(word.encode("utf-8"))
        hashc = bin(int(m.hexdigest(), 16))[2:]  # 获取加密后的二进制字符串，并去掉开头的'0b'
        if len(hashc) < 128:  # hash值需在低位以0补齐128位
            dif = 128 - len(hashc)
            for tmp in range(dif):
                hashc += '0'

        # 加权
        for j in range(len(fv)):  # 给所有特征向量进行加权
            # 合并
            if hashc[j] == '1':  # 合并特征向量的加权结果
                fv[j] += (10 - (10 * i / weight))
            else:
                fv[j] -= (10 - (10 * i / weight))
        i += 1
    # 降维
    simhv = ''
    for k in range(len(fv)):
        if fv[k] >= 0:  # 对于n-bit累加结果，大于0则置1，否则置0
            simhv += '1'
        else:
            simhv += '0'

    return simhv  # simh值


# 计算海明距离得出相似度
def getSimilarity(simhv1, simhv2):
    # 计算海明距离
    d = 0
    if len(simhv1) != len(simhv2):
        d = -1
    else:
        for i in range(len(simhv1)):
            if simhv1[i] != simhv2[i]:
                d += 1

    similarity = 0.01 * (100 - d * 100 / 128)   # 计算相似度
    return similarity


def test():
    path1 = ','.join(sys.argv[1:2])  # 获取命令行参数 将列表转换为字符串
    path2 = ','.join(sys.argv[2:3])
    path3 = ','.join(sys.argv[3:])
    if not os.path.exists(path1):
        print("论文原文不存在！请重新使用命令行输入")
        exit()
    if not os.path.exists(path2):
        print("抄袭论文不存在！请重新使用命令行输入")
        exit()
    simhash1 = getSimh(splitWords(path1))
    simhash2 = getSimh(splitWords(path2))
    s1 = getSimilarity(simhash1, simhash2)
    s2 = round(s1, 2)  # 精确到小数点后两位
    print('文章相似度为:%f' % s2)
    with open(path3, 'a', encoding='utf-8')as f:  # 将结果写入指定路径path3
        f.write(path2 + '与原文的相似度为：')
        f.write(json.dumps(s2, ensure_ascii=False) + '\n')
    return s2


if __name__ == '__main__':
    test()
