module.exports = (robot) ->
  #robot.respond /username (.*)/i, (msg)->	
  robot.respond /AAA/i, (msg)->	
    console.log('TRUE')
    slack_user = msg.message.user.id;
    username = msg.match[1]

    {PythonShell} = require('python-shell');

    execute_path = './src/register_username.py'
    options = {
      args:[
        '-param1', slack_user
        '-param2', username
      ]
    };

    pyshell = new PythonShell(execute_path, options);
    pyshell.send()
    pyshell.on('message', (message)->
      msg.send message
    ); 
