main_branch="master"
working_branch="working"

git checkout "$main_branch"
git merge "$working_branch" --no-ff
git push origin "$main_branch"

echo "Main branch updated"

git checkout "$working_branch"
