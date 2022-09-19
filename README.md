

@[toc]

 ## 1、作业基本信息
|课程名称|[2020级软件工程课程学习](https://bbs.csdn.net/forums/gdut-ryuezh)|
|-- |:-- |
|作业要求|[第二次作业要求的链接](https://bbs.csdn.net/topics/608092799)|
|作业的目标|学习论文查重算法并实现|

 ## 2、项目网址
 + [软件工程第二次作业](https://github.com/Hopelht/3120002096)

 ## 3、PSP表格
|**PSP2.1**|Personal Software Process Stages|预估耗时（分钟）|实际耗时（分钟）|
|-- |:-- |:-- |:-- |
|Planning|计划|40|30|
|· Estimate|· 估计这个任务需要多少时间|40|30|
|Development|开发|700|900|
|· Analysis|· 需求分析 (包括学习新技术)|50|100|
|· Design Spec|· 生成设计文档|50|50|
|· Design Review|· 设计复审|200|200|
|· Coding Standard|· 代码规范 (为目前的开发制定合适的规范)|100|100|
|· Design|· 具体设计|100|200|
|· Coding|· 具体编码|100|150|
|· Code Review|· 代码复审|100|100|
|· Test|· 测试（自我测试，修改代码，提交修改）|100|100|
|Reporting|报告|60|50|
|· Test Repor|· 测试报告|20|10|
|· Size Measurement|· 计算工作量|20|20|
|· Postmortem & Process Improvement Plan|· 事后总结, 并提出过程改进计划|20|20|
||· 合计|800|980|

 ## 4、任务分析与实现流程

 ### 4.1、任务分析
 + 作业的核心任务：对文章进行查重，文章内容为中文或英文字符，计算文章内容相似度
 + 核心算法：simhash算法 + 海明距离
 + 使用语言与工具：python语言 + pycharm工具


 ### 4.2、算法原理
 #### 4.2.1、海明距离
 + 定义：在信息编码中，两个合法代码对应位上编码不同的位数称为码距，又称海明距离
 + 计算方法：计算海明距离，就是对两个位串进行异或（xor）运算，并计算出异或运算结果中1的个数。举例：10101和00110从第一位开始依次有第一位、第四、第五位不同，则海明距离为3。

 #### 4.2.2、simhash算法
+ SimHash是一种局部敏感hash，它是进行海量网页去重使用的主要算法。
主要过程：分词、Hash、加权、合并、降维（参考博客：[SimHash算法原理](https://blog.csdn.net/qq_33905939/article/details/105601848?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166359689316782391857492%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=166359689316782391857492&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-105601848-null-null.142%5Ev47%5Epc_rank_34_2,201%5Ev3%5Econtrol_1&utm_term=simhash%E7%AE%97%E6%B3%95&spm=1018.2226.3001.4187)）

+ 分词：
使用分词手段将文本分割成关键词的特征向量，即将文本文档进行分割成不同的词组，比如词1为：今天星期四，词2为：今天星期五，得出分词结果为【今天，星期四】【今天，星期五】。
假设分词结果如下：
> 12306 服务器 故障 车次 加载失败 购买 候补订单 支付 官方 消费者 建议 卸载 重装 切换网络 耐心 等待

+ Hash:
前面使用分词方法和权重分配将文本就分割成若干个带权重的实词，比如权重使用1-5的数字表示，1最低5最高，把原文本处理成如下:
> 12306(5) 服务器(4) 故障(4) 车次(4) 加载失败(3) 购买(2) 候补订单(4) 支付(2) 官方(2) 消费者(3) 建议(1) 卸载(3) 重装(3) 切换网络(2) 耐心(1) 等待(1)

接着通过hash函数对每一个词向量进行映射，产生一个n位二进制串，一般常用的位数为32、64、128。

+ 加权：
前面的计算已经得到了每个词向量的Hash串和该词向量对应的权重，接着计算权重向量W=hash*weight。具体的计算过程如下：
hash二进制串中为1的，w = 1 * weight，二进制串中为0的，w = weight * -1
例如：12306的带权重哈希值为 [5 -5 -5 5 5 5 -5 -5]


+ 合并：
前面计算出了文本分词之后每一个特征词的权重向量，接着，把文本所有词向量的权重向量相累加，得到一个新的权重向量，则假设的最终结果为 [18 9 -6 -9 22 -35 12 -5]

+ 降维：
 前面合并后得到的文本的权重向量，大于0的位置1，小于等于0的位置0，就可以得到该文本的SimHash值，上面提到的 [18 9 -6 -9 22 -35 12 -5] 可以得到 [1 1 0 0 1 0 1 0] 这个bit串，这个bit串即可用于海明距离计算。

 ### 4.3、实现流程
 
 #### 4.3.1、流程图
 ![在这里插入图片描述](https://img-blog.csdnimg.cn/73bfbbe55098442a83d74314e7bd76ff.png)

 #### 4.3.2、关键模块
+ simhash算法

```python
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

```


+ 计算海明距离得出相似度

```python
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


```


 ## 5、性能分析
+ 使用pycharm自带的profile功能进行性能分析。（参考博客：[Pycharm图形化性能测试工具Profile](https://blog.csdn.net/Castlehe/article/details/118088763?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166360247316782417072897%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=166360247316782417072897&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-118088763-null-null.142%5Ev47%5Epc_rank_34_2,201%5Ev3%5Econtrol_1&utm_term=pycharm%20profile&spm=1018.2226.3001.4187)）
![在这里插入图片描述](https://img-blog.csdnimg.cn/3a541219e8b84b7cafb8e643662815c2.png)![在这里插入图片描述](https://img-blog.csdnimg.cn/42fc514bf0494ff2862b530dac394a41.png)

+ 性能改进：从图中可以看出对内存和运行时间占用较大的是调用jieba库进行分词阶段，因此splitWords()函数中将直接分词改进为先用正则表达式匹配过滤再分词
+ 原始代码：
```python
# 原分词方法
def splitWords(text):
    with open(text, 'r', encoding='UTF-8') as f1:
        f2 = f1.read()
    f1.close()
    length = len(list(jieba.lcut(f2)))
    string = jieba.analyse.extract_tags(f2, topK=length)
    return string
```
 +  改进代码：

```python
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
```




 ## 6、单元测试

 ### 6.1、单元测试结果
 + 对5个抄袭文件的相似度进行测试，测试的结果如下图所示，结果保存在test_save.txt文件中


![在这里插入图片描述](https://img-blog.csdnimg.cn/bae0b009edce44919132088270c57a5f.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/1b03dc15c44a4f588059ce67b3aef80e.png)


 ### 6.2、测试覆盖率
 + 使用coverage命令行进行覆盖率测试和数据导出
![在这里插入图片描述](https://img-blog.csdnimg.cn/2a094a8915ee4612bde26c98da372723.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/570016e505774b8880e3bc13e2b865dc.png)


 ## 7、异常处理
 ### 7.1、路径不存在
+ 文件需要按题目要求使用命令行输入完整的绝对路径，答案文件是写入文件，代码中使用了'a'模式，不存在会自动生成
![在这里插入图片描述](https://img-blog.csdnimg.cn/30d052f171f445cb88a71f60671ac1f8.png)例如：路径不存在导致异常
![在这里插入图片描述](https://img-blog.csdnimg.cn/ae62e7dc901a4ae7afd3286a385e1a13.png)


 ### 7.2、使用cmd命令行运行正确的虚拟环境
 + 使用cmd命令行进行文件运行的时候务必要进入正确的虚拟环境，在完成作业的过程使用中，我使用pycharm根据requirements.txt文件生成项目自己的虚拟环境，但是在cmd中使用命令行运行时会有"No module named 'jieba' "的报错，原因时cmd一开始调用的是python自带的环境，不存在jieba库，因此无论是使用anaconda还是pycharm生成的虚拟环境，运行时务必要进入正确的环境
![在这里插入图片描述](https://img-blog.csdnimg.cn/659c3939450c4b8c971d35d46c258fc0.png)python生成requirements.txt命令行：
```
pip freeze > requirements.txt
```

