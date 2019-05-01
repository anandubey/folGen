from .models import Credential
from user.models import User
from django.contrib import messages
from hashlib import sha256


def get_hash(raw_password, salt=""):
    hashable_string = raw_password + salt
    return sha256(hashable_string.encode('utf-8')).hexdigest()


def authenticate(request):
    username_entered = request.POST['username']
    password_entered = request.POST['password']

    try:
        credential_instance = Credential.objects.get(username=username_entered)
        user_instance = User.objects.get(username=username_entered)
        password_hash = get_hash(password_entered, user_instance.unique_id)
        if password_hash != credential_instance.password_hash:
            return False
        else:
            return True
    except Credential.DoesNotExist:
        return False


def login(request):
    username_entered = request.POST['username']
    request.session['username'] = username_entered
    request.session['logged'] = True
    timeout = 0
    try:
        loginState = request.POST.get('savelogin')
        if loginState is not None:
            timeout = 2592000
    finally:
        request.session.set_expiry(timeout)



def logout(request):
    messages.info(request, '2')
    request.session.clear()




def __next_lexicographic_word(word):
	lowercase_word = word.lower()
	lowercase_ordinals_list = []

	# In case we reach end of dictionary
	if set(lowercase_word) == {'z'}:
		return False
        
	else:
		lowercase_ordinals_list = list(map(ord, list(lowercase_word))) 		# Returns list of ASCII characters in lowercase_word
		for position in range(len(lowercase_word)-1, -1, -1):
			if lowercase_ordinals_list[position] == 122:
				continue													# If current letter is 'z' then move to the next letter at left side
			else:
				lowercase_ordinals_list[position] += 1						# Increase the letter by one
				break
		next_word_letters_list = list(map(chr,lowercase_ordinals_list))		# Convert ASCII list to character list
		next_word = ''.join(next_word_letters_list)							# Convert character list to string
		return next_word


def get_unique_id(deletedUIDlist, activeUIDlist):
	if len(deletedUIDlist) is not 0:
		return(min(deletedUIDlist))											# If there are deleted user IDs, return the lexicographically smallest
	elif len(activeUIDlist) is not 0:
		return (__next_lexicographic_word(str(max(activeUIDlist)[0])))				# If no deleted user IDs, return an ID higher than the max of active ID
	else:
		return 'aaa'														# For first ever user ID

