#incognito('http://codeup.kr/loginpage.php')
(lambda main : main() if __name__ == "__main__" else main)(lambda : (incognito('http://c.x3.kro.kr'), __import__('subpr').lib.subpr('python')))