"""
上下文管理器的任务是：代码块执行前准备，代码块执行后收拾
"""
class open():
    def output(self):
        print("hello world")
    def __enter__(self):
        print("enter")
        return self  #可以返回任何希望返回的东西
    def __exit__(self,exception_type,value,trackback):
        print("exit")
        return False

with open() as p:
    p.output()
