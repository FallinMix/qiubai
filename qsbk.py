#encoding:utf-8
import urllib
import urllib2
import re
import thread
import time

URL = 'http://www.qiushibaike.com/hot/page/'

class Qsbk:
	"""docstring for Qsbk"""
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers = { 'User-Agent' : self.user_agent }
		self.stories = []
		self.enable = False

	#根据传入的页数获取页码代码
	def getPage(self, pageIndex):
		try:
			url = URL + str(pageIndex)
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)

			#将页面转化为utf-8编码
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError as e:
			if hasattr(e, "reason"):
				print u'连接糗事百科失败，错误原因：', e.reason
				return None
			
	def getPageItems(self, pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print "页面加载失败！"
			return None

		pattern = re.compile('<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?content">.*?span>(.*?)</span>(.*?)number">(.*?)</i>.*?number">(.*?)</i>',re.S)
		items = re.findall(pattern, pageCode)
		pageStories = []

		for item in items:
			haveImg = re.search("img", item[2])
			if not haveImg:
				replaceBr = re.compile("<br/>")
				text = re.sub(replaceBr, "\n", item[1])
				#item[0]是作者，item[1]是内容，item[3]是点赞数，item[4]是评论数
				pageStories.append([item[0].strip(), text.strip(), item[3].strip(), item[4].strip()])
				return pageStories

	#加载并提取页面的内容，加入到列表中
	def loadPage(self):
		if self.enable == True:
			if len(self.stories) < 2:
				#获取新一页
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	def printPage(self, pageStories, page):
		for story in pageStories:
			#等待用户输入
			input = raw_input()
			#每当输入一次回车，判断一下是否加载新页面
			self.loadPage()
			#如果输入Q或q则退出
			if input == "Q" or input == "q":
				self.enable = False
				return
			print u'第%d页\t发布人：%s\t点赞数：%s\t评论数：%s\n%s' %(page, story[0], story[2], story[3], story[1])

	def start(self):
		print u'正在读取糗事百科，按回车查看新内容，输入Q或q退出'
		#使能变量enable，开启程序
		self.enable = True
		#预加载页面
		self.loadPage()
		currentPage = 0
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				currentPage += 1
				del self.stories[0]
				self.printPage(pageStories, currentPage)

spider = Qsbk()
spider.start()