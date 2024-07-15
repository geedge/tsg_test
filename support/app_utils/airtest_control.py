import os
import argparse

def run_script(device_id, app_name):
    test_device_id = device_id
    app_operation = "open"
    packet_name = app_name
    report_name = app_name + "_report"
    rootDirectory = os.path.dirname(os.path.abspath(__file__))
    command = "python " + rootDirectory + "/app"
    if test_device_id == "http+usbmux://00008101-001951312251001E":
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], command + "/" + app_name + "/" + app_name + "_ios" + ".py" + " " + "-d " + test_device_id + " -n " + app_name + " -o " + app_operation + " -p " + packet_name + " -r " + report_name)
        result = os.system(command + "/" + app_name + "/" + app_name + "_ios" + ".py" + " " + "-d " + test_device_id + " -n " + app_name + " -o " + app_operation + " -p " + packet_name + " -r " + report_name)
    elif test_device_id == "http+usbmux://00008020-000244CE1A8A002E":
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], command + "/" + app_name + "/" + app_name + "_ios" + ".py" + " " + "-d " + test_device_id + " -n " + app_name + " -o " + app_operation + " -p " + packet_name + " -r " + report_name)
        result = os.system(command + "/" + app_name + "/" + app_name + "_ios" + ".py" + " " + "-d " + test_device_id + " -n " + app_name + " -o " + app_operation + " -p " + packet_name + " -r " + report_name)
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(datetime.now().microsecond)[:3], command + "/" + app_name + "/" + app_name + ".py" + " " + "-d " + test_device_id + " -n " + app_name + " -o " + app_operation + " -p " + packet_name + " -r " + report_name)
        result = os.system(command + "/" + app_name + "/" + app_name + ".py" + " " + "-d " + test_device_id + " -n " + app_name + " -o " + app_operation + " -p " + packet_name + " -r " + report_name)
    return result

if __name__ == '__main__':
    run_script("AWMCUT1325002090", "taobao")