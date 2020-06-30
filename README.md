# chessbot
discord bot for chess

# What it does currently
- allow for two players in a discord chat to play chess
- each move will display an image updated with your current move
- the bot will tell you if you make illegal moves/out of turn moves
- adheres to strict syntax i.e. (nc5 must be Nc5)
- allows players to resign (whether on their turn or not) and allows players to offer draws (on their own turn)

# What it should do in the future
- a !help command listing out valid commands
- a way to store games for persisent storage/multiple games at once in a discord room
- a way to keep track of win/loss against a certain user
- a command to show the notation of a match

### Note

note that this is a fork of [taylor zheng's](https://github.com/taylorzhang2/chessbot) chessbot. I needed one and found his, but had to update it to so that it worked with the latest revisions to the discord api (the rewrite -- the project hadn't been committed to in three years). I ended up doing a little more than just that, and ended up with functionality for resignation and draws. other changes I implemented were making the bot edit a message instead of making new ones to prevent spam, making the bot delete move messages (and its own warning messages), and making the current position function more... functional.
