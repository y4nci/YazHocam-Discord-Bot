# YazHocam-Discord-Bot

This is a Discord bot based on the content on https://yazhocam.com/. The website has more than 140 articles written by more than 60 authors and is operated by METU Media Society, which is based in METU.

Since to run the code one must have the token for the Discord Application, you unfortunately cannot run the code.

If you could, you probably would want to install the modules discord and dotenv, if they're not previously installed in order to run the code.

  pip install discord

  pip install -U python-dotenv
  
Even though you can't run the code, you can add the bot to your server by clicking the link below.

  https://discord.com/api/oauth2/authorize?client_id=813836793531203655&permissions=0&scope=bot

Normally these bots run on the servers that run 7/24 and has huge features, but we don't have to do -and most probably won't need- this.

The bot -for now- has just a couple of functions.

  "yazdırhocam" command provokes the bot to send a random paragraph from one of the randomly chosen articles in YazHocam.
  
  "hangiyazı" command provokes the bot to send the link of the article which it chose the last quote it sent from.
  
  "10kelime {author name}" is the most complex command in the bot's catalogue. It provokes the bot to sort the words the author used the most in their articles. Bot sends the list in two versions, one includes conjunctions, prepositions etc. whereas the other list doesn't.

  "yardımhocam" is the command to see the help message.
  
Every week a new article is uploaded to the site which means new quotes worth to see, so updating the archive is highly important. Running updater.py does this elegantly.

To learn more about discord bots an find out how to make one, the site below is I think very useful. I suggest you to take a look at it if you're interested.
  
  https://realpython.com/how-to-make-a-discord-bot-python/
    
Enjoy!
