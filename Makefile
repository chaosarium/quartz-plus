.DEFAULT_GOAL := serve

build:
	hugo --cleanDestinationDir --enableGitInfo

serve: ## Serve Quartz locally
	hugo server --enableGitInfo

preprocess: ## prepare commands
	# clear content folder
	find "content" -type f -delete

	# copy published notes to quartz
	python preprocess.py --source_path "content-source/100 Vault" --target_path "content" --target_attachment_path "static/attachments"
	
	# build indices
	hugo-obsidian -input=content -output=assets/indices -index -root=. 


	# rm -r public
	# hugo-obsidian -input=content -output=assets/indices -index -root=. 
	# python utils/lower_case.py #change linkIndex to lowercase for proper linking

test: ## small scale content testing
	make regen
	open http://localhost:1313/something
	make serve

regen: ## re-preprocess when testing. Useful when hugo server already running
	# clear content folder
	find "content" -type f -delete
	find "static/attachments" -type f -delete

	#copy test vault to quartz
	python preprocess.py --source_path "content-source-test" --target_path "content" --target_attachment_path "static/attachments"

	# generate graph
	hugo-obsidian -input=content -output=assets/indices -index -root=. 

genproduction: ## re-preprocess when testing. Useful when hugo server already running
	# clear content folder
	find "content" -type f -delete
	find "static/attachments" -type f -delete

	#copy test vault to quartz
	python preprocess.py --source_path "/Users/chaosarium/Library/Mobile Documents/iCloud~md~obsidian/Documents/Zettelkasten" --target_path "content" --target_attachment_path "static/attachments"

	# generate graph
	hugo-obsidian -input=content -output=assets/indices -index -root=. 

watch: ## regenerates content folder every time file changes
	make regen
	fswatch -0 -v -o content-source-test | xargs -0 -n 1 -I {} make regen