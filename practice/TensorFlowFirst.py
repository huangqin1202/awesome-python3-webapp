#引入tensorflow模块
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
a = tf.constant(10)
b = tf.constant(32)
print(sess.run(a+b))

matrix1 = tf.constant([[3.,3.]])
matrix2 = tf.constant([[2],[2.]])
product = tf.matmul(matrix1,matrix2)
sess = tf.Session()
result = sess.run(product)
print(result)
sess.close()


with tf.Session() as sess:
    result = sess.run([product])
    print(result)

sess = tf.InteractiveSession()
x = tf.Variable([1.0,2.0])
a = tf.constant([3.0,3.0])
x.initializer.run()
def sub(x,y):
    return x-y
sub = sub(x,a)
print(sub.eval())


#创建一个变量，初始化为标量0
state = tf.Variable(0,name="counter")
#创建一个op，其作用是使state增加1
one = tf.constant(1)
new_value = tf.add(state,one)
update = tf.assign(state,new_value)
#启动图后，变量必须先经过‘初始化’(init) op初始化，首先必须增加一个‘初始化’op到图中
init_op = tf.initialize_all_variables()
#启动图，运行op
with tf.Session() as sess:
    #运行'init'op
    sess.run(init_op)
    #打印'state'的初始值
    print(sess.run(state))
    #运行op，更新‘state’，并打印‘state’
    for _ in range(3):
        sess.run(update)
        print(sess.run(state))

#创建一个整形常量，即0阶Tensor
t0 = tf.constant(3,dtype=tf.int32)
#创建一个浮点数的一维数组，即1阶Tensor
t1 = tf.constant([3.,4.1,5.2],dtype=tf.float32)
#创建一个字符串的2x2数组，即2阶Tensor
t2 = tf.constant([['Apple','Orange'],['Potato','Tomato']],dtype=tf.string)
#创建一个2x3x1数组，即3阶张量，数据类型默认为整型
t3 = tf.constant([[[5],[6],[7]],[[4],[3],[2]]])
print('t0 = ',t0)
print('t1 = ',t1)
print('t2 = ',t2)
print('t3 = ',t3)
#print 一个 Tensor 只能打印出它的属性定义，并不能打印出它的值，要想查看一个 Tensor 中的值还需要经过Session 运行一下：
sess = tf.Session()
print('t0 = ',sess.run(t0))
print('t1 = ',sess.run(t1))
print('t2 = ',sess.run(t2))
print('t3 = ',sess.run(t3))

#tf.constant()创建Tensor常量
#创建两个常量节点
node1 = tf.constant(3.2)
node2 = tf.constant(4.8)
#创建一个adder节点，对上面两个节点执行+操作
adder = node1 + node2
#打印adder节点
print('adder节点:',adder)
#打印adder运行后的结果
sess = tf.Session()
print('adder运行后的结果:',sess.run(adder))

#使用tf.placeholder创建占位Tensor
#创建两个占位Tensor节点
a = tf.placeholder(tf.float32)
b = tf.placeholder(tf.float32)
#创建一个adder节点，对上面两个节点执行+操作
adder_node = a + b
#打印三个节点
print(a)
print(b)
print(adder_node)
# 运行一下，后面的 dict 参数是为占位 Tensor 提供输入数据
sess = tf.Session()
print(sess.run(adder_node,{a:3,b:4.5}))
print(sess.run(adder_node,{a:[1,3],b:[2,4]}))
#添加x操作
add_and_triple = adder_node*3
print(sess.run(add_and_triple,{a:3,b:4.5}))

#tf.Variable()可以创建一个变量 Tensor
#创建变量W和b节点，并设置初始值
W = tf.Variable([.1],dtype=tf.float32)
b = tf.Variable([-.1],dtype=tf.float32)
#创建x节点，用来输入实验中的输入数据
x = tf.placeholder(tf.float32)
#创建线性模型
linear_model = W*x + b
#创建y节点，用于输入实验中得到的输出数据，用于损失模型计算
y = tf.placeholder(tf.float32)
#创建损失模型
loss = tf.reduce_sum(tf.square(linear_model-y))
#创建Session用来计算模型
sess = tf.Session()
#初始化变量
init = tf.global_variables_initializer()
sess.run(init)
print(sess.run(W))
#用上面对W和b设置的初始值0.1和-0.1运行一下我们的线性模型看看结果：
print(sess.run(linear_model,{x:[1,2,3,6,8]}))
#运行一下损失模型：
print(sess.run(loss,{x:[1,2,3,6,8],y:[4.8, 8.5, 10.4, 21.0, 25.3]}))#1223.0499
#用tf.assign()对W和b变量重新赋值再检验一下：
#给W和b赋新值
fixW = tf.assign(W,[2.])
fixb = tf.assign(b,[1.])
#run之后新值才会生效
sess.run([fixW,fixb])
# 重新验证损失值
print(sess.run(loss, {x: [1, 2, 3, 6, 8], y: [4.8, 8.5, 10.4, 21.0, 25.3]}))#159.93999
#使用 TensorFlow 训练模型
#梯度下降(Gradient Descent)算法
#创建一个梯度下降优化器，学习率0.001
optimizer = tf.train.GradientDescentOptimizer(0.001)
train = optimizer.minimize(loss)
#用两个数组保存训练数据
x_train = [1, 2, 3, 6, 8]
y_train = [4.8, 8.5, 10.4, 21.0, 25.3]
#训练10000次
for i in range(10000):
    sess.run(train,{x:x_train,y:y_train})
#打印训练后的结果
print('W:%s b: %s loss:%s'%(sess.run(W),sess.run(b),sess.run(loss,{x:x_train,y:y_train})))