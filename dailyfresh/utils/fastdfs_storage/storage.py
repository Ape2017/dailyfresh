from django.core.files.storage import Storage # Storage django系统自带的文件存储仓库
# Fdfs 分布式快速文件管理系统
from fdfs_client.client import Fdfs_client
# 系统配置
from dailyfresh import settings


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
        :return:
        """
        # 创建fastdfs客户端
        client = Fdfs_client(self.client_conf)
        # 通过文件对象读取文件内容
        file_data = content.read()

        # 利用客户端保存文件到fastdfs服务器中的Storage服务器,返回的是一个文件相关字典
        # ret是字典,内容为{
        # 'Group name' : group_name,  # storage存储服务器的组名
        # 'Remote file_id' : remote_file_id, # 文件名字,唯一
        # 'Status' : 'Upload successed.',   # 上传状态:成功
        # 'Local file name' : '',       # 本地文件名
        # 'Uploaded size' : upload_size, #上传文件大小
        # 'Storage IP' : storage_ip } # 存储的ip地址
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
