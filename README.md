# Pandemiia
Pandemiia is an open source supply chain platform where hospitals fighting coronavirus on site may request extra supplies from volunteers, local businesses, charities or government organizations.

https://pandemiia.herokuapp.com https://pandemiia.in.ua/

Our public roadmap -  https://www.notion.so/03ff6e7ece2d45e38eae9abb7f19e640?v=16c0b45807b84291970b7621bd566b87

# Tech stack
Pipenv, Django, Bootstrap, Amazon Web Services, GoogleMaps

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
