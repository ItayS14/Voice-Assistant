import requests
import json
import base64

def main():
	test = Session()   
	# print('Register: ', test.register('abc','asfdF123123411','it.shirizly@gmail.com'))
	print('Login: ', test.login('abc', 'asfdF123123411'))
	#print('update img:', test.update_picture('sadf.txt'))
	#print('Profile: ', test.profile())
	#print('Password reset Request', test.reset_password_request('jday.david.2002@gmail.com'))
	#print('Password reset code', test.password_reset('Q5239L','jday.david.2002@gmail.com'))
	#print('New password: ', test.new_password('eyJ1c2VyX2lkIjoxfQ.XmAwMg.552pVgu2_gg4x0mpWj4rd_tbhjw','Aa1234567'))
	#print('Calculate:', test.calculate('5 + 5'))
	#print('Translate:', test.translate('Hello world','HE'))
	#print('Search: ', test.search('Who is the author of Game Of Thrones?','game of thrones'))
	#print('Parse: ', test.parse('who is the author of game of thrones?'))
	print(test.server_features(test.parse('who is the authoer of game of Thrones')))
	print(test.server_features(test.parse('Exchange 4 euros to shekels')))
	print(test.server_features(test.parse('Translate hello world to spanish')))
	print(test.server_features(test.parse('How much is 3 + 3')))
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
		return self.session.post(self.server_url + '/register', register_data).json()

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

		return self.session.post(self.server_url + '/login', login_data).json()

	def logout(self):
		"""
		The function will logout a user from the server
		:return: requests.Response
		"""
		return self.session.get(self.server_url + '/logout').json()

	def translate(self,text,dest_lang):
		"""
		This function will translate the text to the destination language
		:param text: the text to translate
		:param dest_lang: the language to translate into
		:return: the translated text (str)
		"""
		data = {
			'text': text,
			'lang': dest_lang
		}
		return  self.session.get(self.server_url + "/translate",params=data).json()
		
	def profile(self):
		"""
		The function will return a user's profile
		:return: details about the specific user (dict)
		"""
		return self.session.get(self.server_url + '/profile').json()

	def reset_password_request(self, email):
		"""
		This function will create a password reset request for a user
		:param email: the mail to send the code to
		:return: None
		"""
		data = {
			'email' : email
		}
		return self.session.post(self.server_url + '/get_password_reset_token', data).json()

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
		return self.session.post(self.server_url + '/validate_code', data).json()

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
		return self.session.post(self.server_url + '/new_password/' + token,data).json()
	
	def calculate(self, expression):
		"""
		This function will calculate the result of a mathematical expression
		:param expression: the mathematical expression to be calculated (str)
		:return: the value of the expression (int)
		"""
		data = {
			'expression': expression
		}
		return self.session.get(self.server_url + '/calculate',params=data).json()
	
	def exchange(self, from_coin, to_coin, amount):
		"""
		The function will exchange a coin
		:param from_coin: the old currency (str)
		:param to_coin: the currency to change to (str)
		:param amount: the amount to change (int)
		"""
		data = {
			'from_coin' : from_coin,
			'to_coin': to_coin,
			'amount': amount
		}
		return self.session.get(self.server_url + '/exchange', params=data).json()


	def search(self, question,keywords):
		"""
		This function will search a certain expression in wikipedia
		:param text: the text to search on wikipedia (str)
		:return: the answer from wikipedia search about the term (str) 
		"""
		return self.session.get(self.server_url + f'/search?question={question}&keywords={keywords}').json()

	def parse(self, text):
		"""
		Thhe function will parse a query
		:param text: the string to parse (str)
		:return: the answer from the parse route in the server (str)
		"""
		return self.session.get(self.server_url + f'/parse/{text}').json()

	def update_picture(self, picture_path):
		"""
		The function will upload a picture to the server
		:param picture_path: path to the picture to upload (str)
		:return: the answer from the update_img route of the server (str)
		"""
		with open(picture_path, 'rb') as f:
			content = f.read()
		content = base64.b64encode(content).decode('ascii')
		data =  {
			'img': content,
			'file_name': picture_path.split('/')[-1]
		}
		return self.session.post(self.server_url + '/update_img', data)

	def server_features(self, server_response):
		"""
		The fucntion will go to the route from the server_response
		:param server_response: response of the server from the parse function
		:return: result of the command (str)
		"""
		if not server_response[0]:
			return 'Action is not valid' + str(server_response)
		return self.session.get(server_response[1]['route'], params=server_response[1]['params']).json()
if __name__ == '__main__':
	main()
