import os
import re
import tarfile
from datetime import datetime

# 导入Fabric API:
# fabric的安装：pip install fabric3
from fabric.api import *

# 服务器登录用户名和密码：
env.user = 'hq'
env.password = 'hq'
# sudo 用户为root：
env.sudo_user = 'root'
# 服务器地址，可以有多个，依次部署：
# env.hosts = ['192.168.1.133']
env.host_string = '192.168.1.133'

# 服务器MySQL用户名和口令：
db_user = 'root'
db_password = 'root'

_TAR_FILE = 'dist-awesome.tar.gz'


_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/awesome'


def _current_path():
    return os.path.abspath('.')


def _now():
    return datetime.now().strftime('%y-%m-%d_%H.%M.%S')


# 打包的任务
def build():
    # includes = ['static', 'templates', 'transwarp', 'favicon.ico', '*.py']
    # excludes = ['test', '.*', '*.pyc', '*.pyo']
    # local('rm -f dist/%s' % _TAR_FILE)  # fabric提供的local()，运行本地命令
    # with lcd(os.path.join(os.path.abspath('.'), 'www')):  # 将当期命令的目录设定为lcd()指定的目录
    #     cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
    #     cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
    #     cmd.extend(includes)
    #     local(' '.join(cmd))
    local('del dist\\%s' % _TAR_FILE)  # 删除旧压缩包
    tar = tarfile.open("dist/%s" % _TAR_FILE, "w:gz")  # 创建新压缩包
    for root, _dir, files in os.walk("www/"):  # 打包www文件夹
        for f in files:
            if not (('.pyc' in f) or ('.pyo' in f)):  # 排除开发过程调试产生的文件
                fullpath = os.path.join(root, f)
                tar.add(fullpath)
    tar.close()


def deploy():
    newdir = 'www-%s' % _now()
    # 删除已有的tar文件
    run('rm -f %s' % _REMOTE_TMP_TAR)
    # 上传新的tar文件：
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    # 创建新目录
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    # 解压到新目录
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)  # 解压
        sudo('mv www/* .')  # 解压后多一层www文件， 因此向上移动一层
        sudo('rm -rf www')  # 删除空文件夹www
        sudo('dos2unix app.py')  # 解决windows和linux行尾换行不同问题
        sudo('chmod a+x app.py')  # 是app.py可直接执行
    # 重置软链接：
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')  # 删除旧软链接
        sudo('ln -s %s www' % newdir)  # 创建新软链接
        sudo('chown hq:hq www')  # 授权
        sudo('chown -R hq:hq %s' % newdir)
    # 重启python服务和nginx服务器
    with settings(warn_only=True):
        # supervisor重启app
        sudo('supervisorctl stop awesome')
        sudo('supervisorctl start awesome')
        # Nginx重启
        sudo('/etc/init.d/nginx reload')


RE_FILES = re.compile('\r?\n')


def rollback():
    """
    rollback to previous version
    :return:
    """
    with cd(_REMOTE_BASE_DIR):
        r = run('ls -p -1')
        files = [s[:-1] for s in RE_FILES.split(r) if s.startswith('www-') and s.endswith('/')]
        files.sort(reverse=True)
        r = run('ls -l www')
        ss = r.split(' -> ')
        if len(ss) != 2:
            print('ERROR: \'www\' is not a symbol link.')
            return
        current = ss[1]
        print('Found current symbol link points to: %s\n' % current)
        try:
            index = files.index(current)
        except ValueError as e:
            print('ERROR: symbol link is invalid.')
            return
        if len(files) == index + 1:
            print('ERROR: already the oldest version.')
        old = files[index + 1]
        print('==================================================')
        for f in files:
            if f == current:
                print('      Current ---> %s' % current)
            elif f == old:
                print('  Rollback to ---> %s' % old)
            else:
                print('                   %s' % f)
        print('==================================================')
        print('')
        yn = input('continue? y/N ')
        if yn != 'y' and yn != 'Y':
            print('Rollback cancelled.')
            return
        print('Start rollback...')
        sudo('rm -f www')
        sudo('ln -s %s www' % old)
        sudo('chown www-data:www-data www')
        with settings(warn_only=True):
            sudo('supervisorctl stop awesome')
            sudo('supervisorctl start awesome')
            sudo('/etc/init.d/nginx reload')
        print('ROLLBACKED OK.')


def backup():
    """
    Dump entire database on server and backup to local.
    :return:
    """
    dt = _now()
    f = 'backup-awesome-%s.sql' % dt
    with cd('/tmp'):
        run('mysqldump --user=%s --password=%s --skip-opt --add-drop-table --default-character-set=utf8 --quick awesome > %s' % (db_user, db_password, f))
        run('tar -czvf %s.tar.gz %s' % (f, f))
        get('%s.tar.gz' % f, '%s/backup/' % _current_path())
        run('rm -f %s' % f)
        run('rm -f %s.tar.gz' % f)


def restore2local():
    """
    Restore db to local
    :return:
    """
    backup_dir = os.path.join(_current_path(), 'backup')
    fs = os.listdir(backup_dir)
    files = [f for f in fs if f.startswith('backup-') and f.endswith('.sql.tar.gz')]  # 获取备份文件列表
    files.sort(reverse=True)  # 最近的文件排在前面
    if len(files) == 0:
        print('No backup files found.')
        return
    print('Found %s backup files:' % len(files))
    print('==================================================')
    n = 0
    for f in files:
        print('%s: %s' % (n, f))
        n = n + 1
    print('==================================================')
    print('')
    try:
        num = int(input('Restore file: '))  # 选择恢复哪个备份
    except ValueError:
        print('Invalid file number.')
        return
    restore_file = files[num]
    yn = input('Restore file %s: %s? y/N ' % (num, restore_file))  # 确定开始恢复
    if yn != 'y' and yn != 'Y':
        print('Restore cancelled.')
        return
    print('Start restore to local database...')
    p = input('Input mysql root password: ')
    sqls = [
        'drop database if exists awesome;',
        'create database awesome;',
        'alter database awesome default character set utf8 collate utf8_general_ci;'  # 修改为utf8字符集
        'grant select, insert, update, delete on awesome.* to \'%s\'@\'localhost\' identified by \'%s\';' % (db_user, db_password)
    ]
    for sql in sqls:
        local(r'mysql -uroot -p%s -e "%s"' % (p, sql))  # 删除旧数据库，新建数据库，授权给用户
    extract('backup\\%s' % restore_file, 'backup\\')    # 解压
    with lcd('backup'):
        # linux系统和windows系统之间数据库导入导出，可能因为字符集不同出现'unknown command \\'错误
        # 通过在创建数据库后修改为utf8字符集，以及导入时指定--default-character-set=utf8，解决这个问题
        local(r'mysql -uroot -p%s --default-character-set=utf8 awesome < %s' % (p, restore_file[:-7]))  # 导入数据库
        local('del %s' % restore_file[:-7])  # 删除解压出的文件


def extract(tar_path, target_path):
    """
    解压tar.gz文件到目标目录
    :param tar_path:
    :param target_path:
    :return:
    """
    try:
        tar = tarfile.open(tar_path, "r:gz")
        file_names = tar.getnames()
        for file_name in file_names:
            tar.extract(file_name, target_path)
        tar.close()
    except Exception as e:
        raise e


if __name__ == '__main__':
    build()
    deploy()
    # rollback()
    # backup()
    # restore2local()
    # input()





