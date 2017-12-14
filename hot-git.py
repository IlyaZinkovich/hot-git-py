import sys
import git as gitpy

repoPath = sys.argv[1]
git = gitpy.Git(repoPath)
repo = gitpy.Repo(repoPath)

files = git.ls_files().split('\n')

history = {}

def rawCommitToObject(commit):
    commitData = commit.split(',')
    return {'hash' : commitData[0], 'timestamp' : commitData[1]}

for file in files:
    rawCommits = git.log('--pretty=format:%H,%ad', '--date=short', '--follow', '--', file).split('\n')
    history[file] = list(map(rawCommitToObject, rawCommits))

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

commits = history['src/main/java/com/thomsonreuters/ask/model/Question.java']
commits.reverse()

dates = list(map(lambda commit: datetime.datetime.strptime(commit['timestamp'], "%Y-%m-%d"), commits))
values = [1]*len(commits)

plt.plot_date(x=dates, y=values)
plt.gcf().autofmt_xdate(rotation=25)
plt.show()
