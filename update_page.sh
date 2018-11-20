python3 gen_hub.py
git add lecture_list
git add index.html
git commit -m $0
git push
cat remote_update.sh | ssh archimedes.cs.virginia.edu
exit
