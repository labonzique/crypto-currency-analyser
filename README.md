# crypto-currency-analyser
Telegram bot which provides crypto currency's prices and gives a forecast of the currency movement.

  This product is an assistant bot for people involved in cryptocurrency, which will allow you to quickly and without much difficulty get the price 
of the cryptocurrency you are interested in, as well as get a forecast for the growth or fall of one of the main cryptocurrencies.
  
  At the moment, I have written the basic logic of the assistant’s work, as well as the logic of logging users and messages to the database 
(in the script, the token and access logs are taken from the auth file, but for security reasons, I removed this file in gitignore, 
you can see the scheme for filling the necessary logs in the constrains.py file).

  Now I am working on collecting the necessary data and then designing and fitting a neural network that will supposedly give predictions for 4-8 output neurons 
(from a strong fall to a strong currency growth) in percentage probabilities. 
For the final value, to which the forecast will be given, 24 hours and one week from the moment the forecast was received will be taken.
