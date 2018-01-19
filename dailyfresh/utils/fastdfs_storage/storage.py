"""
FastDFS是一个开源的轻量级分布式文件系统。
它解决了大数据量存储和负载均衡等问题。
特别适合以中小文件（建议范围：4KB< file_size <500MB）
为载体的在线服务，如相册网站、视频网站等等。
系统组成有:FastDFS只有两个角色：Tracker server和Storage server。
Tracker server作为中心结点，其主要作用是负载均衡和调度。
Tracker server在内存中记录分组和Storage server的状态等信息，不记录文件索引信息，占用的内存量很少。
另外，客户端（应用）和Storage server访问Tracker server时，Tracker server扫描内存中的分组和Storage server信息，然后给出应答。
由此可以看出Tracker server非常轻量化，不会成为系统瓶颈。
FastDFS中的Storage server在其他文件系统中通常称作Trunk server或Dataserver。
Storage server直接利用OS的文件系统存储文件。
FastDFS不会对文件进行分块存储，客户端上传的文件和Storage server上的文件一一对应。

Nginx为反向代理服务器:
在管理员上传文件到fastDFS文件存储服务器后,nginx会自动将图片资源缓存到自身服务器中,
在用户请求时,通过模板文件中的函数自动访问nginx服务器的地址下载图片.

FastDFS + Nginx 可以很好的管理静态资源
"""
# Storage django系统自带的文件存储仓库
from django.core.files.storage import Storage
# Fdfs分布式快速文件管理系统的Python实现包
from fdfs_client.client import Fdfs_client
# FASTDFS_CLIENT_CONF:快速分布式文件管理系统客户端的配置路径
# FASTDFS_NGINX_URL:反向代理服务器的url地址
from dailyfresh import settings

# fastDFS服务器配置文件修改:
# 主机地址用命令ifconfig查看,不要写localhost和127.0.0.1
# 1.将/etc/fdfs目录下的storage.conf配置文件中的第118行tracker_server的主机地址改为自己实际的主机地址
# 2.将/etc/fdfs目录下的mod_fastdfs.conf配置文件中的第40行tracker_server的主机地址改为自己实际的主机地址
# 3.将/etc/fdfs目录下的client.conf配置文件中的第14行tracker_server的主机地址改为自己实际的主机地址
# Nginx服务器的配置文件修改
# # 3.将/usr/local/nginx/conf目录下的nginx.conf配置文件中的第14行tracker_server的主机地址改为自己实际的主机地址
# server
# { listen 8888;
#   server_name localhost;
#   location ~ / group[0 - 9] / {
#   ngx_fastdfs_module;

# 启动
# fastDFS服务器和nginx服务器
# 1.启动tracker服务器: sudo service fdfs_trackerd start
# 2.启动storage服务器: sudo service fdfs_storaged start
# 3.启动Nginx服务器: sudo /usr/local/nginx/sbin/nginx
# 测试:
# 命令: fdfs_upload_file 客户端的配置文件路径 文件地址
# 如:  fdfs_upload_file /etc/fdfs/client.conf ./fruit.jpg
# 返回: group1/M00/00/00/wKg-glph_FuAOYR6AABtR_KnVbE877.jpg


class FastDFSStorage(Storage):
    """自定义文件存储系统"""
    def __init__(self, client_conf=None, nginx_url=None):
        """
        类的初始化,主要用于传参数,不在系统中写死是为了后续维护方便
        :param client_conf: fastDFS文件管理系统客户端配置文件
        :param nginx_url: nginx服务器的访问路径
        """
        # 如果系统启动时没有传入配置文件路径,使用默认路径
        if client_conf is None:
            client_conf = settings.FASTDFS_CLIENT_CONF
        self.client_conf = client_conf
        # 如果系统启动时没有指定nginx服务器路径,使用默认路径
        if nginx_url is None:
            nginx_url = settings.FASTDFS_NGINX_URL
        self.nginx_url = nginx_url

    def _open(self, name, mode='rb'):
        """如果项目需要打开文件,返回文件内容,代码在此实现"""
        pass

    def _save(self, name, content):
        """
        保存文件的时候,被调用,如何存储文件,代码在此实现
        :param name: 文件名
        :param content: 传送过来的文件对象,即要保存的文件对象
        :return: 文件存储id字符串
        """
        # 创建fastdfs客户端
        client = Fdfs_client(self.client_conf)
        # 通过文件对象读取文件内容
        file_data = content.read()

        # 利用客户端保存文件到fastdfs服务器中的Storage服务器,返回的是一个文件相关字典
        # ret是字典,内容为{
        # 'Group name'是文件存储在Storage存储服务器的组名
        # 'Group name' : group_name,
        # 'Remote file_id'文件在服务器中的文件名,包含访问服务器路径
        # 'Remote file_id' : remote_file_id,
        # 'Status' : 上传状态:成功
        # 'Status' : 'Upload successed.',
        # 'Local file name' :本地文件名
        # 'Local file name' : '',
        # 'Uploaded size' : 上传文件大小
        # 'Uploaded size' : upload_size, #上传文件大小
        # 'Storage IP'文件存储服务器的ip地址
        # 'Storage IP' : storage_ip }
        ret = client.upload_by_buffer(file_data)
        # 获取上传状态
        status = ret.get("Status")
        # 判断是否上次成功
        if status != 'Upload successed.':
            # 上传失败,抛出异常
            raise Exception("保存文件到fastdfs失败")
        else:
            # 上传成功,获取文件id
            file_id = ret.get("Remote file_id")

            # 返回id,管理员在提交时会存储到数据库中
            return file_id

    def exists(self, name):
        """
        django调用,用来判断要保存的文件是否存在,如果返回false,django会去调用_save()保存文件
        :param name:文件名
        :return:
        """
        return False

    def url(self, name):
        """
        当视图返回模板时,模板中的请求数据会从数据库中查询到对象后调用该方法,其返回值填充模板{{ sku.default_image.url }}
        :param name: 数据库中保存的文件信息，在我们的项目中，是之前保存的file_id
        :return: ulr
        """
        return self.nginx_url + name
