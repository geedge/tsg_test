import random
import string
import time
import datetime

class RandomName:
    """
    生成随机使用名称
    """
    def __init__(self, pro_name="test_uitemp", r_letter_count=8, r_number_count=8):
        self.pro_name = pro_name
        self.r_letter_count = r_letter_count
        self.r_number_count = r_number_count

    def random_name(self, source_name="", is_none = False):
        # 如果有sourceName内容则按source_name输出32位组长度输出字符串
        if source_name != "":
            if source_name.isalnum():   # 字母或数组
                source_name_len = len(source_name)
                count_half = int(source_name_len / 2)
                if source_name_len <= 14:
                    r_name = self.random_letter(count=source_name_len)
                else:
                    letters = self.random_letter(count=count_half)
                    numbers = self.random_number(count=count_half)
                    format_time = self.current_time()
                    r_name_1 = f"{self.pro_name}_{format_time}_{letters}_{numbers}"
                    r_name = r_name_1[:source_name_len]
            else:      # 含有其它非字母、数字字符
                r_name = "{}_{}_{}".format(self.pro_name, source_name, self.current_time())
        else:  # 如果无sourceName内容则输出32位组合长度
            letters = self.random_letter(self.r_letter_count)
            numbers = self.random_number(self.r_number_count)
            format_time = self.current_time()
            r_name = f"{self.pro_name}_{letters}_{numbers}_{format_time}"
            if is_none == True:
                r_name = ""
        return r_name

    def random_letter(self, count=8):
        temp_list = []
        for i in range(count):
            temp_list.append(random.choice(string.ascii_letters))
        r_letter = "".join(temp_list)
        return r_letter

    def random_number(self, count=8):
        temp_list = []
        for i in range(count):
            temp_list.append(random.choice(string.digits))
        r_number = "".join(temp_list)
        return r_number

    def random_phone(self, count=8):
        temp_list = []
        for i in range(count):
            temp_list.append(random.choice(string.digits))
        r_number = "".join(temp_list) + "*"
        return r_number

    def random_ipv4(self):
        ipv4_value = ".".join(str(random.randint(1, 255)) for _ in range(4))
        return ipv4_value

    def random_ipv6(self):
        ipv6 = []
        for i in range(8):
            segment = ''.join(random.choice("0123456789abcdef") for _ in range(4))
            ipv6.append(segment)
        ipv6_value = ":".join(ipv6)
        return ipv6_value

    def random_ipv4_or_ipv6(self):
        if random.random() > 0.2:
            ip = self.random_ipv4()
        else:
            ip = self.random_ipv6()
        return ip

    def random_url(self, length=5):
        letters = string.ascii_lowercase + string.digits
        abc = ''.join(random.choice(letters) for i in range(length)) + '.' + ''.join(
            random.choice(letters) for i in range(2))
        random_type_code = random.randint(0, 3)
        if random_type_code == 0:
            return '*{}'.format(abc)
        elif random_type_code == 1:
            return '{}*'.format(abc)
        elif random_type_code == 2:
            return '{}'.format(abc)
        elif random_type_code == 3:
            return '${}'.format(abc)
        else:
            return '{}'.format(abc.split(".")[0])

    def random_url_4_categories(self, length=8):
        letters = string.ascii_lowercase + string.digits
        abc = ''.join(random.choice(letters) for i in range(length)) + '.' + ''.join(
            random.choice(letters) for i in range(3))
        random_type_code = random.randint(0, 1)
        if random_type_code == 0:
            return '*{}'.format(abc)
        elif random_type_code == 1:
            return '${}'.format(abc)

    def random_account(self, length=8):
        letters = string.ascii_lowercase + string.digits
        abc = ''.join(random.choice(letters) for i in range(length))
        random_type_code = random.randint(0, 3)
        if random_type_code == 0:
            return '*{}'.format(abc)
        elif random_type_code == 1:
            return '{}*'.format(abc)
        elif random_type_code == 2:
            return '{}'.format(abc)
        elif random_type_code == 3:
            return '${}'.format(abc)

    def random_interval(self):
        low_boundary = 0
        up_boundary = 2 ** 31
        size = 2  # 选取两个数值
        random_interval = random.sample(range(low_boundary, up_boundary),
                                        size)  # 从[low_boundary, up_boundary)的序列中随机选择两个不重复的元素，返回列表
        return sorted(random_interval)

    def random_flag(self):
        flag_name_code = [i for i in range(1, 17)]
        flag_value_code = [0, 1]
        r_flag_name_code = str(random.choice(flag_name_code))
        r_flag_value_code = str(random.choice(flag_value_code))
        return r_flag_name_code + ":" + r_flag_value_code

    def current_time(self):
        c_time = time.time()
        formatted_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        return formatted_time

    def ip_to_int(self, ip):
        parts = [int(part) for part in ip.split('.')]
        return parts[0] * 256 ** 3 + parts[1] * 256 ** 2 + parts[2] * 256 + parts[3]

    def random_tunnel(self):
        start_ip = "10.0." + ".".join(str(random.randint(0, 255)) for _ in range(2))
        end_ip = "10.0." + ".".join(str(random.randint(0, 255)) for _ in range(2))
        if self.ip_to_int(start_ip) > self.ip_to_int(end_ip):
            start_ip, end_ip = end_ip, start_ip
        return start_ip + "-" + end_ip

    def random_apns(self, length=5):
        letters = string.ascii_lowercase + string.digits
        abc = ''.join(random.choice(letters) for i in range(length)) + '.' + ''.join(
            random.choice(letters) for i in range(2))
        random_type_code = random.randint(0, 3)
        if random_type_code == 0:
            return '*{}'.format(abc)
        elif random_type_code == 3:
            return '${}'.format(abc)
        else:
            return '*{}'.format(abc)

    def random_name_by_source(self, source_name="", source_letter=""):
        r_name = ""
        # 如果有sourceName内容则按source_name长度输出字符串，且字符在source_letter中
        if source_name != "":
            source_name_len = len(source_name)
            r_name = self.generate_code(length=source_name_len, chart_parttern=source_letter)
            if source_name_len > 32:
                letters = self.random_letter(self.r_letter_count)
                format_time = self.current_time()
                r_name = f"{self.pro_name}_{letters}_{format_time}_{r_name}"
                r_name = r_name[:source_name_len]

        else:  # 如果无sourceName内容则输出32位组合长度
            letters = self.random_letter(self.r_letter_count)
            numbers = self.random_number(self.r_number_count)
            format_time = self.current_time()
            r_name = f"{self.pro_name}_{letters}_{numbers}_{format_time}"
        return r_name

    def generate_code(self, length=4, chart_parttern=""):
        code1 = ""
        # str_pattern = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c'
        str_pattern = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"
        if chart_parttern != "":
            str_pattern = chart_parttern
        for _ in range(0, length):
            code1 = code1 + str_pattern[random.randint(0, len(str_pattern) - 1)]
        return code1
    
    def rand_password(self,min_length=8,max_length=16,password_strength=2, chart_parttern=""):
        password = ""
        if password_strength > 4:
            password_strength = 4
        if password_strength == 2:
            min_length = 8
        elif password_strength == 3:
            min_length = 10
        elif password_strength == 4:
            min_length = 12
        password_length = random.randint(min_length,max_length)
        str_pattern = ""
        #str_pattern = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c'
        list = ["0123456789", "abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "~!@#$%^&*_.?"]
        list_sub = random.sample(list, password_strength)
        for var in list_sub:
            str_pattern += str(var)
        if chart_parttern != "":
            str_pattern = chart_parttern
        for _ in range(0, password_length):
            password = password + str_pattern[random.randint(0, len(str_pattern) - 1)]
        if password_strength > 1 and password.isalpha():
            passowrd = self.rand_password(min_length=min_length,max_length=max_length,password_strength=password_strength, chart_parttern=chart_parttern)
        return password