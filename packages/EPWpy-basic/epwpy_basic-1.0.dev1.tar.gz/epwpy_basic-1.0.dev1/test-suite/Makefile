test:
	pytest -q --disable-warnings ./tests_cluster/test_zg.py
	pytest -q --disable-warnings ./tests_cluster/test_scf.py
	pytest -q --disable-warnings ./tests_cluster/test_nscf.py
	pytest -q --disable-warnings ./tests_cluster/test_epw.py
	pytest -q --disable-warnings ./tests_cluster/test_ph.py
test_local:
	pytest -q --disable-warnings ./tests/test_zg.py
	pytest -q --disable-warnings ./tests/test_scf.py 
	pytest -q --disable-warnings ./tests/test_nscf.py
	pytest -q --disable-warnings ./tests/test_ph.py 
	pytest -q --disable-warnings ./tests/test_epw2.py
clean_local:
	rm -r scf nscf ph epw_indabs ZG_si 
	rm -r ./tests/__pycache__
clean_cluster:
	rm -r scf nscf ph epw_indabs ZG_si 
	rm -r ./tests_cluster/__pycache__		
