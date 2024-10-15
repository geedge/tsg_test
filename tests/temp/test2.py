# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import support.ui_utils.env

def test2():
    # try:
    #     print(33333333333)
    #     driver = support.ui_utils.env.my_driver()
    #     return "execute test2"
    # except Exception as e:
    #     print("test2 error:", str(e))
    #     return "test2 error:" + str(e)
    # finally:
    #     print(44444444444)
    print(33333333333)
    driver = support.ui_utils.env.my_driver()
    print(44444444444)

if __name__ == "__main__":
    test2()