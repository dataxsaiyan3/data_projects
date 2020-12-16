# Basic commands to git and push 
git init
git add README.md
git add .
git commit -m "first commit"
git remote add origin https://github.com/userName/repoName.git
git push --force origin master


# Code command for github that solved please tell me who you are issue
1.git init
2.git config user.name "someone"
3.git config user.email "someone@someplace.com"
4.git add *
5.git commit -m "some init msg"

# This code will let git log display better when used
git log --topo-order --all --graph --date=local --pretty=format:'%C(green)%h%C(reset) %><(55,trunc)%s%C(red)%d%C(reset) %C(blue)[%an]%C(reset) %C(yellow)%ad%C(reset)%n'


# This code let you fix rejection issues
git fetch origin master:tmp
git rebase tmp
git push origin HEAD:master
git branch -D tmp

# This code let you pick GitHub branch name
$ git branch -m master


