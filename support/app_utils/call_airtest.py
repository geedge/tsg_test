#coding=utf-8
import subprocess
import time
import support.app_utils.airtest_control as airtest_control

class CallAirtest():
    def __init__(self):
        self.device_id = ""

    def start_airtest(self):
        # adb devices
        adb_devices = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "------>>>>>>", adb_devices.communicate()[0].decode().strip())
        subprocess.Popen("adb kill-server", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.Popen("adb start-server", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # adb root
        for i in range(100):
            time.sleep(int(2))
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "尝试adb root ----{}".format(i))
            adb_root = subprocess.Popen("adb root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            res_root = adb_root.communicate()[0].decode().strip()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "------>>>>>>", adb_root.communicate()[0].decode().strip())
            time.sleep(2)
            if res_root:
                adb_devices = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                break
            time.sleep(1)
            if i == 4:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "adb root 失败")
                exit(1)

        # adb devices
        for i in range(10):
            adb_devices = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            device_i = adb_devices.communicate()[0].decode().strip()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "------>>>>>>", device_i)
            if "device" in device_i.split()[-1]:
                self.setDeviceId(device_i.split()[-2])
                break
            time.sleep(4)
            if i == 4:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "adb devices offline")
                exit(1)
        
        # adb remount，若fail且用的是雷电9，需要在设置中使能system.vmdk可写入
        adb_remount = subprocess.Popen("adb remount", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], "------>>>>>>", adb_remount.communicate()[0].decode().strip())
        time.sleep(1)

    def stop_airtest(self):
        subprocess.Popen("adb root", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.Popen("adb remount", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        
    def run_airtest_script(self, device_id, app_name):
        result = airtest_control.run_script(device_id, app_name)
        return result

    def setDeviceId(self, extract_device_id):
        self.device_id = extract_device_id
    
    def getDeviceId(self):
        device_id = self.device_id
        return device_id

    def verifyResult(self):
        # 待补充
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], 111)

if __name__ == '__main__':
    # ms传给airtest信息：启动验证的状态（status=1是run，status=0是stop）、待验证的app名
    app_full_name = "com.taobao.taobao"
    app_name = "taobao"
    call_airtest = CallAirtest(app_full_name)
    call_airtest.start_airtest()
    device_id = call_airtest.getDeviceId()
    result = call_airtest.run_airtest_script(device_id, app_name)
    if result == 0:
        pcap_abs_path = call_airtest.stop_airtest()
    elif result != 0:
        call_airtest.verifyResult()