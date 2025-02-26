# -*- coding: utf-8 -*-
import unittest

from co6co.utils import hash
from co6co.utils import File
from co6co.utils import log

class TestFile(unittest.TestCase):
    content:str=None
    def setUp(self):
        self.content="co6co[安安]！"
        pass 
    def test_base64(self): 
        data=hash.enbase64(self.content)
        self.assertEqual(data , 'Y282Y29b5a6J5a6JXe+8gQ==') 
        print(type(data))
        self.assertEqual(hash.debase64(data),self.content)
        
    def test_md5(self):
        self.assertEqual(hash.md5(self.content),"8e95c4650cf629db1a94dd1e0a72e787") 
    def test_hash(self):
        self.assertEqual(hash.str_sha1(self.content),"ae4fe3db3c0280941d34be63e8c0af330f9e5e5a")
        self.assertEqual(hash.str_sha224(self.content),"920eb220e67336c3ecb5d4b2b25fe10ec0651a15e050ee4355cc2f02")
        self.assertEqual(hash.str_sha256(self.content),"ad13bb193d5cd19c29fd8e6a70ae7679b931497c0f35116aed8c101659a9890f")
        self.assertEqual(hash.str_sha384(self.content),"45c7b80604d68f5e1e5c2b994cdec2ac2b8d42d7d3dcd0676151ecd85913cb37ea4497fff14a13ad38a95bf7cfa93787")
        self.assertEqual(hash.str_sha512(self.content),"e319fdd751fa61e08b5874e94ce80e2e9ff85fad0fe5ad2e96cd2ebf43a14a572803f95b359b21933ac4acf0f30baa1f3d15336748b28763e77c4951e6692d5c")
        
     
        
    def tearDown(self):
        pass
    
def suite():
    #若测试用例都是以test开头，则用 makeSuite()方法一次性运行
    return unittest.makeSuite(TestFile )
    suite=unittest.TestSuite() 
    suite.addTest(TestFile("test_base64"))  #添加测试用例
    return suite

if __name__=="__main__":
    #文件使用方案1. python v_utils_test.py
    #文件使用方案2 python -m unittest v_utils_test
    # 使用方案1
    unittest.main(defaultTest='suite') 
    # 使用方案2
    #runner=unittest.TextTestRunner()
    #runner.run(suite2)
    