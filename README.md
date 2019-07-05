# web-to-slack

**This project is just proof of concept. It's not production ready, I took some
shortcuts to make things easier to implement. Use it at your own risk.**

## What is web-to-slack?

It's a project that allows your website to talk to Slack. It utilises websockets,
pubsub messaging and Slack bot to achieve its goal. In theory each part is
independent and can be updated without disturbing other components, e.g. you
could replace Redis with Rabbit MQ and project would still work. At the moment
such change is possible but requires additional work.

## How to use it?

- create slack channel named **client-notifications**
- create Slack bot with access to chanel messages (if you want to run it on you 
local machine you will need to expose Slack bot, best option for that is to use
ngrok)
- clone this repository
- run `docker-compose up -d`
- run `client.html` file in your browser


## TODO

I'm going to improve this project and implement new features but it won't happen
overnight. Got other things to work on, this project is more like a hobby.

- create separate Slack channels for each user
- create message broker factory (allow to change messaging part without touching
the code)
- create config file to keep all hardcoded stuff (channel names, broker name, etc.)
- create proper docs
