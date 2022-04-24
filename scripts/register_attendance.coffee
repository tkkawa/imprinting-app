module.exports = (robot) ->
  robot.respond /start/i, (msg)->	
    slack_user = msg.message.user.id;
    mode = "start"

    {PythonShell} = require('python-shell');

    execute_path = './scripts/register_attendance_and_leaving.py'
    options = {
      args:[
        '-param1', slack_user,
        '-param2', mode
      ]
    };

    pyshell = new PythonShell(execute_path, options);
    pyshell.send()
    pyshell.on('message', (message)->
      msg.send message
    ); 
