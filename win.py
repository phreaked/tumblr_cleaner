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
		self.info_label.resize(250,20)
		self.progress = QProgressBar(self)
		self.progress.setGeometry(20, 40, 250, 30)
		self.progress.setValue(0)
		self.original_btn = QPushButton("Keep orginal", self)
		self.original_btn.move(20,80)
		self.original_btn.resize(120,30)
		self.relevant_btn = QPushButton("Keep relevant", self)
		self.relevant_btn.move(150,80)
		self.relevant_btn.resize(120,30)
		self.delete_btn = QPushButton("Delete all", self)
		self.delete_btn.move(20,120)
		self.delete_btn.resize(120,30)
		self.quit_btn = QPushButton("Quit", self)
		self.quit_btn.move(150,120)
		self.quit_btn.resize(120,30)
		self.show()

class statsThread(QThread): 
	signal = pyqtSignal("PyQt_PyObject")
	def __init__(self, tumblr):
		QThread.__init__(self)
		self.t_ = tumblr
		self.username = ""

	def run(self):
		self.t_.set_username(self.username)
		try:
			pages = self.t_.all_pages()
			self.t_.form_key()
		except:
			pages = ""
		self.signal.emit(pages)

class loginThread(QThread):
	signal = pyqtSignal("PyQt_PyObject")
	def __init__(self, tumblr):
		QThread.__init__(self)
		self.t_ = tumblr
		self.email = ""
		self.password = ""

	def run(self):
		try:
			login = self.t_.login(self.email, self.password)
			self.t_.all_blogs()
		except:
			login = False
		self.signal.emit(login)

class cleanThread(QThread):
	signal = pyqtSignal("PyQt_PyObject")
	def __init__(self, tumblr):
		QThread.__init__(self)
		self.t_ = tumblr
		self.cleaner = ""

	def run(self):
		deleted = True
		try:
			self.t_.get_posts()
			self.cleaner()
			if len(self.t_.posts) > 100 or self.t_.pages == 0:
				self.t_.delete_posts()
		except:
			deleted = False
		self.signal.emit(deleted)

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.main_title = "TumblrCleaner 1.0"
		self.loading_title = "Loading..."
		self.setWindowTitle(self.main_title)
		self.t = Tumblr()
		self.startTumblrLogin()

	def login_error(self):
		login_error_title = "Login Error"
		login_error_message = "Invalid login. More than two attempts will trigger captcha. Make sure to disable 2-step authenitcaton."
		QMessageBox.information(self, login_error_title, login_error_message)

	def major_error(self):
		major_error_title = "Error"
		major_error_message = "Something went wrong. Reopen the application and try again."
		QMessageBox.critical(self, major_error_title, major_error_message)
		self.quit()

	def done(self):
		done_title = "All Done"
		done_message = "The posts have been deleted."
		QMessageBox.information(self, done_title, done_message)
		self.quit()
	
	def startTumblrLogin(self):
		self.setGeometry(200,200,280,190)
		self.TumblrLogin = UITumblrLogin(self)
		self.setCentralWidget(self.TumblrLogin)
		self.tumblr_login_thread = loginThread(self.t)
		self.tumblr_login_thread.signal.connect(self.tumblr_login_done)
		self.TumblrLogin.login_btn.clicked.connect(self.tumblr_login)
		self.show()

	def startListBlogs(self):
		self.ListBlogs = UIListBlogs(self.t.blogs, self)
		self.setCentralWidget(self.ListBlogs)
		self.blog_stats_thread = statsThread(self.t)
		self.blog_stats_thread.signal.connect(self.blog_stats_done)
		self.ListBlogs.usernames.itemClicked.connect(self.blog_stats)
		self.show()

	def startBlogStats(self):
		self.setGeometry(200,200,290,170)
		self.BlogStats = UIBlogStats(self.t.username, self.t.post_count, self)
		self.setCentralWidget(self.BlogStats)
		self.clean_thread = cleanThread(self.t)
		self.clean_thread.signal.connect(self.clean_done)
		self.BlogStats.quit_btn.clicked.connect(self.quit)
		self.BlogStats.original_btn.clicked.connect(self.keep_original_posts)
		self.BlogStats.relevant_btn.clicked.connect(self.keep_relevant_posts)
		self.BlogStats.delete_btn.clicked.connect(self.delete_all_posts)
		self.show()

	def tumblr_login(self):
		self.setWindowTitle(self.loading_title)
		self.TumblrLogin.email_txt.setDisabled(True)
		self.TumblrLogin.password_txt.setDisabled(True)
		self.TumblrLogin.login_btn.setDisabled(True)
		self.tumblr_login_thread.email = self.TumblrLogin.email_txt.text()
		self.tumblr_login_thread.password = self.TumblrLogin.password_txt.text()
		self.tumblr_login_thread.start()

	def tumblr_login_done(self, login):
		self.setWindowTitle(self.main_title)
		if login:
			self.startListBlogs()
		else:
			self.login_error()
			self.TumblrLogin.email_txt.setDisabled(False)
			self.TumblrLogin.password_txt.setDisabled(False)
			self.TumblrLogin.login_btn.setDisabled(False)

	def blog_stats(self, username):
		self.setWindowTitle(self.loading_title)
		self.ListBlogs.usernames.setDisabled(True)
		self.blog_stats_thread.username = self.ListBlogs.usernames.currentItem().text()
		self.blog_stats_thread.start()
		
	def blog_stats_done(self, pages):
		self.setWindowTitle(self.main_title)
		if pages != "":
			self.pages = pages
			self.startBlogStats()
		else:
			self.major_error()

	def keep_original_posts(self):
		self.clean_thread.cleaner = self.t.keep_original
		self.clean_title = "Keeping original"
		self.start_clean()

	def keep_relevant_posts(self):
		self.clean_thread.cleaner = self.t.keep_relevant
		self.clean_title = "Keeping relevant"
		self.start_clean()
	
	def delete_all_posts(self):
		self.clean_thread.cleaner = self.t.delete_all
		self.clean_title = "Deleting all"
		self.start_clean()

	def start_clean(self):
		self.BlogStats.original_btn.setDisabled(True)
		self.BlogStats.relevant_btn.setDisabled(True)
		self.BlogStats.delete_btn.setDisabled(True)
		self.BlogStats.info_label.setText("[{}:{}] {} posts".format(self.t.username, self.t.post_count, self.clean_title))
		self.clean()

	def clean(self):
		self.clean_thread.start()

	def clean_done(self, deleted):
		if deleted:
			progress_bar = (self.pages - self.t.pages)/(self.pages/100)
			self.BlogStats.progress.setValue(progress_bar)
			if self.t.pages == 0:
				self.done()
			else:
				self.clean()
		else:
			self.major_error()
	
	def quit(self):
		sys.exit()

def run():
	app = QApplication(sys.argv)
	w = MainWindow()
	sys.exit(app.exec_())

run()
