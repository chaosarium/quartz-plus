.DEFAULT_GOAL := serve
TEST_CONTENT_PATH := "content-source-test"
PROD_CONTENT_PATH := "/Users/chaosarium/Library/Mobile Documents/iCloud~md~obsidian/Documents/Zettelkasten"

build: cleanhugo genprod
	hugo --cleanDestinationDir --enableGitInfo

serve: ## Serve Quartz locally
	hugo server --enableGitInfo

cleanhugo: ## delete output
	find "content" -type f -delete
	find "public" -type f -delete
	find "resources" -type f -delete
	find "static/attachments" -type f \( -iname "*" ! -iname ".gitkeep" \) -delete

cleancontent: 
	find "content" -type f -delete
	find "static/attachments" -type f \( -iname "*" ! -iname ".gitkeep" \) -delete

buildindices: 
	hugo-obsidian -input=content -output=assets/indices -index -root=. 

proctest: cleancontent
	python preprocess.py --source_path $(TEST_CONTENT_PATH) --target_path "content" --target_attachment_path "static/attachments" >/dev/null
procprod: cleancontent
	python preprocess.py --source_path $(PROD_CONTENT_PATH) --target_path "content" --target_attachment_path "static/attachments" >/dev/null

proctestverbose: cleancontent
	python preprocess.py --source_path $(TEST_CONTENT_PATH) --target_path "content" --target_attachment_path "static/attachments"
procprodverbose: cleancontent
	python preprocess.py --source_path $(PROD_CONTENT_PATH) --target_path "content" --target_attachment_path "static/attachments"

gentest: cleancontent proctest buildindices
genprod: cleancontent procprod buildindices

watchtest: gentest ## regenerates content folder every time file changes
	fswatch -0 -v -o $(TEST_CONTENT_PATH) | xargs -0 -n 1 -I {} make gentest