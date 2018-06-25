import time, re
from selenium import webdriver

username = 'your_username'
password = 'your_password'
url = 'https://www.duolingo.com'
userAbsXPath = '/html/body/div[1]/div/div[1]/div/div[1]/div[3]/span[1]'
langAbsXPath = '/html/body/div[1]/div/div[1]/div/div[1]/div[1]/span[2]'
unitAbsXPath = '/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/div/a/div'
notesAbsXPath = '/html/body/div[1]/div/div[2]/div'
notesTitleRelXPath = 'div[1]/div/div[2]/div[1]'
loginDelay = 10
stepDelay = .3
rgxButtons = re.compile(r'<button.*?\/button>')
rgxClass = re.compile(r'\Wclass="(?!chapter|title).*?"')

print('Loading page...')
driver = webdriver.Firefox()
driver.get(url)
# login
driver.implicitly_wait(loginDelay)
print('Logging in as %s...' % username)
driver.find_element_by_id('sign-in-btn').click()
driver.find_element_by_id('top_login').send_keys(username)
driver.find_element_by_id('top_password').send_keys(password)
driver.find_element_by_id('login-button').click()
driver.implicitly_wait(loginDelay)
try :
    if driver.find_element_by_xpath(userAbsXPath).get_attribute('innerHTML') == username :
        print('Successfully logged in.')
    else :
        raise Exception('Error: could not verify user.')
except :
    print('Error while logging in.')
    driver.quit()
    quit()

# setting up html file
lang = driver.find_element_by_xpath(langAbsXPath).get_attribute('innerHTML')
pageTitle = 'Duolingo - %s Tips and Notes' % lang
htmlFile = open(pageTitle + '.html', 'w')
htmlFile.write('<!DOCTYPE html><html><head><title>' + pageTitle + '</title><meta charset="utf-8">')
try :
    cssFile = open('embed.css')
    css = cssFile.read()
    cssFile.close()
except :
    print('Warning: error while opening CSS file.')
    css = ''
htmlFile.write('<style media="screen" type="text/css">' + css + '</style></head>')
htmlFile.write('<body><h1>Duolingo: %s</h1><h2>Tips and notes</h2>' % lang)

unitsCount = len(driver.find_elements_by_xpath(unitAbsXPath))
print(str(unitsCount) + " lessons found.")
print('Scraping %s tips and notes...' % lang)
for n in range(0, unitsCount) :
    # selecting nth unit
    driver.find_element_by_xpath(userAbsXPath).click()
    units = driver.find_elements_by_xpath(unitAbsXPath)
    units[n].click()
    time.sleep(stepDelay)
    # clicking on tips & notes (if available)
    popupButtons = units[n].find_elements_by_tag_name('button')
    if not len(popupButtons) :
        print('No more unlocked lessons to process.')
        break
    foundTips = False
    for b in popupButtons :
        if b.get_attribute('innerHTML').find('lightbulb') != -1 : # lightbulb button = notes link
            foundTips = True
            b.click()
            break
    if not foundTips :
        print('No notes available for unit ' + str(n + 1))
        continue
    print('Now processing unit ' + str(n + 1))
    time.sleep(stepDelay)
    # scraping notes and heading back to tree
    htmlFile.write('<h4 class="chapter">Unit ' + str(n + 1) + '</h4>')
    content = driver.find_element_by_xpath(notesAbsXPath)
    notesTitleClass = content.find_element_by_xpath(notesTitleRelXPath).get_attribute('class')
    content = content.get_attribute('innerHTML')
    content = content.replace(notesTitleClass, 'title')
    content = content.replace('Tips and notes', '')
    for r in rgxButtons.findall(content) :
        content = content.replace(r, '')
    for r in rgxClass.findall(content) :
        content = content.replace(r, '')
    htmlFile.write(content)
    driver.back()
    time.sleep(stepDelay)

htmlFile.write('</body></html>')
htmlFile.close()
driver.quit()
print('Program terminated.')
