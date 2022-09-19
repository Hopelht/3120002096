import json
import os
import unittest
from main import getSimh, splitWords, getSimilarity


# 为了方便测试,重新写了一个路径处理函数,可以直接用pycharm运行
def test():
    path1 = input("请输入论文原文的路径：")
    path2 = input("请输入抄袭论文的路径：")
    if not os.path.exists(path1):
        print("论文原文不存在！请重新输入")
        exit()
    if not os.path.exists(path2):
        print("抄袭论文不存在！请重新输入")
        exit()
    path3 = 'test_save.txt'
    simhash1 = getSimh(splitWords(path1))
    simhash2 = getSimh(splitWords(path2))
    s1 = getSimilarity(simhash1, simhash2)
    s2 = round(s1, 2)
    print('文章相似度为:%f' % s2)
    with open(path3, 'a', encoding='utf-8')as f:
        f.write(path2 + '与原文的相似度为：')
        f.write(json.dumps(s2, ensure_ascii=False) + '\n')
    return s2




class MyTestCase(unittest.TestCase):   # 单元测试
    def test_something1(self):
        self.assertEqual(test(), 0.7)

if __name__ == '__main__':
    unittest.main()
