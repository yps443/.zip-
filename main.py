import threading
import queue
import time
import zipfile
import itertools

# 执行测试
def run_test(q, zf):
    global wover
    count=0
    while True:
        if not q.empty():
            password = q.get()
            try:
                count+=1
                zf.extractall(pwd=password.encode("utf8"))
                print('\n 密码 = ' + password + '\n')
                q.queue.clear()
                wover = True
            except Exception as e:
                if count%1000==0:
                    # 输出测试
                    print(threading.current_thread().name+' 测试密码： '+password)
                pass
            q.task_done()  # 处理完成
        elif wover:
            break
        else:
            time.sleep(0.2)

# 是否等待结束
wover = False
# 创建字典
def create_dictionary(q):
    global wover#将wover变为全局变量
    time.sleep(2)
    li = [chr(i) for i in range(ord("0"), ord("9")+1)] + \
       [chr(i) for i in range(ord("a"), ord("z")+1)] + \
    [chr(i) for i in range(ord("A"), ord("Z")+1)]
    try:
        wei1, wei2 = map(int, input("位数之间请加空格分隔 数字空格数字").split())
    except:
        print("请检查，再来一遍吧")
        wei1, wei2 = map(int, input("位数之间请加空格分隔 数字空格数字").split())
    else:
        print("你输入的是" + str(wei1) + "位至" + str(wei2) + "位")
        YN = input("输入Y开始破解awa")
        if YN == "Y":
            print(li)
            print("线程名", threading.current_thread().name)
            for i in range(wei1, wei2):# 密码可能的长度，这里设置的3位到7位
                for s in itertools.product(li, repeat=i):
                    if wover == True:
                        return
                    ps = "".join(list(s))
                    q.put(ps)
            wover = True

def main():
    zf = zipfile.ZipFile(r"test.zip")#这里修改文件名
    threadlist = []
    # 创建队列
    q = queue.Queue()  # 不传MaxSize
    qlen = 0  # 记录队列长度
    # 异步生成字典
    threadlist.append(threading.Thread(
        target=create_dictionary, args=(q,), name="create0"))
    for x in range(0, 11):  # <=== 运行的线程数量
        th = threading.Thread(target=run_test, args=(q, zf,))
        threadlist.append(th)
    # 运行并加入等待运行完成
    for t in threadlist:
        t.start()
    for t in threadlist:
        t.join()

if __name__ == '__main__':
    print("运行开始了,请输入密码大概的位数")
    main()
    print("结束")
