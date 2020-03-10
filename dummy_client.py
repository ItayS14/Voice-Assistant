import requests
import json

def main():
	test = Session()   
	#print('Register: ', test.register('abc','asfdF123123411','jday.david.2002@gmail.com').text)
	#print('Login: ', test.login('abc', 'Aa1234567').text)
	#print('Profile: ', test.profile())
	#print('Password reset Request', test.reset_password_request('jday.david.2002@gmail.com'))
	#print('Password reset code', test.password_reset('Q5239L','jday.david.2002@gmail.com'))
	#print('New password: ', test.new_password('eyJ1c2VyX2lkIjoxfQ.XmAwMg.552pVgu2_gg4x0mpWj4rd_tbhjw','Aa1234567'))
	print('Calculate:', test.calculate('5 + 5'))
	#print('Logout: ', test.logout())


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

	def reset_password_request(self, email):
		"""
		This function will create a password reset request for a user
		:param email: the mail to send the code to
		:return: None
		"""
		data = {
			'email' : email
		}
		return json.loads(self.session.post(self.server_url + '/get_password_reset_token', data).text)

	def password_reset(self, code, email):
		"""
		This function sends the given reset code to the server and recieves a token in response
		:param code: the code the client enters (str)
		:param email: the email of the user (str)
		:return: the token given by the server used to authenticate (str)
		"""
		data = {
			'code' : str(code),
			'email': email
		}
		return json.loads(self.session.post(self.server_url + '/validate_code', data).text)

	def new_password(self, token, password):
		"""
		This function will update a user's password using the token he got in the last level
		:param token: the token to use to authenticate (str)
		:param password: the new password which the client chose (str)
		:return: None
		"""
		data = {
			'password': password
		}
		return json.loads(self.session.post(self.server_url + '/new_password/' + token,data).text)
	
	def calculate(self, expression):
		"""
		This function will calculate the result of a mathematical expression
		:param expression: the mathematical expression to be calculated (str)
		:return: the value of the expression (int)
		"""
		data = {
			'expression': expression
		}
		return json.loads(self.session.get(self.server_url + '/calculate',params=data).text)
	
if __name__ == '__main__':
	main()
