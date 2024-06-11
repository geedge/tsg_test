import json
import os
from workpath import workdir

class ReadData:
    def __init__(self):
        #json文件和测试文件目录
        self.workdir = workdir
        self.testdata = "testdata"
        self.ui_data = "ui_data"
        #profiles模块目录名称
        self.profiles_data = "profiles_data"
        self.profiles_file = "profiles"
        #objects模块目录名称
        self.objects_data = "objects_data"
        self.ui_file = "ui_file"
        self.objects ="objects"
        self.import_file = "import_file"
        self.download_file = "download_file"
        #admin模块目录名称
        self.admin_data = "admin_area"
        self.System_Appearance = "System_Appearance"

    def _from_json(self, file):
        """
        从json中读取数据函数
        :param file:
        :return:
        """
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)["item"]
            data = list(data)
            return data

    def _abs_path(self, file_name):
        """
        重组路径-profiles模块路径重组
        :param file_name:
        :return:
        """
        file = os.path.join(self.workdir, self.testdata, self.ui_data, self.profiles_data, file_name)
        return file
    
    def _abs_obj_path(self,file_name):
        '''
        重组路径-objects模块路径重组
        '''
        file = os.path.join(self.workdir,self.testdata, self.ui_data, self.objects_data, file_name)
        return file
    
    def _profiles_files_dowload_path(self):
        self.file_path = os.path.join(self.workdir, self.testdata, self.ui_file, self.profiles_file, self.download_file)
        return self.file_path
    
    def _obj_files_path(self,file_name):
        '''
        重组路径-objects模块路径重组
        '''
        file = os.path.join(self.workdir,self.testdata, self.ui_file, self.objects,self.import_file,file_name)
        return file
    
    def _obj_files_dowload_path(self):
        self.file_path = os.path.join(self.workdir,self.testdata, self.ui_file, self.objects,self.download_file)
        return self.file_path

    def _admin_files_dowload_path(self):
        self.file_path = os.path.join(self.workdir, self.testdata, self.ui_file, "admin")
        return self.file_path
    
    def _admin_logs_dowload_path(self):
        self.file_path = os.path.join(self.workdir, self.testdata, self.ui_file, "admin","admin_logs")
        return self.file_path
    
    def _object_applications_export_path(self):
        self.file_path = os.path.join(self.workdir, self.testdata, self.ui_file, "objects", "Applications","export_json")
        return self.file_path

    def _abs_admin_path(self,file_name):
        '''
        重组路径-admin模块路径重组
        '''
        file = os.path.join(self.workdir,self.testdata, self.ui_data, self.admin_data, self.System_Appearance,file_name)
        return file

    def _abs_update_path(self,file_name):
        '''
        重组路径-admin模块路径重组
        '''
        file = os.path.join(self.workdir,self.testdata, self.ui_data, self.admin_data, "System_Updates",file_name)
        return file

    def _abs_Assessment_path(self,file_name):
        '''
        重组路径-admin模块路径重组
        '''
        file = os.path.join(self.workdir,self.testdata, self.ui_data, self.admin_data, "System_Assessment",file_name)
        return file

    def _abs_Ip_Library_path(self, file_name):
        '''
        重组路径-admin模块路径重组
        '''
        file = os.path.join(self.workdir, self.testdata, self.ui_data, self.admin_data, "IP_Libraries", file_name)
        return file

    def _abs_admin_logs_path(self, file_name):
        '''
        重组路径-admin模块路径重组
        '''
        file = os.path.join(self.workdir, self.testdata, self.ui_data, self.admin_data, "Admin_Logs", file_name)
        return file

    def read_data_profiles(self, file_name):
        """
        profile模块提取json数据方法
        :param file_name:
        :return:
        """
        file = self._abs_path(file_name)
        return self._from_json(file)

    def read_data_object(self,file_name):     # Json文件
        '''
        object模块提取json数据方法
        :param file_name:
        :return:
        '''
        file = self._abs_obj_path(file_name)
        return self._from_json(file)

    def read_data_admin(self,file_name):
        '''
        object模块提取json数据方法
        :param file_name:
        :return:
        '''
        file = self._abs_admin_path(file_name)
        return self._from_json(file)

    def read_data_admin_System_Updates(self, file_name):
        '''
        object模块提取json数据方法
        :param file_name:
        :return:
        '''
        file = self._abs_update_path(file_name)
        return self._from_json(file)

    def read_data_admin_System_Assessment(self, file_name):
        '''
        object模块提取json数据方法
        :param file_name:
        :return:
        '''
        file = self._abs_Assessment_path(file_name)
        return self._from_json(file)

    def read_data_admin_IP_Libraries(self, file_name):
        '''
        object模块提取json数据方法
        :param file_name:
        :return:
        '''
        file = self._abs_Ip_Library_path(file_name)
        return self._from_json(file)
    
    def read_data_admin_admin_logs(self, file_name):
        '''
        object模块提取json数据方法
        :param file_name:
        :return:
        '''
        file = self._abs_admin_logs_path(file_name)
        return self._from_json(file)
    
    def generate_id(self, param):
        """
        测试用例中ids信息提取
        :param param:
        :return:
        """
        ids: str = param["ids"]
        #print(ids)
        return ids

    def _admin_area_path(self, file_name):
        """
        重组路径
        :param file_name:
        :return:
        """
        file = os.path.join(self.workdir, self.testdata, self.ui_data, "admin_area", file_name)
        return self._from_json(file)
    
    def _federation_path(self, file_name):
        """
        重组路径
        :param file_name:
        :return:
        """
        file = os.path.join(self.workdir, self.testdata, self.ui_data, "federation", file_name)
        return self._from_json(file)
    
    def _manage_users_path(self, file_name):
        """
        重组路径
        :param file_name:
        :return:
        """
        file = os.path.join(self.workdir, self.testdata, self.ui_data, "admin_area", "manage_users", file_name)
        return self._from_json(file)
    
    def Read_Header_logo(self,folder_path):
        """
        提取测试图片

        """
        # 获取文件夹下所有文件的完整路径
        file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]
        return file_paths

    def Read_Appearance_Title(self,title_file):
        """
        提取Appearance下的Title
        """
        with open(title_file, 'r') as file:
            lines = file.readlines()  # 逐行读取文件内容并存储到列表中
        return lines

    def Read_Favicon(self,Favicon_path):
        # 获取文件夹下所有文件的完整路径
        file_paths = [os.path.join(Favicon_path, file) for file in os.listdir(Favicon_path)]
        return file_paths

    def Read_Login_Logo_Data(self,Login_path):
        file_paths = [os.path.join(Login_path, file) for file in os.listdir(Login_path)]
        return file_paths

    def Read_Language_txt(self,language_path):
        with open(language_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file]
        return lines
    
if __name__ == '__main__':
    r = ReadData()
    r.read_data_admin(file_name="language.json")