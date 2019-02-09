from tumblr import Tumblr
from os import system
from sys import stdout
from math import floor

def clear():
	system("cls")

class Main:
	def __init__(self):
		self.major_error = "[!] Something went wrong. Reopen the Program and try again."
		self.invalid_error = "[!] Invalid entry."
		self.logged_out_error = "[!] You were logged out. Reopen the application and try again."
		self.login_error = "[!] Invalid login. More than two attempts will trigger captcha. Make sure to disable 2-step authenitcaton."
		self.t = Tumblr()
		self.tumblr()

	def v(self):
		clear()
		print("+-------------------+--------------------+\n| TumblrCleaner 1.0 | [ctrl + c] to quit |\n+-------------------+--------------------+\n")

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
					self.v()
					print(self.login_error)
			except:
				self.v()
				print(self.major_error)
				self.quit()
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
				print(self.invalid_error)
		self.stats()

	def stats(self):
		self.v()
		print("Fetching stats...")
		try:
			self.pages = self.t.all_pages()
			self.t.form_key()
		except:
			self.v()
			if self.t.logged_in == False:
				print(self.logged_out_error)
				quit()
			else:
				print(self.major_error)
				quit()
		self.v()
		print("[{}] {} posts".format(self.t.username, self.t.post_count))
		self.clean()

	def clean(self):
		print("\n[0] Keep original\n[1] Delete all\n")
		while True:
			self.option = input("Select option: ")
			if self.option in [0,"0"]:
				self.clean_func = self.t.keep_original
				self.option_message = "Keeping original"
				break
			elif self.option in [1,"1"]:
				self.clean_func = self.t.delete_all
				self.option_message = "Deleting all"
				break
			else:
				print(self.invalid_error)
		self.delete()

	def delete(self):
		self.v()
		print("[{}:{}] {} posts\n".format(self.t.username, self.t.post_count, self.option_message))
		while self.t.pages >= 1:
			try:
				self.t.get_posts()
			except:
				self.v()
				if self.t.logged_in == False:
					print(self.logged_out_error)
					quit()
				else:
					print(self.major_error)
					quit()
			self.clean_func()
			if len(self.t.posts) > 100 or self.t.pages == 0:
				try:
					self.t.delete_posts()
				except:
					self.v()
					print(self.major_error)
					self.quit()
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

cleaner = Main()