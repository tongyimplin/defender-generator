import os
import shutil
import time
import zipfile


class GeneratorCore:

    def __init__(self, copyPath, idcardTpl, count, targetPath):
        self.copyPath = copyPath
        self.idcardTpl = idcardTpl
        self.count = count
        self.targetPath = targetPath

    """
    将数字和身份证模板拼凑在一起
    """
    def _combinedStr(self, tpl, c):
        starLen = tpl.count('*')
        return tpl.replace('*', '', starLen)+str(c).rjust(starLen, '0')

    def _writeSpecificFile(self, path, idcard):
        file = path+"/crq_p001.txt"
        print("处理特殊文件: %s"%file)
        fo = open(file, 'w')
        fo.write("""<?xml version="1.0" encoding="utf-8"?>
<Transaction>
	<TransHeader>
		<TransCode>P001</TransCode>
		<TransDate>20180528</TransDate>
		<TransTime>103724</TransTime>
	</TransHeader>
	<TransBody>
	<Response>
		<RespCode>CRQ000</RespCode>
		<RespMsg>成功获取本地信用报告!</RespMsg>
		<SerialNo>201805070000001</SerialNo>
		<ReportNo>{IDCARD}</ReportNo>
	</Response>
	</TransBody>
</Transaction>""".replace("{IDCARD}", idcard))
        fo.close()
        print("处理完成!")

    def _sealToZip(self, path):
        # 上级目录
        parentDic = os.path.dirname(path)
        # 文件名
        zipFileName = time.strftime("%Y%m%d%H%M%S.zip", time.localtime())
        zipFullName = parentDic+"/"+zipFileName
        f = zipfile.ZipFile(zipFullName, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                f.write(os.path.join(dirpath, filename), dirpath.replace(path+"\\", '')+"/"+filename)
        f.close()
        # 创建压缩包成功
        print("创建压缩包成功: "+zipFullName)
        return zipFullName

    def start_work(self):
        # 检测源目录是否存在
        if(os.path.exists(self.copyPath) == False):
            raise SystemError("不存在的copy目录: %s" % self.copyPath)
        # 检测目标目录是否存在
        if(os.path.exists(self.targetPath)):
            shutil.rmtree(self.targetPath)
        time.sleep(1)
        os.mkdir(self.targetPath)
        for i in range(1, int(self.count)):
            idcard = self._combinedStr(self.idcardTpl, i)
            curPath = self.targetPath+"/"+idcard
            print("开始处理: %s" % curPath)
            # 创建目标目录
            shutil.copytree(self.copyPath, curPath)
            self._writeSpecificFile(curPath, idcard)
        # 打压缩包
        return self._sealToZip(self.targetPath)




# generator = GeneratorCore("E:/temp/copy", "51302119920404****", 5, "E:/temp/target")
# generator.start_work()