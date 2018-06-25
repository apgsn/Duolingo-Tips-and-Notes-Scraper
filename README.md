# Duolingo-Tips-and-Notes-Scraper
<p>
A simple Python 3 web scraper. After accessing your [Duolingo](https://www.duolingo.com) account, it scans the page looking for unlocked lessons that have tips and notes to download, then it puts them all together in a single HTML file.
The script uses Firefox and [Selenium](https://github.com/SeleniumHQ).
</p>
<h3>How to use</h3>
<p>
After making sure you have Firefox and Selenium correctly installed, set Duolingo's home page on the course you want the notes of, then close your browser. Open the script, write your username and password in their respective fields and execute it. Let the bot do its thing without interacting with the pages it opens nor minimizing the window, it can take up to three minutes to scrape a whole course tree. Please note that the bot won't be able to scrape locked lessons.
Once it's done, there should be an HTML page complete with all of the course's tips and notes the bot was able to find. The file <code>embed.css</code> contains some CSS code I wrote to improve its readability, the script will automatically embed it to the page if both files are located in the same directory, but it's not necessary for it to work properly.
</p>
<h3>Getting stuck?</h3>
<p>
Duolingo is a project in constant evolution, and the name, position and numerosity of page elements is bound to change from time to time.
If the bot seems to be stuck at some point, check if the XPaths of the elements it's trying to process have been changed, and modify their related fields accordingly. Pay attention to the difference between absolute and relative paths!
If you have loading issues (slow connection), change <code>loginDelay</code> and <code>stepDelay</code> to bigger values, hopefully the bot will go slower and work fine.
For anything else, just give me a holler.
</p>
