from linkedin import linkedin

# Define CONSUMER_KEY, CONSUMER_SECRET,  
# USER_TOKEN, and USER_SECRET from the credentials 
# provided in your LinkedIn application

CONSUMER_KEY = '770iuq17p7d42x'
CONSUMER_SECRET = 'NWnWfTuuhyp9OPp8'
USER_TOKEN = 'e792f288-5d79-4465-a036-29eb8b9cb3b7'
USER_SECRET = 'bebea788-22cc-466e-8257-1b55568fdf02'
RETURN_URL = 'http://www.cs.stonybrook.edu/~hkshah/'



# Instantiate the developer authentication class

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                                          USER_TOKEN, USER_SECRET, 
                                                          RETURN_URL, linkedin.PERMISSIONS.enums.values())

# Pass it in to the app...

application = linkedin.LinkedInApplication(authentication)

# Use the app....

print application.get_profile()
