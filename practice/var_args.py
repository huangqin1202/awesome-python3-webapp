#函数的参数
#除了正常定义的必选参数外，还可以使用默认参数、可变参数和关键字参数，使得函数定义出来的接口，不但能处理复杂的参数，还可以简化调用者的代码。
#位置参数(传入的两个值按照位置顺序依次赋给参数)
#计算x平方的函数
def power(x):
    return x * x
print(power(2))
#计算x的n次方
def power(x,n):
    s= 1
    while n>0:
        n = n-1
        s = s*x
    return s
print(pow(2,3))
#print(power(2))

#默认参数(最大的好处是能降低调用函数的难度。)
def power(x,n=2):
    s= 1
    while n>0:
        n = n-1
        s = s*x
    return s
print(power(5))
print(power(5,2))
print(power(5,3))
#默认参数可以简化函数的调用
#一年级小学生注册的函数，需要传入name和gender两个参数：
def enroll(name,gender):
    print('name:',name)
    print('gender:', gender)
print(enroll('huangqin','F'))

#如果要继续传入年龄,可以把年龄和城市设为默认参数：
def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)
print(enroll('huangqin','F'))
#默认参数不符的学生才需要提供额外的信息
print(enroll('huangqin','F',city='HuBei'))
#默认参数必须指向不变对象！
def add_end(L=[]):
    L.append('END')
    return L
print(add_end([1, 2, 3])) #[1, 2, 3, 'END']
print(add_end())#['END']
print(add_end())#['END', 'END']
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
print(add_end())#['END']
print(add_end())#['END']
#可变参数
#传入的参数个数是可变的(在参数前面加了一个*号)
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc(1,2,3))
print(calc(1,2,3,4))
#Python允许你在list或tuple前面加一个*号
nums = [1, 2, 3]
print(calc(*nums))
#关键字参数
#关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
print(person('Michael', 30))#name: Michael age: 30 other: {}
print(person('Bob', 35, city='Beijing'))#name: Bob age: 35 other: {'city': 'Beijing'}
print(person('Adam', 45, gender='M', job='Engineer'))#name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
extra = {'city': 'Beijing', 'job': 'Engineer'}
print(person('Jack', 24, **extra))
#命名关键字参数
#限制关键字参数的名字
#只接收city和job作为关键字参数
def person(name, age, *, city, job):
    print(name, age, city, job)
print(person('Jack', 24, city='Beijing', job='Engineer'))
#参数组合
#在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，这5种参数都可以组合使用
#参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def product(*x):
    s = 1
    for n in x:
        s = s * n
    return s
print('test:',product())


#总结：
#默认参数一定要用不可变对象，如果是可变对象，程序运行时会有逻辑错误！
#*args是可变参数，args接收的是一个tuple；
#**kw是关键字参数，kw接收的是一个dict。
#可变参数既可以直接传入：func(1, 2, 3)，又可以先组装list或tuple，再通过*args传入：func(*(1, 2, 3))；
#关键字参数既可以直接传入：func(a=1, b=2)，又可以先组装dict，再通过**kw传入：func(**{'a': 1, 'b': 2})。
#使用*args和**kw是Python的习惯写法，当然也可以用其他参数名，但最好使用习惯用法。
#命名的关键字参数是为了限制调用者可以传入的参数名，同时可以提供默认值。
#定义命名的关键字参数在没有可变参数的情况下不要忘了写分隔符*，否则定义的将是位置参数。