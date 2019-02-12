from tumblr import Tumblr
from os import system
from sys import stdout
from math import floor

def clear():
	system("cls")

class Main:
	def __init__(self):
		self.t = Tumblr()
		self.tumblr()

	def v(self):
		clear()
		print("+-------------------+--------------------+\n| TumblrCleaner 1.0 | [ctrl + c] to quit |\n+-------------------+--------------------+\n")

	def invalid_error(self):
		invalid_error_message = "[!] Invalid entry."
		print(invalid_error_message)

	def login_error(self):
		self.v()
		login_error_message = "[!] Invalid login. Beware of captcha and 2-step authentication. If you keep getting this error, login through your browser then restart the program.\n"
		print(login_error_message)

	def major_error(self):
		self.v()
		major_error_message = "[!] Something went wrong. Reopen the Program and try again."
		print(major_error_message)
		self.quit()

	def tumblr(self):
		self.v()
		while True:
			print("Enter tumblr details\n")
			self.email = input("Email: ")
			self.password = input("Password: ")
			try:
				if self.t.login(self.email, self.password):
					break
				else:
					self.login_error()
			except:
				self.login_error()
		self.blogs()
	
	def blogs(self):
		self.v()
		print("Login successful!")
		print("Fetching blogs...")
		self.t.all_blogs()
		self.v()
		for i in range(len(self.t.blogs)):
			print("[{}] {}".format(i, self.t.blogs[i]))
		print("")
		while True:
			username = input("Enter the blog number: ")
			try:
				self.t.set_username(self.t.blogs[int(username)])
				break
			except:
				self.invalid_error()
		self.stats()

	def stats(self):
		self.v()
		print("Fetching stats...")
		try:
			self.pages = self.t.all_pages()
			self.t.form_key()
		except:
			self.major_error()
		self.v()
		print("[{}] {} posts".format(self.t.username, self.t.post_count))
		self.clean()

	def clean(self):
		print("\n[0] Keep original\n[1] Keep relevant\n[2] Delete all\n")
		while True:
			self.option = input("Select option: ")
			if self.option in [0,"0"]:
				self.clean_func = self.t.keep_original
				self.option_message = "Keeping original"
				break
			elif self.option in [1,"1"]:
				self.clean_func = self.t.keep_relevant
				self.option_message = "Keeping relevant"
				break
			elif self.option in [2,"2"]:
				self.clean_func = self.t.delete_all
				self.option_message = "Deleting all"
				break
			else:
				self.invalid_error()
		self.delete()

	def delete(self):
		self.v()
		print("[{}:{}] {} posts\n".format(self.t.username, self.t.post_count, self.option_message))
		while self.t.pages >= 1:
			try:
				self.t.get_posts()
			except:
				self.major_error()
			self.clean_func()
			if len(self.t.posts) > 100 or self.t.pages == 0:
				try:
					self.t.delete_posts()
				except:
					self.major_error()
			progress = (self.pages - self.t.pages)/(self.pages/100)
			percent = "[{}%] complete".format(int(floor(progress)))
			digits = len(percent)
			delete = "\b" * (digits)
			print("{0}{1:{2}}".format(delete, percent, digits), end="")
			stdout.flush()
			if self.t.pages == 0:
				break
		stdout.write("\n")
		print("All done!")
		self.quit()

	def quit(self):
		input("Type enter to quit")
		exit()

_ = Main()
