import sys
from tumblr import Tumblr
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class UITumblrLogin(QWidget):
	def __init__(self, parent=None):
		super(UITumblrLogin, self).__init__(parent)
		self.email_label = QLabel(self)
		self.email_label.setText("Tumblr Email:")
		self.email_label.move(20,20)
		self.email_txt = QLineEdit(self)
		self.email_txt.move(20,40)
		self.email_txt.resize(240,25)
		self.password_label = QLabel(self)
		self.password_label.setText("Tumblr Password:")
		self.password_label.move(20,75)
		self.password_txt = QLineEdit(self)
		self.password_txt.move(20,95)
		self.password_txt.resize(240,25)
		self.login_btn = QPushButton("Login", self)
		self.login_btn.resize(100,30)
		self.login_btn.move(165,130)
		self.show()

class UIListBlogs(QWidget):
	def __init__(self, blogs, parent=None):
		super(UIListBlogs, self).__init__(parent)
		self.list_label = QLabel(self)
		self.list_label.setText("Select a blog below:")
		self.list_label.move(20,20)
		self.usernames = QListWidget(self)
		self.usernames.move(20,40)
		self.usernames.resize(240,130)
		for blog in blogs:
			self.usernames.addItem(blog);
		self.show()

class UIBlogStats(QWidget):
	def __init__(self, username, post_count, parent=None):
		super(UIBlogStats, self).__init__(parent)
		self.info_label = QLabel(self)
		self.info_label.setText("{}: {} posts".format(username, post_count))
		self.info_label.move(20,20)
		self.progress = QProgressBar(self)
		self.progress.setGeometry(20, 50, 320, 10)
		self.progress.setValue(0)
		self.clean_btn = QPushButton("Keep Orginal", self)
		self.clean_btn.move(15,70)
		self.clean_btn.resize(110,30)
		self.delete_btn = QPushButton("Delete All", self)
		self.delete_btn.move(125,70)
		self.delete_btn.resize(110,30)
		self.quit_btn = QPushButton("Quit", self)
		self.quit_btn.move(235,70)
		self.quit_btn.resize(110,30)
		self.show()

class UIMessage(QWidget):
	def __init__(self, message_text, parent=None):
		super(UIMessage, self).__init__(parent)
		self.message_label = QLabel(self)
		self.message_label.move(20,20)
		self.message_label.setText(str(message_text))
		self.show()

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.main_title = "TumblrCleaner 1.0"
		self.setWindowTitle(self.main_title)
		self.setWindowIcon(QIcon("icon.ico"))
		self.t = Tumblr()
		self.startTumblrLogin()

	def login_error_message(self):
		self.login_error_title = "Login Error"
		self.login_error = "Invalid login. More than two attempts will trigger captcha. Make sure to disable 2-step authenitcaton."
		QMessageBox.about(self, self.login_error_title, self.login_error)

	def logged_out_message(self):
		self.setGeometry(200,200,275,75)
		self.logged_out_text = "You were logged out.\nReopen the application and try again."
		self.logged_out = UIMessage(self.logged_out_text, self)
		self.setCentralWidget(self.logged_out)
		self.show()

	def major_error_message(self):
		self.setGeometry(200,200,275,75)
		self.major_error_text = "Something went wrong.\nReopen the application and try again."
		self.major_error = UIMessage(self.major_error_text, self)
		self.setCentralWidget(self.major_error)
		self.show()

	def done_message(self):
		self.setGeometry(200,200,230,60)
		self.done_text = "The posts have been deleted."
		self.done_ = UIMessage(self.done_text, self)
		self.setCentralWidget(self.done_)
		self.show()

	def startTumblrLogin(self):
		self.setGeometry(200,200,280,170)
		self.TumblrLogin = UITumblrLogin(self)
		self.setCentralWidget(self.TumblrLogin)
		self.TumblrLogin.login_btn.clicked.connect(self.tumblr_login)
		self.show()

	def startListBlogs(self):
		self.setGeometry(200,200,280,190)
		self.ListBlogs = UIListBlogs(self.t.blogs, self)
		self.setCentralWidget(self.ListBlogs)
		self.ListBlogs.usernames.itemClicked.connect(lambda: self.blog_stats(self.ListBlogs.usernames.currentItem().text()))
		self.show()

	def startBlogStats(self):
		self.BlogStats = UIBlogStats(self.t.username, self.t.post_count, self)
		self.setCentralWidget(self.BlogStats)
		self.BlogStats.quit_btn.clicked.connect(self.quit_app)
		self.setGeometry(200,200,360,110)
		self.BlogStats.clean_btn.clicked.connect(self.keep_original_posts)
		self.BlogStats.delete_btn.clicked.connect(self.delete_all_posts)
		self.show()

	def tumblr_login(self):
		self.TumblrLogin.email_txt.setDisabled(True)
		self.TumblrLogin.password_txt.setDisabled(True)
		self.TumblrLogin.login_btn.setDisabled(True)
		try:
			if self.t.login(self.TumblrLogin.email_txt.text(), self.TumblrLogin.password_txt.text()):
				self.t.all_blogs()
				self.startListBlogs()
			else:
				self.login_error_message()
				self.TumblrLogin.email_txt.setDisabled(False)
				self.TumblrLogin.password_txt.setDisabled(False)
				self.TumblrLogin.login_btn.setDisabled(False)
		except:
			self.major_error_message()

	def blog_stats(self, username):
		self.ListBlogs.usernames.setDisabled(True)
		self.t.set_username(username)
		try:
			self.pages = self.t.all_pages()
			self.t.form_key()
		except:
			if self.t.logged_in == False:
				self.logged_out_message()
			else:
				self.major_error_message()
		self.ListBlogs.usernames.setDisabled(False)
		self.startBlogStats()

	def keep_original_posts(self):
		self.clean_func = self.t.keep_original
		self.start_clean()
	
	def delete_all_posts(self):
		self.clean_func = self.t.delete_all
		self.start_clean()

	def start_clean(self):
		self.BlogStats.delete_btn.setDisabled(True)
		self.BlogStats.clean_btn.setDisabled(True)
		while self.t.pages >= 1:
			try:
				self.t.get_posts()
			except:
				if self.t.logged_in == False:
					self.logged_out_message()
				else:
					self.major_error_message()
			self.clean_func()
			if len(self.t.posts) > 100 or self.t.pages == 0:
				try:
					self.t.delete_posts()
				except:
					self.major_error_message()
				progress_bar = (self.pages - self.t.pages)/(self.pages/100)
				self.BlogStats.progress.setValue(progress_bar)
				if self.t.pages == 0:
					self.done_message()
	
	def quit_app(self):
		sys.exit()

def run():
	app = QApplication(sys.argv)
	w = MainWindow()
	sys.exit(app.exec_())

run()
