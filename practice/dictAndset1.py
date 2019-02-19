#dict
#字典，全称dictionary。其他语言中成为map，使用键-值（key-value）存储，具有极快的查找速度
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d['Michael'])
#通过key把数据放入dict
d['Adam'] = 67
print(d)
#由于一个key只能对应一个value，所以，多次对一个key放入value，后面的值会把前面的值冲掉：
d['Jack'] = 90
print(d)
d['Jack'] = 99
print(d)
#如果key不存在，dict就会报错：
#print(d['Thomas'])
#判断key是否存在
#第一种：通过in判断key是否存在
print('Thomas' in d)
#第二种：通过dict提供的get()方法，如果key不存在，可以返回None，或者自己指定的value
print(d.get('Thomas'))
print(d.get('Thomas',-1))
#要删除一个key，用pop(key)方法，对应的value也会从dict中删除
d.pop('Bob')
print(d)
#总结：dict是用空间来换取时间的一种方法。dict的key必须是不可变对象，比如字符串、整数等。

#set
#set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。
#要创建一个set，需要提供一个list作为输入集合
s = set([1, 2, 3])
print(s) #{1, 2, 3}
#重复元素在set中自动被过滤：
s = set([1, 1, 2, 2, 3, 3])
print(s)
#通过add(key)方法可以添加元素到set中，可以重复添加，但不会有效果：
s.add(4)
print(s)
s.add(4)
print(s)
#通过remove(key)方法可以删除元素
s.remove(4)
print(s)
#set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作：
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
print(s1 & s2) #{2, 3}
print(s1 | s2) #{1, 2, 3, 4}
#不可以放入可变对象
#s = set([[1,2],2,3])
#print(s)

#对于不变对象来说，调用对象自身的任意方法，也不会改变该对象自身的内容。相反，这些方法会创建新的对象并返回，这样，就保证了不可变对象本身永远是不可变的。
a = 'abc'
a.replace('a', 'A')
print(a) #abc
a = 'abc'
b=a.replace('a', 'A')
print(a) #abc
print(b) #Abc

a = set([(1, 2, 3),2,3])
print(a)
