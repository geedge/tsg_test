import test2
def test1():
    try:
        print(11111111111)
        test2.test2()
        print(55555555555)
        return "execute test1"
    except Exception as e:
        print("test1 error:", str(e))
        return "test1 error:" + str(e)
    finally:
        print(22222222222)

if __name__ == "__main__":
    test1()