.DEFAULT_GOAL := serve

update: ## Update Quartz to the latest version on Github
	go install github.com/jackyzha0/hugo-obsidian@latest
	@git remote show upstream || (echo "remote 'upstream' not present, setting 'upstream'" && git remote add upstream https://github.com/jackyzha0/quartz.git)
	git fetch upstream
	git log --oneline --decorate --graph ..upstream/hugo
	git checkout -p upstream/hugo -- layouts .github Makefile assets/js assets/styles/base.scss assets/styles/darkmode.scss config.toml data

update-force: ## Forcefully pull all changes and don't ask to patch
	go install github.com/jackyzha0/hugo-obsidian@latest
	@git remote show upstream || (echo "remote 'upstream' not present, setting 'upstream'" && git remote add upstream https://github.com/jackyzha0/quartz.git)
	git fetch upstream
	git checkout upstream/hugo -- layouts .github Makefile assets/js assets/styles/base.scss assets/styles/darkmode.scss config.toml data

build:
	hugo --cleanDestinationDir --enableGitInfo

serve: ## Serve Quartz locally
	hugo server --enableGitInfo

preprocess: ## prepare commands
	# clear content folder
	find "content" -type f -delete
	#copy published notes to quartz
	python preprocess.py --source_path "content-source/100 Vault" --target_path "content" --target_attachment_path "content/images"
	hugo-obsidian -input=content -output=assets/indices -index -root=. 

	# rm -r public
	# hugo-obsidian -input=content -output=assets/indices -index -root=. 
	# python utils/lower_case.py #change linkIndex to lowercase for proper linking

test: ## small scale content testing
	# clear content folder
	find "content" -type f -delete

	#copy test vault to quartz
	python preprocess.py --source_path "content-source-test" --target_path "content" --target_attachment_path "content/images"

	# generate graph
	hugo-obsidian -input=content -output=assets/indices -index -root=. 

	open http://localhost:1313/
	make serve