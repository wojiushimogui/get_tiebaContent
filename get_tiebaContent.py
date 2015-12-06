#encoding=utf-8
#功能：抓取百度贴吧中帖子的内容
import urllib2
import urllib
import re
#定义一个工具类来处理内容中的标签
class Tool:
	#去除img标签，7位长空格
	removeImg=re.compile('<img.*?>| {7}|')
	#去除超链接标签
	removeAddr=re.compile('<a.*?>|</a>')
	#把换行的标签换为\n
	replaceLine=re.compile('<tr>|<div>|</div>|</p>')
	#将表格制表<td>替换为\t
	replaceTD=re.compile('<td>')
	#把段落开头换为\n加空两格
	replacePara=re.compile('<p.*?>')
	#将换行符或双换行符替换为\n
	replaceBR=re.compile('<br><br>|<br>')
	#将其余标签删除
	removeExtraTag=re.compile('<.*?>')
	def replace(self,x):
		x=re.sub(self.removeImg,"",x)
		x=re.sub(self.removeAddr,"",x)
		x=re.sub(self.replaceLine,"\n",x)
		x=re.sub(self.replaceTD,"\t",x)
		x=re.sub(self.replacePara,"\n  ",x)
		x=re.sub(self.replaceBR,"\n",x)
		x=re.sub(self.removeExtraTag,"",x)
		return x.strip()

#定义一个类
class BaiduTieBa:
	#初始化，传入地址，以及是否只看楼主的参数
	def __init__(self,url,seeLZ):
		self.url=url
		self.seeLZ="?see_lz="+str(seeLZ)
		self.tool=Tool()
	#根据传入的页码来获取帖子的内容太
	def getPageContent(self,pageNum):
		url=self.url+self.seeLZ+"&pn="+str(pageNum)
		user_agent="Mozilla/5.0 (Windows NT 6.1)"
		headers={"User-Agent":user_agent}
		try:
			request=urllib2.Request(url,headers=headers)
			response=urllib2.urlopen(request)
			content=response.read().decode("utf-8")
			#print content  #测试输出
			return content
		except urllib2.URLError,e:
			if hasattr(e,"reason"):
				print e.reason
	#得到帖子的标题
	def getPageTitle(self,pageNum):
		content=self.getPageContent(pageNum)
		pattern=re.compile(r'<h3 class="core_title_txt pull-left text-overflow .*?>(.*?)</h3>',re.S)
		title=re.search(pattern,content)
		if title:
			print title.group(1).strip()
			return title.group(1).strip()
		else:
			print None
	#得到帖子的作者
	def getPageAuthor(self,pageNum):
		content=self.getPageContent(pageNum)
		# <div class="louzhubiaoshi  j_louzhubiaoshi" author="懂球君">
		pattern=re.compile(r'<div class="louzhubiaoshi  j_louzhubiaoshi" author="(.*?)">',re.S) 
		author=re.search(pattern,content)
		if author:
			print author.group(1).strip()#测试输出
			return author.group(1).strip()
		else :
			print None
	#得到帖子的总页数和总回复数
	def getPageTotalPageNum(self,pageNum):
		content=self.getPageContent(pageNum)
		#<li class="l_reply_num" style="margin-left:8px" ><span class="red" style="margin-right:3px">1</span>回复贴，共<span class="red">1</span>页</li>
		pattern=re.compile(r'<li class="l_reply_num".*? style="margin-right:3px">(.*?)</span>.*?<span class="red">(.*?)</span>',re.S)
		totalPageNum=re.search(pattern,content)
		if totalPageNum:
			print totalPageNum.group(1).strip(),totalPageNum.group(2).strip()#测试输出
			#print totalPageNum[0],totalPageNum[1]
			return totalPageNum.group(1).strip(),totalPageNum.group(2).strip()#第一个返回值为回复个数，第二个返回值为帖子的页数
		else:
			print "没找到"
			print None
	#提取帖子的内容
	def getContent(self,pageNum):
		content=self.getPageContent(pageNum)
		#html代码中的格式如下：
		#<div id="post_content_80098618952" class="d_post_content j_d_post_content "> 
		#一个省女性几千万人 比刘亦菲漂亮的可以找出几个</div>
		#提取正则表达式如下：
		pattern=re.compile(r'<div id="post_content_.*?>(.*?)</div>',re.S)
		items=re.findall(pattern,content)
		floor=1
		for item in items:
			print floor,u"楼-------------------------------------------\n"
			print self.tool.replace(item)
			floor+=1
		return items


#url=raw_input("raw_input:")
url="http://www.tieba.baidu.com/p/4197307435"
seeLZ=input("input a number:")
pageNum=input("input pageNum:")
baidutieba=BaiduTieBa(url,seeLZ)#实例化一个对象
#content=baidutieba.getPageContent(pageNum)#调用函数
#开始解析得到帖子标题
#baidutieba.getPageTitle(1)
#开始解析得到帖子的作者
#baidutieba.getPageAuthor(1)
#baidutieba.getPageTotalPageNum(1)
#解析帖子中的内容
baidutieba.getContent(pageNum)