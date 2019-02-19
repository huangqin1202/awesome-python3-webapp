import tensorflow as tf
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