#list
# 列表，有序集合，可添加删除（可变）
# 列出班里所有同学的名字：
classmates = ['Michael', 'Bob', 'Tracy']
print (classmates)
#用len()函数可以获得list元素的个数
print ('list 中元素个数：',len(classmates))
#用索引来访问list中每一个位置的元素，索引从0开始
print ('list 中第一个元素：',classmates[0])
print ('list 中第二个元素：',classmates[1])
print ('list 中第三个元素：',classmates[2])
#当索引超出了范围时，Python会报一个IndexError错误
#print ('list 中第四个元素：',classmates[3])
#最后一个元素的索引是len(classmates) - 1
print ('list 中最后一个元素1：',classmates[len(classmates) - 1])
#负数做索引
# -1 标示最后一个
print ('list 中最后一个元素2：',classmates[-1])
#以此类推，-2标示倒数第2个，-3标示倒数第3个：
print ('list 中倒数第2个元素：',classmates[-2])
print ('list 中倒数第3个元素：',classmates[-3])
#往list中追加元素到末尾，append()
classmates.append('Adam')
print ('追加一个元素后的classmates：',classmates)
#把元素插入到指定的位置，比如索引号为1的位置,insert
classmates.insert(1, 'Jack')
print ('索引号为1的位置追加一个元素后的classmates：',classmates)
#删除list末尾的元素，用pop()方法
classmates.pop()
print ('删除末尾元素后的classmates：',classmates)
#删除指定位置的元素，用pop(i)方法，其中i是索引位置
classmates.pop(1)
print ('删除索引号为1的位置的元素后的classmates：',classmates)
#把某个元素替换成别的元素，可以直接赋值给对应的索引位置
classmates[1] = 'Sarah'
print ('替换后的classmates：',classmates)
#list里面的元素的数据类型也可以不同
L = ['Apple', 123, True]
print ('拥有不同类型元素的list：',L)
#list元素也可以是另一个list(类似二维数组)
s = ['python', 'java', ['asp', 'php'], 'scheme']
print ('list中含list：',s)
#获取list中list中的元素，比如s中的'asp'
print (s[2][0])

#tuple
#元组，有序列表，不能修改
classmates = ('Michael', 'Bob', 'Tracy')
#空tuple
t = ()
#定义一个只有1个元素的tuple
#错误的定义
t = (1) #是1这个数！这是因为括号()既可以表示tuple，又可以表示数学公式中的小括号，这就产生了歧义，因此，Python规定，这种情况下，按小括号进行计算，计算结果自然是1
#正确的定义
t = (1,) #只有1个元素的tuple定义时必须加一个逗号,，来消除歧义


