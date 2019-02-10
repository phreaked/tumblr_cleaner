from mechanize import Browser
from lxml import html
from math import ceil

class Tumblr:
	def __init__(self):
		self.m = Browser()
		self.m.set_handle_robots(False)
		self.m.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36')]

	def login(self, email, password):
		self.m.open("https://www.tumblr.com/login")
		self.m.select_form(nr=0)
		self.m.form["user[email]"] = email
		self.m.form["user[password]"] = password
		self.m.submit()
		self.posts = []
		login = False
		if "dashboard" in self.m.geturl():
			login = True
		return login

	def logged_in(self):
		active = True
		if "tumblr.com/login" in self.m.geturl():
			active = False
		return active

	def set_username(self, username):
		self.username = username

	def all_blogs(self):
		self.m.open("https://www.tumblr.com/settings/account")
		tree = html.fromstring(self.m.response().read())
		blogs = tree.xpath("//div[@class='hide_overflow']/text()")
		blogs = [blog.replace("\n","").replace(" ","") for blog in blogs]
		self.blogs = blogs[6:-1]

	def all_pages(self):
		self.m.open("https://tumblr.com/blog/{}".format(self.username))
		blog_html = self.m.response().read()
		tree = html.fromstring(blog_html)
		sidebar = tree.find_class("count")
		self.post_count = int(sidebar[0].text_content().replace(",","").replace(".",""))
		if self.post_count > 10:
			pages = int(ceil((self.post_count/10)))
		else:
			pages = 1
		self.pages = pages
		while True:
			self.m.open("https://tumblr.com/blog/{}/{}".format(self.username, (self.pages + 1)))
			blog_html = self.m.response().read()
			tree = html.fromstring(blog_html)
			posts = tree.find_class("with_permalink")
			if len(posts) != 0:
				self.pages += 1
				self.post_count += len(posts)
			else:
				break
		return self.pages

	def form_key(self):
		self.m.open("https://www.tumblr.com/mega-editor/{}".format(self.username))
		key_html = self.m.response().read().splitlines()
		key_html = [line for line in key_html if "form_key" in str(line)]
		key_html = str(key_html[0]).strip().split("'")
		self.key = key_html[1]

	def delete_posts(self):
		ids = self.posts[0:100]
		[self.posts.remove(i) for i in ids]
		ids = ",".join(ids)
		data = "post_ids={}&form_key={}".format(ids, self.key)
		self.m.open("https://www.tumblr.com/delete_posts", data)

	def strip_perma(self, permalink):
		post_id = permalink.split("/post/")
		if "/" in post_id[1]:
			post_id = post_id[1].split("/")
			post_id = post_id[0]
		else:
			post_id = post_id[1]
		return post_id

	def get_posts(self):
		self.m.open("http://tumblr.com/blog/{}/{}".format(self.username, self.pages))
		html_source = self.m.response().read()
		tree = html.fromstring(html_source)
		self.conts = tree.find_class("with_permalink")
		self.permalinks = [cont.find_class("post_permalink") for cont in self.conts]
		self.pages -= 1

	def add_id(self, id_number):
		try:
			self.posts += [str(self.strip_perma(self.permalinks[id_number][0].xpath("@href")[0]))]
		except:
			pass

	def keep_original(self):
		parents = [cont.find_class("post_info_fence") for cont in self.conts]
		for i in range(len(self.conts)):
			if len(parents[i]) > 0:
				self.add_id(i)

	def keep_relevant(self):
		for i in range(len(self.conts)):
			post_text = self.conts[i].text_content().splitlines()
			post_parent = post_text[1]
			del post_text[1]
			post_text = "".join(post_text)
			if "reblogged" in post_parent:
				if self.username not in post_text:
					self.add_id(i)
				
	def delete_all(self):
		for i in range(len(self.conts)):
			self.add_id(i)
