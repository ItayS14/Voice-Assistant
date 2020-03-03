import requests
import json

def main():
	test = Session()   
	print('Register: ', test.register('abc','asfdF123123411','jday.david.2002@gmail.com').text)
	print('Login: ', test.login('abc', 'asfdF123123411').text)
	#print('Request: ', request_reset_password(s,'jday.david.2002@gmail.com').text)
	#print('Reset: ', reset_password(s,'eyJ1c2VyX2lkIjoxfQ.XeqPBw.ZODG4SO9kGiQ8acGbptsAX3cOEU','212456724716714256471asdf78aA'))
	print('Profile: ', test.profile())
	
	print('Logout: ', test.logout())


class Session:
	def __init__(self, server_url = r'http://localhost:5000'):
		self.session = requests.Session()
		self.server_url = server_url

	def register(self, username, password, email):
		"""
		The function will register to the server
		:param username: username to register (str)
		:param password: password to register (str)
		:param email: email to register (str)
		:return: requests.Response
		"""
		register_data = {
			'username': username,
			'password': password,
			'email': email
		}
		return self.session.post(self.server_url + '/register', register_data)


	def login(self, auth, password):
		"""
		The function will login to the server
		:param auth: email or username (str)
		:param password: password for the user (str)
		:return: requests.Response
		"""
		login_data = {
			'auth': auth,
			'password': password,
		}

		return self.session.post(self.server_url + '/login', login_data)


	def logout(self):
		"""
		The function will logout a user from the server
		:return: requests.Response
		"""
		return self.session.get(self.server_url + '/logout')


	def request_reset_password(self,email):
		"""
		This function will ask for a password reset (send an email to the user)
		:param email: email to send the link to (str)
		:return: requests.response
		"""
		data = {
			'email':email
		}
		return self.session.post(self.server_url + "/password_reset",data)


	def reset_password(self, token, new_password):
		"""
		This function will reset the password with a token
		:param token: the validity token (str)
		:param new_password: the new password to change in the server (str)
		:return: requests.response
		"""
		data = {
			'password': new_password
		}
		return self.session.post(self.server_url + "/password_reset/" + token, data)

	def translate(self,text,dest_lang):
		"""
		This function will translate the text to the destination language
		:param text: the text to translate
		:param dest_lang: the language to translate into
		:return: the translated text (str)
		"""
		data = {
			'data': text,
			'dest_lang': dest_lang
		}
		translated = self.session.get(self.server_url + "/translate",params=data).text
		return json.loads(translated)[1] # [0] is True/False, [1] is the text
		
	def profile(self):
		"""
		The function will return a user's profile
		:return: details about the specific user (dict)
		"""
		return json.loads(self.session.get(self.server_url + '/profile').text)

if __name__ == '__main__':
	main()
