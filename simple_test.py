def trace(func):
    def wrapper(self, *args, **kwargs):
        print(f"在 wrapper 中，可以访问实例变量: {getattr(self, 'instance_var', '未找到')}")
        print(f"在 wrapper 中，可以访问类变量: {getattr(self, 'class_var', '未找到')}")
        return func(self, *args, **kwargs)

    return wrapper


class MyClass:
    class_var = "我是类变量"

    def __init__(self):
        self.instance_var = "我是实例变量"

    @trace
    def my_method(self):
        print("执行原始方法")


# 测试
obj = MyClass()
obj.my_method()
