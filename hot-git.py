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

#commits = history['.gitignore']
commits = history['src/main/java/com/thomsonreuters/ask/model/Question.java']
commits.reverse()

import pandas as pd
dataframe = pd.DataFrame(commits)
dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

dataframe.set_index(['timestamp'])
aggregate = dataframe.groupby([pd.Grouper(key='timestamp', freq='W')], as_index=False).size().to_frame('count').reset_index()
print(aggregate)

dates = aggregate['timestamp']
values = aggregate['count']
plt.plot_date(dates, values, linestyle='solid', marker='None')
plt.gcf().autofmt_xdate(rotation=25)
plt.show()
