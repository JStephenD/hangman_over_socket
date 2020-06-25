# Hangman Over Socket

![logo](/images/demo.png)

## How to install and run:

1. clone/download repository <br>
2. cd into repository (terminal of your choosing)

```$ pip install pipenv```
> 3.&nbsp;install pipenv for environment management, be sure to be in the correct directory

```[in cloned] $ pipenv install```

> 4.&nbsp;install the modules required

5. open two terminals

```[in cloned] (1) $ pipenv run python server.py```

> launch server.py and wait for server to listen 

```[in cloned] (2) $ pipenv run python client.py```

> launch client.py and you're good to go

## Gameplay

Desktop Browser | Phone Browser
--------------- | -------------
ctrl click on the link provided by client.py | goto \<ipadd\>:5050
or go to \<ipadd\>:5050 | 
\# guess the word | \# guess the word

> ipadd = ip address of the computer running client.py