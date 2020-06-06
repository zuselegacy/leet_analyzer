import sys
from bs4 import BeautifulSoup
from collections import OrderedDict
import itertools
import pprint

problemMap = {}

def tagCount():
    tagMap = {}
    tags = [tag for problemProperty in problemMap.values() for tag in problemProperty["tags"]]
    for tag in tags:
        tagMap[tag] = tagMap.get(tag,0) + 1
    dd = OrderedDict(sorted(tagMap.items(), key=lambda x: x[1]))
    pprint.pprint(dd,width=1)
    pass

def tagCountNgram(count=2):
    tagMap = {}
    combinations = [combination for problemProperty in problemMap.values() for combination in list(itertools.combinations(problemProperty["tags"], count))]
    for combination in combinations:
        tagStr=""
        for tag in combination:
            tagStr = tagStr + ":" + tag
            pass
        tagMap[tagStr] = tagMap.get(tagStr,0) +1
        pass
    dd = OrderedDict(sorted(tagMap.items(), key=lambda x: x[1]))
    print dd

def tagSearch(searchTags):
    filteredProblems = [problemProperty for problemProperty in problemMap.values() if set(searchTags).issubset(problemProperty["tags"])]
    for problem in filteredProblems:
        line = "{} {} {} {}".format(problem["title"],problem["url"],problem["difficulty"],problem["tags"])
        print line

with open(sys.argv[1]) as fp:
    soup = BeautifulSoup(fp,"html5lib")
tables = soup.find_all("tbody", {"class": "reactable-data"})
# Every row(tr) is a Problem
rows = soup.find_all("tr")
# Process each row/Problem
for item in rows:
    data = item.find_all("td")
    if len(data) > 5:
        problemId = data[1].text
        title = data[2].text
        url = data[2].div.a["href"]
        tags = []
        for tag in data[3].find_all("a"):
             tags.append(tag.text)
        tags.sort()
        difficulty = data[5].text
        if data[6].get("value"):
            frequency = data[6]['value']
        else:
            frequency = 'N/A'

        problemProperty = {}
        problemProperty["title"] = title
        problemProperty["url"] = url
        problemProperty["tags"] = tags
        problemProperty["difficulty"] = difficulty
        problemProperty["frequency"] = frequency
        problemMap[problemId] = problemProperty
        line = "{} {} {} {} {}".format(problemId,title,difficulty,frequency,tags)
if len(sys.argv) == 2: 
   tagCount()
   tagCountNgram(2)
   tagCountNgram(3)
   pass
else:
   tagSearch([tag for tag in sys.argv[2:]])
