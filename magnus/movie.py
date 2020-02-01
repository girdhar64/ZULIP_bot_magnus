import requests,json

class Movie(object):
	def about(self,text):
		baseurl = "http://omdbapi.com/?apikey=thewdb&t="
		response=(requests.get(baseurl+text)).json()
		# print(response)
		if(response['Response']=='False'):
			result = "Please Enter a correct movie name"
		else:
			result=response['Title']+ '\nImdb : '+str(response['imdbRating'])+ '\n Genre:'+str(response['Genre'])+ '\n year:'+str(response['Year'])
		# print(result)
		return result

# def main():
# mov = Movie()
# print(mov.about("Gdfather"))

# if __name__ == main:
	# main()
