from _pytest.runner import runtestprotocol


def pytest_addoption(parser):
    parser.addoption("--maxretry", action="store", default="1")


def report_run(item):
    item.ihook.pytest_runtest_logstart(
        nodeid=item.nodeid, location=item.location)
    for report in item.reports:
        item.ihook.pytest_runtest_logreport(report=report)
    item.ihook.pytest_runtest_logfinish(
        nodeid=item.nodeid, location=item.location)


def pytest_runtest_protocol(item, nextitem):
    if item.cls is None:
        return False

    if getattr(item, "reports", None) is not None:
        report_run(item)
        return True

    siblings = [item]
    items = item.session.items
    index = items.index(item)
    for i in items[index+1:]:
        siblings.append(i)
        if item.cls != i.cls:
            siblings.append(i)
            break
    if siblings[-1].cls == item.cls:
        siblings.append(None)

    run_count = 1
    all_passed = False
    max_run_count = int(item.session.config.option.maxretry)
    while not all_passed and run_count <= max_run_count:
        all_passed = True
        for i in range(len(siblings)-1):
            siblings[i].reports = runtestprotocol(
                siblings[i], nextitem=siblings[i+1], log=False)
            all_passed = all_passed and all(
                [rep.passed for rep in siblings[i].reports])
            if not all_passed:
                # Clean up setup state.
                item.session._setupstate.stack = {}
        run_count += 1

    report_run(item)
    return True
