# linebot_test

> 在資料夾路徑那邊輸入 cmd

> 主要教學參考

> reply

https://github.com/yaoandy107/line-bot-tutorial

> post

https://medium.com/@lukehong/%E5%88%9D%E6%AC%A1%E5%98%97%E8%A9%A6-line-bot-sdk-eaa4abbe8d6e

> google API

https://console.developers.google.com/apis/dashboard?project=inlaid-way-203806&folder&organizationId&duration=PT1H

> Heroku CLI (安裝Heroku 環境)

https://devcenter.heroku.com/articles/heroku-cli

```javascript
85  git clone https://github.com/howarder3/linebot_test.git
86  git remote -v
92  git remote add heroku https://git.heroku.com/apriltestbot.git
95  brew install heroku/brew/heroku
96  heroku login
97  git push heroku master
98  git add .
99  git commit -m "ready to push"
100  git push heroku master
101  git remote -v
102  git push heroku master
103  git pull heroku
104  git branch
105  git push heroku master
106  git pull
107  git push heroku master
108  git push -f heroku master
109  git add .
110  git commit -m "fix"
111  git push -f heroku master
```

> google sheet API 參考文件

spreadsheetId/sheetId用法 與 取Sheet與範圍

https://developers.google.com/sheets/api/guides/concepts

> gspread library 與參考文件

https://github.com/burnash/gspread

> apriltestbot dictionary list

https://docs.google.com/spreadsheets/d/1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk/edit#gid=0


> heroku pip install

https://devcenter.heroku.com/articles/python-pip


> in cmd

```javascript
git remote
echo "# linebot_test" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/howarder3/linebot_test.git
git push -u origin master

git add .
git commit -m 'update readme'
git push origin master
git push heroku master

doskey /history
```

> git 雙push

https://yami.io/git-multiple-origin/
https://stackoverflow.com/questions/14290113/git-pushing-code-to-two-remotes

```javascript
查看目前所有的路徑：
$ git remote -v
(push) 意味著會被推送的遠端
(fetch) 則是可供拉回的遠端，一般只有一個 fetch。

新增一個 Origin 的遠端：
$ git remote set-url origin --push --add https://github.com/howarder3/linebot_test.git

再檢查一次：
$ git remote -v
```

> cmd history 指令

doskey /history

> VS code 註解快速鍵

Ctrl + /

> sublime 註解快速鍵

Ctrl + Shift + /

> notepad++ 註解快速鍵

Ctrl + Q

> python list

http://www.runoob.com/python/python-lists.html

> python string/字串處理

https://chusiang.gitbooks.io/using-python/content/String.html
https://www.dotnetperls.com/string-list-python

> python for 處理

http://www.runoob.com/python/python-for-loop.html

> python string contain

https://my.oschina.net/mickelfeng/blog/727010

> python string split

http://www.runoob.com/python/att-string-split.html

> python strip

http://python3-cookbook.readthedocs.io/zh_CN/latest/c02/p11_strip_unwanted_characters.html

> python random

隨機選取0到100間的偶數：

```javascript
import random
random.randrange(0, 101, 2)
```

https://dotblogs.com.tw/chris0920/2010/10/25/18560

> python random choose one item in list

```javascript
foo = ['a', 'b', 'c', 'd', 'e']
print(random.choice(foo))
```

> python list multi search

https://zhidao.baidu.com/question/488359074223051332.html

> python replace

http://www.runoob.com/python/att-string-replace.html

> python len

```javascript
len(items)
```

> python if

http://ez2learn.com/basic/if.html

> pyhton split

http://www.runoob.com/python/att-string-split.html

> python global variable

https://ephrain.net/python-%E5%9C%A8%E5%87%BD%E5%BC%8F%E8%A3%A1%E4%BD%BF%E7%94%A8%E5%85%A8%E5%9F%9F%E8%AE%8A%E6%95%B8%E8%A6%81%E5%8A%A0-global/

> python find list index

```javascript
index = list.index("object")
```
> python find in list

```javascript
3 in [1, 2, 3]
```

> python range

> range(10)        # 0-9 (不含10)

[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

> range(1, 11)     # 1-11 (不含11)

[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

> randint(0, 9) # 0-9(包含)

http://www.runoob.com/python/python-func-range.html
http://www.cnblogs.com/buro79xxd/archive/2011/05/23/2054493.html

> Heroku Scheduler

https://devcenter.heroku.com/articles/scheduler

> git 多人合作

http://tech-marsw.logdown.com/blog/2013/08/17/git-notes-github-n-person-cooperation-settings

> git branch

https://ihower.tw/blog/archives/2620
https://git-scm.com/book/zh-tw/v1/Git-%E5%88%86%E6%94%AF-%E4%BD%95%E8%AC%82%E5%88%86%E6%94%AF
