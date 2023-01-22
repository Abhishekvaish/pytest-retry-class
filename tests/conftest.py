from _pytest.runner import runtestprotocol #as og_runtestprotocol

# def runtestprotocol(item , nextitem , log):
# 	if getattr(item , "reports" , None) is not None:
# 		return item.reports 
# 	return og_runtestprotocol(item= item , nextitem=nextitem , log= log)


def dummy_run(item) :
	item.ihook.pytest_runtest_logstart(nodeid=item.nodeid, location=item.location)
	for report in item.reports :
		item.ihook.pytest_runtest_logreport(report=report)
		# _remove_failed_setup_state_from_session(item)
		# _remove_cached_results_from_fixtures(item)
	item.ihook.pytest_runtest_logfinish(nodeid=item.nodeid, location=item.location)



def pytest_runtest_protocol(item, nextitem):
	# if item.cls is None :
	# 	return False
	
	if getattr(item , "reports" , None) is not None :
		# runtestprotocol(item= item , nextitem= nextitem , log=False)
		# dummy_run(item)
		return True
	
	siblings = [item]
	items = item.session.items
	index = items.index(item)
	for i in items[index+1:]:
		siblings.append(i)
		if item.cls  != i.cls :
			break
	if siblings[-1].cls == item.cls :
		siblings.append(None)

	for i in range(len(siblings)-1):
		siblings[i].reports = runtestprotocol(siblings[i] , nextitem=siblings[i+1] , log=False)
		dummy_run(siblings[i])
		# break
	
	# item.session._setupstate.teardown_exact(None)
	
	

	# item.reports = runtestprotocol(item, nextitem=nextitem , log=False)
	# dummy_run(item)

	# if nextitem is None:
	# 	print("="*37)
	# 	items = item.session.items
	# 	for i in range(len(items)-1):
	# 		items[i].reports = runtestprotocol(items[i], nextitem=items[i+1] , log=False)
	# 		dummy_run(items[i])
	# 	items[-1].reports = runtestprotocol(items[-1], nextitem=nextitem , log=False)
	# 	dummy_run(items[-1])
			
	return True

def pytest_runtest_teardown(item , nextitem ):
	a   = [ ]
	# if item.nodeid == 'test_one.py::TestOne::test_1c':
		# a = []

def _remove_failed_setup_state_from_session(item):
	"""
	Clean up setup state.
	Note: remove all failures from every node in _setupstate stack
		  and clean the stack itself
	"""
	
	PYTEST_GTE_63 = True
	setup_state = item.session._setupstate
	if PYTEST_GTE_63:
		setup_state.stack = {}
	else:
		for node in setup_state.stack:
			if hasattr(node, "_prepare_exc"):
				del node._prepare_exc
		setup_state.stack = []


def _remove_cached_results_from_fixtures(item):
	"""Note: remove all cached_result attribute from every fixture."""
	cached_result = "cached_result"
	fixture_info = getattr(item, "_fixtureinfo", None)
	for fixture_def_str in getattr(fixture_info, "name2fixturedefs", ()):
		fixture_defs = fixture_info.name2fixturedefs[fixture_def_str]
		for fixture_def in fixture_defs:
			if getattr(fixture_def, cached_result, None) is not None:
				delattr(fixture_def, cached_result)                        