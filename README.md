# imprinting-app
## Install Hubot in Slack
You first need to install Hubot in Slack. See the following article.

https://qiita.com/shosho/items/057d7b67d1dd3a700554#3-slack%E3%81%A8%E9%80%A3%E6%90%BA%E3%81%99%E3%82%8B
## Installation Steps
1. clone
```sh
$ git clone git@github.com:tkkawa/imprinting-app.git
```

2. environment setup

The names of the docker image and container are specified by constants described in docker/env.sh.
These constants can be edited to suit your project.
```sh
$ cd imprinting-app
$ cp docker/.env.sh docker/env.sh
$ sh docker/build.sh
$ sh docker/run.sh
$ sh docker/exec.sh
```
## Run demo
1. Run Hubot

You can use the command:
```
$ sh hubot.sh
```
2. Register username

You will need to link your slack id to your username. You can use the command on Slack:
```
@{HUBOT NAME} username {username}
```
3. Register attendance and leaving

You can use the command on Slack to register attendance and leaving:
```
@{HUBOT NAME} start
```
```
@{HUBOT NAME} end
```
4. Read working time


You can use the command on Slack to read working time by specify username and date:
```
@{HUBOT NAME} log {username} {date}
```
