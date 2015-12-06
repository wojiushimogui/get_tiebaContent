#encoding=utf-8
#功能：抓取百度贴吧中帖子的内容
import urllib2
import urllib
import re
#定义一个类
class BaiduTieBa:
	#初始化，传入地址，以及是否只看楼主的参数
	def __init__(self,url,seeLZ):
		self.url=url
		self.seeLZ="?see_lz"+str(seeLZ)
	#根据传入的页码来获取帖子的内容太
	def getPageContent(self,pageNum):
		url=self.url+self.seeLZ+"&pn="+str(pageNum)
		user_agent="Mozilla/5.0 (Windows NT 6.1)"
		headers={"User-Agent":user_agent}
		try:
			request=urllib2.Request(url,headers=headers)
			response=urllib2.urlopen(request)
			content=response.read().decode("utf-8")
			print content
			return content
		except urllib2.URLError,e:
			if hasattr(e,"reason"):
				print e.reason

url=raw_input("raw_input:")
seeLZ=input("input a number:")
pageNum=input("input pageNum:")
baidutieba=BaiduTieBa(url,seeLZ)
baidutieba.getPageContent(pageNum)