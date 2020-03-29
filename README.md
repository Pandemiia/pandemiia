# Pandemiia
Pandemiia is an open source supply chain platform where hospitals fighting coronavirus on site may request extra supplies from volunteers, local businesses, charities or government organizations.

https://pandemiia.herokuapp.com

# Tech stack
Pipenv, Django, Bootstrap, Heroku

# How to run the Django project locally
1. First, install pipenv to manage dependencies in virtual environment
`pip install pipenv`
2. Install dependencies from Pipfile
`pipenv install`
3. Enter a virtual environment
`pipenv shell`
PS. To add a dependency in Pipfile you may run `pipenv install` or if you need to specify version `pipenv install "django>=3.0.3"`

# How to deploy on Heroku
First, you need to login into your Heroku account from the CLI client.
`heroku login`
Then you add Heroku remote to your local repo. 
`heroku git:remote -a pandemiia`
Voila! Now you can deploy by pushing to master on Heroku.
`git push heroku master`

If you need to deploy a branch please use `git push heroku testbranch:master`
More details on Heroku - https://devcenter.heroku.com/articles/git
