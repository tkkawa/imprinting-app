module.exports = (robot) ->
  robot.respond /log (.*) (.*)/i, (msg)->	
    target_user = msg.match[1]
    date = msg.match[2]

    {PythonShell} = require('python-shell');

    execute_path = './scripts/read_working_time.py'
    options = {
      args:[
        '-param1', target_user,
        '-param2', date
      ]
    };

    pyshell = new PythonShell(execute_path, options);
    pyshell.send()
    pyshell.on('message', (message)->
      msg.send message
    ); 
