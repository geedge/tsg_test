# -*- coding: UTF-8 -*-
import os
import platform
import subprocess
import shutil

def search_package(command):
    output = ""
    success_flag = False
    try:
        result = subprocess.check_output(command, shell=True)
        print("The command is executed successfully. The output is:")
        print(result.decode("utf-8"))
        output = result.decode("utf-8")
        success_flag = True
    except subprocess.CalledProcessError as e:
        print("Fail to execute the command. The return code: {}".format(e.returncode))  
        print("Error message: {}".format(e.output.strip() if e.output else "no output"))
        success_flag = False
    return output, success_flag

def install_package():
    try:
        os_name = platform.system()
        if os_name == "Linux":
            release_result = subprocess.check_output("cat /etc/centos-release", shell=True)
            release_output = release_result.decode("utf-8")
            if "release 7.9" in release_output:
                cli = "python3"
                command = "rpm -qa | grep '{}'".format(cli.replace("'", "'\\''"))
                _, flag = search_package(command)
                if flag == False:
                    print("Python3 is not installed, start installing now.")
                    subprocess.check_call(["yum", "-y", "update"])
                    subprocess.check_call(["yum", "install", "-y", "net-tools"])
                    subprocess.check_call(["yum", "install", "-y", "wget"])
                    subprocess.check_call(["yum", "install", "-y", "zlib-devel", "bzip2-devel", "openssl-devel", "ncurses-devel", "sqlite-devel", "readline-devel", "tk-devel", "gcc", "make"])
                    subprocess.check_call(["yum", "install", "-y", "python3-devel"])
                    subprocess.check_call(["yum", "install", "-y", "java-1.8.0-openjdk"])
                    # 安装远程桌面需要的包
                    # subprocess.check_call(["yum", "install", "-y", "epel-release"])
                    # subprocess.check_call(["yum", "install", "-y", "xrdp"])
                    # subprocess.check_call(["systemctl", "start", "xrdp"])
                    # subprocess.check_call(["systemctl", "enable", "xrdp"])
                    subprocess.check_call(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm"])
                    subprocess.check_call(["yum", "localinstall", "-y", "google-chrome-stable_current_x86_64.rpm"])
                    result = subprocess.check_output("google-chrome --version", shell=True)
                    output = result.decode("utf-8")
                    if len(output) > 0:
                        temp = output.split(" ", 2)
                        if len(temp) > 2:
                            chrome_version = temp[2].rstrip()
                            url = "https://storage.googleapis.com/chrome-for-testing-public/{}/linux64/chromedriver-linux64.zip".format(chrome_version)
                        subprocess.check_call(["wget", url])
                        subprocess.check_call(["unzip", "chromedriver-linux64.zip"])
                        os.chdir("/opt/chromedriver-linux64")
                        subprocess.check_call(["mv", "chromedriver", "/usr/local/bin"])
                        subprocess.check_call(["chmod", "777", "/usr/local/bin/chromedriver"])
                    subprocess.check_call(["yum", "install", "-y", "python3"])
                    # subprocess.check_call(["wget", "https://www.python.org/ftp/python/3.11.8/Python-3.11.8.tgz"])
                    # subprocess.check_call(["tar", "-xzf", "Python-3.11.8.tgz"])
                    # os.chdir("/opt/Python-3.11.8")
                    # subprocess.check_call(["./configure", "--prefix=/usr/local/python3", "--with-openssl=/usr/bin/openssl"])
                    # subprocess.check_call(["make"])
                    # subprocess.check_call(["make", "install"])
                    # subprocess.check_call(["mv", "/usr/bin/python", "/usr/bin/python.bak"])
                    # subprocess.check_call(["ln", "-s", "/usr/local/python3/bin/python3", "/usr/bin/python"])
                    # with open("/usr/bin/yum", "r") as file:
                    #     content = file.readlines()
                    # content[0] = "#!/usr/bin/python2.7\n"
                    # with open("/usr/bin/yum", "w") as file:
                    #     file.writelines(content)
                    # with open("/usr/libexec/urlgrabber-ext-down", "r") as file:
                    #     content = file.readlines()
                    # content[0] = "#!/usr/bin/python2.7\n"
                    # with open("/usr/libexec/urlgrabber-ext-down", "w") as file:
                    #     file.writelines(content)
                    # subprocess.check_call(["yum", "install", "-y", "python3-pip"])
                    # subprocess.check_call(["ln", "-s", "/usr/local/python3/bin/pip3", "/usr/bin/pip"])
                    # subprocess.check_call(["python3", "-m", "pip", "install", "requests"])
                    # subprocess.check_call(["pip3", "install", "requests"])
                    # subprocess.check_call(["pip3", "install", "flask"])
                    # subprocess.check_call(["pip3", "install", "psutil"])
                    # subprocess.check_call(["pip3", "install", "selenium"])
                    # subprocess.check_call(["pip3", "install", "pymysql"])
                    # subprocess.check_call(["pip3", "install", "scapy"])
                    # subprocess.check_call(["pip3", "install", "PyYAML"])
                    # subprocess.check_call(["pip3", "install", "pytest"])
                    # subprocess.check_call(["pip3", "install", "pytest_check"])
                    # print("Install package successfully.")
        elif os_name == "Windows":
            command = "python --version"
            output, _ = search_package(command)
            if "Python was not found" in output:
                print("python is not installed.")
                # install chrome
                chrome_path = "D:/Document/Project-TSG/Code/git/tsg_test/package/chrome_setup/ChromeStandaloneSetup64.exe"
                subprocess.run([chrome_path], check=True)
                # move chromedriver to chrome path
                source_path = "D:/Document/Project-TSG/Code/git/tsg_test/package/chromedriver_win64/chromedriver.exe"
                destination_path = "C:/Program Files/Google/Chrome/Application"
                shutil.move(source_path, destination_path)
                # install java
                jdk_path = "D:/Document/Project-TSG/Code/git/tsg_test/package/jdk_setup"
                subprocess.run([jdk_path], check=True)
                # set java env
                # os.environ["JAVA_HOME"] = "C:/Program Files/Java/jdk1.8.0_301"
                # os.environ["Path"] = "C:/Program Files/Java/jdk-21/bin"
                # os.environ["CLASSPATH"] = "C:/Program Files/Java/jdk-21/lib"
                jdk_command = ["setx", "System", "JAVA_HOME", "C:/Program Files/Java/jdk1.8.0_301"]
                subprocess.run(jdk_command, check=True)
                bin_command = ["setx", "System", "Path", "C:/Program Files/Java/jdk-21/bin"]
                subprocess.run(bin_command, check=True)
                lib_command = ["setx", "System", "CLASSPATH", "C:/Program Files/Java/jdk-21/lib"]
                subprocess.run(lib_command, check=True)
                print("Install package successfully.")
    except:
        print("Fail to install package.")
        
if __name__ == '__main__':
    install_package()