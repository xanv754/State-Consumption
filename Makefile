DATE=$(shell date +%Y-%m-%d)

setup:
	if [ ! -d ".venv" ]; then \
		python3.13 -m venv .venv; \
		. .venv/bin/activate; \
		pip install -r requirements.txt; \
	fi

setup-virtualvenv:
	if [ ! -d ".venv" ]; then \
		virtualvenv .venv; \
		. .venv/bin/activate; \
		pip install -r requirements.txt; \
	fi

clean:
	rm -rf __pycache__
	rm -rf .venv

importdb:
	if mongoimport --version > /dev/null; then \
		if [ -n "$(FILE)" ]; then \
			if [ -z "$(URI)" ]; then \
				mongoimport -c nodes mongodb://localhost:27017/state_consumption $(FILE); \
			else \
				mongoimport -c nodes $(URI) $(FILE); \
			fi \
		else \
			echo "File to import not specified"; \
		fi \
	else \
		echo "mongoimport command not found"; \
	fi

exportdb:
	if mongoexport --version > /dev/null; then \
		if [ -n "$(FILE)" ]; then \
			if [ -z "$(URI)" ]; then \
				mongoexport --collection=nodes --out=$(FILE) mongodb://localhost:27017/state_consumption; \
			else \
				mongoexport --collection=nodes --out=$(FILE) $(URI); \
			fi \
		else \
			if [ -z "$(URI)" ]; then \
				mongoexport --collection=nodes --out="/tmp/nodes_$(DATE).json" mongodb://localhost:27017/state_consumption; \
			else \
				mongoexport --collection=nodes --out="/tmp/nodes_$(DATE).json" $(URI); \
			fi \
		fi \
	else \
		echo "mongoexport command not found"; \
	fi