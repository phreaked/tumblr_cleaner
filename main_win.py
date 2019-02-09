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
		self.email_txt.resize(240,30)
		self.password_label = QLabel(self)
		self.password_label.setText("Tumblr Password:")
		self.password_label.move(20,80)
		self.password_txt = QLineEdit(self)
		self.password_txt.move(20,100)
		self.password_txt.resize(240,30)
		self.login_btn = QPushButton("Login", self)
		self.login_btn.resize(240,30)
		self.login_btn.move(20,140)
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
		self.progress.setGeometry(20, 40, 260, 30)
		self.progress.setValue(0)
		self.clean_btn = QPushButton("Keep Orginal", self)
		self.clean_btn.move(20,80)
		self.clean_btn.resize(80,30)
		self.delete_btn = QPushButton("Delete All", self)
		self.delete_btn.move(110,80)
		self.delete_btn.resize(80,30)
		self.quit_btn = QPushButton("Quit", self)
		self.quit_btn.move(200,80)
		self.quit_btn.resize(80,30)
		self.show()

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.main_title = "TumblrCleaner 1.0"
		self.load_title = "Loading..."
		self.setWindowTitle(self.main_title)
		self.setWindowIcon(QIcon("icon.ico"))
		self.t = Tumblr()
		self.startTumblrLogin()

	def login_error_message(self):
		self.login_error_title = "Login Error"
		self.login_error = "Invalid login. More than two attempts will trigger captcha. Make sure to disable 2-step authenitcaton."
		QMessageBox.about(self, self.login_error_title, self.login_error)

	def logged_out_message(self):
		self.logged_out_title = "Logged Out"
		self.logged_out = "You were logged out. Reopen the application and try again."
		QMessageBox.about(self, self.logged_out_title, self.logged_out)
		self.quit_app()

	def major_error_message(self):
		self.major_error_title = "Tumblr Error"
		self.major_error = "Something went wrong. Reopen the application and try again."
		QMessageBox.about(self, self.major_error_title, self.major_error)
		self.quit_app()

	def done_message(self):
		self.done_title = "All Done"
		self.done_ = "The posts have been deleted."
		QMessageBox.about(self, self.done_title, self.done_)
		self.quit_app()
	
	def startTumblrLogin(self):
		self.setGeometry(200,200,280,170)
		self.TumblrLogin = UITumblrLogin(self)
		self.setCentralWidget(self.TumblrLogin)
		self.TumblrLogin.login_btn.clicked.connect(self.tumblr_login)
		self.show()

	def startListBlogs(self):
		self.ListBlogs = UIListBlogs(self.t.blogs, self)
		self.setCentralWidget(self.ListBlogs)
		self.ListBlogs.usernames.itemClicked.connect(lambda: self.blog_stats(self.ListBlogs.usernames.currentItem().text()))
		self.show()

	def startBlogStats(self):
		self.BlogStats = UIBlogStats(self.t.username, self.t.post_count, self)
		self.setCentralWidget(self.BlogStats)
		self.BlogStats.quit_btn.clicked.connect(self.quit_app)
		self.setGeometry(200,200,300,130)
		self.BlogStats.clean_btn.clicked.connect(self.keep_original_posts)
		self.BlogStats.delete_btn.clicked.connect(self.delete_all_posts)
		self.show()

	def tumblr_login(self):
		self.setWindowTitle(self.load_title)
		self.TumblrLogin.email_txt.setDisabled(True)
		self.TumblrLogin.password_txt.setDisabled(True)
		self.TumblrLogin.login_btn.setDisabled(True)
		try:
			if self.t.login(self.TumblrLogin.email_txt.text(), self.TumblrLogin.password_txt.text()):
				self.t.all_blogs()
				self.startListBlogs()
				self.setWindowTitle(self.main_title)
			else:
				self.login_error_message()
				self.setWindowTitle(self.main_title)
				self.TumblrLogin.email_txt.setDisabled(False)
				self.TumblrLogin.password_txt.setDisabled(False)
				self.TumblrLogin.login_btn.setDisabled(False)
		except:
			self.major_error_message()

	def blog_stats(self, username):
		self.setWindowTitle(self.load_title)
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
		self.setWindowTitle(self.main_title)
		self.ListBlogs.usernames.setDisabled(False)
		self.startBlogStats()

	def keep_original_posts(self):
		self.clean_func = self.t.keep_original
		self.setWindowTitle("Keeping Original")
		self.start_clean()
	
	def delete_all_posts(self):
		self.clean_func = self.t.delete_all
		self.setWindowTitle("Deleting All")
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
