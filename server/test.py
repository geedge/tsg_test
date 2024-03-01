import subprocess

def test():
    try:
        command = "google-chrome --version"
        # subprocess.check_call(["python2", "installPython3.py"])
        result = subprocess.check_output(command, shell=True)
        output = result.decode("utf-8")
        print(output)
        if len(output) > 0:
            temp = output.split(" ", 2)
            if len(temp) > 2:
                chrome_version = temp[2]
                print(chrome_version)
                url = "https://storage.googleapis.com/chrome-for-testing-public/{}/linux64/chromedriver-linux64.zip".format(chrome_version)
                print(url)
    except:
        print("Error")

if __name__ == "__main__":
    test()