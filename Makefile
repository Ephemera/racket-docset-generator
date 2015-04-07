all: copy generate

.PHONY: all 

copy:
	racket -e ' \
		(require setup/dirs) \
		(delete-directory/files "racket.docset/Contents/Resources/Documents") \
		(copy-directory/files (~a (find-doc-dir)) "racket.docset/Contents/Resources/Documents")'

generate:
	python generator.py

compress:
	tar --exclude='.DS_Store' -cvzf Racket.tgz Racket.docset

