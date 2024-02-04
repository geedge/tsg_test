from selenium import webdriver
import shutil
import time, datetime
import os
import functools
from workpath import workdir

# 截图装饰器
def screenshot_on_failure(func):
    @functools.wraps(func)
    def warpper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except:
            driver = self.driver
            if driver:
                formatted_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
                file = "{}.png".format(formatted_time)
                file_path = os.path.join(workdir, "results", "screenshot", file)
                file_path_work = os.path.join(workdir, "results", "screenshot")
                if not os.path.exists(file_path_work):
                    os.makedirs(file_path_work)
                if not os.path.exists(file_path):
                    print(f"截图保存于：{file_path}")
                    driver.save_screenshot(file_path)
                #删除历史7天前数据
                try:
                    clear_history(file_path)
                except:
                    print("删除历史数据失败...")
                raise
    return warpper

def clear_history(file_path, retain_time=3600*24*1):
    time_now = time.time()
    file_work = os.path.dirname(file_path)
    data_list = [os.path.join(file_work, i) for i in os.listdir(file_work)]
    for datapath in data_list:
        if time_now - os.path.getctime(datapath) > retain_time:
            try:
                os.remove(datapath)
            except:
                shutil.rmtree(datapath)
