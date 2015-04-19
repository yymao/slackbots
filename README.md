# slackbots
useful custom slash commands for slack

These scripts will be called by a common interface with slack.
To create a new bot, you can create a python moudle which has a function named `program`. 
The `program` function should take one argument, and return a string. 
The argument would be a dict-like object, and it contains the data passed by slack slash command. The key `'text'` is probably the one you need. 
