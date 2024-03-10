project_name := "moadaly"

alias t := test
alias r := run

_default:
	@just --list

run:
	python -m {{ project_name }}

test:
	pytest tests/

lint_all:
	pre-commit run --all-files

compile_dep:
	pre-commit run pip-compile --all-files

sync_dep:
	pip-sync requirements/{requirements,requirements-dev}.txt

todo:
	rg ".(FIX|TODO|HACK|WARN|PREF|NOTE): " --glob !{{ file_name(justfile()) }}

# vim: set ft=make :
