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
    break

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

commits = history['.gitignore']
##commits = history['src/main/java/com/thomsonreuters/ask/model/Question.java']
commits.reverse()

import pandas as pd
dataframe = pd.DataFrame(commits)
dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])
dataframe['today'] = pd.Series([pd.to_datetime('today')]*len(commits))
dataframe['days'] = 1 - (dataframe['today'] - dataframe['timestamp']).dt.days
print(dataframe)

dates = dataframe['days']
values = [1]*len(commits)

plt.plot(dates, values, 'ro')
plt.gcf().autofmt_xdate(rotation=25)
plt.show()
