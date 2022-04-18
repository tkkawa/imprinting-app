module.exports = (robot) ->

   robot.respond /c/i, (msg) ->
     console.log('BBB')
     msg.send "bbb"
