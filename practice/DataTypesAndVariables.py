#字符串
print('I ame huangqin.')
#字符串中含单引号,可以用双引号括起来
print("I'm ok.")
#字符串中含单引号和双引号，可以使用转义符\来标识
print('I\'m \"ok\".')
#转义字符\可以转义很多字符，\n标示换行，\t表示制表符，\\标示转义\
print('I\'m leaning \nPython.')
print('\\\n\\')
#r''标示''中的字符串不转义
print('\\\t\\')
print(r'\\\t\\')
#'''...'''的格式表示多行内容
print('''line1
line2
line3''')

#布尔值 True、False，注意首字母大写
print(True)
print(False)
print(3>2)
print(3>5)
#布尔值可以用and、or和not运算
#and
print('True and True :',True and True)
print('True and False:',True and False)
print('False and True:',False and True)
print('False and False:',False and False)
#or
print('True or True:',True or True)
print('True or False',True or False)
print('False or True:',False or True)
print('False or False:',False or False)
#not
print ('not True:',not True)
print ('not False:',not False)
print ('not 1>2:',not 1>2)
#布尔值经常用在条件判断中
age = 15
if age >=18:
    print ('adult')
else:
    print ('teenager')

#空值：None

#变量
#变量名必须是大小写英文、数字和_的组合，且不能用数字开头
a = 1
t_007 = 'T007'
print ('a = ',a,'\nt_007 =',t_007)
#同一个变量可以反复赋值，而且可以是不同类型的变量
a = 123 # a是整数
print(a)
a = 'ABC' # a变为字符串
print(a)

#常量
#常量就是不能变的变量,通常用全部大写的变量名表示常量
PI = 3.14159265359

#整数的除法
#第一种：/
print ('10/3=',10/3) #3.3333333333333335
print ('9/3=',9/3) #3.0
#总结：/除法计算结果是浮点数，即使是两个整数恰好整除，结果也是浮点数
#第二种：//，称为地板除
print('10//3=',10//3) #3
#总结：整数的地板除//永远是整数，即使除不尽。要做精确的除法，使用/就可以。//除法只取结果的整数部分

#Python还提供一个余数运算，可以得到两个整数相除的余数
print ('10%3=',10%3) #1
#无论整数做//除法还是取余数，结果永远是整数，所以，整数运算结果永远是精确的。

n = 123
f = 456.789
s1 = 'Hello, world'
s2 = 'Hello, \'Adam\''
s3 = r'Hello, "Bart"'
s4 = r'''Hello,
Lisa!'''
print ('n=',n,'\nf=',f,'\ns1=',s1,'\ns2=',s2,'\ns3=',s3,'\ns4=',s4)


#Python支持多种数据类型，在计算机内部，可以把任何数据都看成一个“对象”，而变量就是在程序中用来指向这些数据对象的，对变量赋值就是把数据和变量给关联起来。
#对变量赋值x = y是把变量x指向真正的对象，该对象是变量y所指向的。随后对变量y的赋值不影响变量x的指向。
#注意：Python的整数没有大小限制，而某些语言的整数根据其存储长度是有大小限制的，例如Java对32位整数的范围限制在-2147483648-2147483647。
#Python的浮点数也没有大小限制，但是超出一定范围就直接表示为inf（无限大）。





