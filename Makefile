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

serve: ## Serve Quartz locally
	hugo-obsidian -input=content -output=assets/indices -index -root=. && hugo server --enableGitInfo --minify

prepare: ## prepare commands
	# clear content folder
	find "content" -type f -delete
	#copy published notes to quartz
	python content-preprocess.py
	
	# rm -r public
	# hugo-obsidian -input=content -output=assets/indices -index -root=. 
	# python utils/lower_case.py #change linkIndex to lowercase for proper linking