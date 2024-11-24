from _pytest.runner import runtestprotocol


def pytest_addoption(parser):
    parser.addini(
        name="maxretry",
        help="Number of times to retry a test class",
        type="string",
        default=None,
    )
    parser.addini(
        name="retry_on_exception",
        help="Exceptions to retry on",
        type="linelist",
        default=None,
    )
    parser.addoption("--maxretry", action="store", default=None)
    parser.addoption("--retry_on_exception", action="store", default=None)


def report_run(item):
    item.ihook.pytest_runtest_logstart(
        nodeid=item.nodeid, location=item.location
    )
    for report in item.reports:
        item.ihook.pytest_runtest_logreport(report=report)
    item.ihook.pytest_runtest_logfinish(
        nodeid=item.nodeid, location=item.location
    )


def pytest_runtest_protocol(item, nextitem):
    if item.cls is None:
        return False

    if getattr(item, "reports", None) is not None:
        report_run(item)
        return True

    siblings = [item]
    items = item.session.items
    index = items.index(item)
    for i in items[index + 1:]:
        if item.cls != i.cls:
            break
        siblings.append(i)
    if siblings[-1].cls == item.cls:
        siblings.append(None)

    run_count = 1
    all_passed = False
    config = item.session.config
    max_run_count = int(
        (config.getoption("maxretry") or config.getini("maxretry")) or 1
    )
    cmd_retry_arg = config.getoption("retry_on_exception") or None
    handle_exceptions = (
        cmd_retry_arg.strip("[]").split(", ")
        if cmd_retry_arg
        else [] or config.getini("retry_on_exception")
    )
    while not all_passed and run_count <= max_run_count:
        exceptions = []
        all_passed = True
        for i in range(len(siblings) - 1):
            siblings[i].reports = runtestprotocol(
                siblings[i], nextitem=siblings[i + 1], log=False
            )
            all_passed = all_passed and all(
                [rep.passed for rep in siblings[i].reports]
            )
            failed_steps = [rep for rep in siblings[i].reports if rep.failed]
            try:
                exceptions += [
                    step.longrepr.reprcrash.message.split(":")[0].split(".")[
                        -1
                    ]
                    for step in failed_steps
                ]
            except AttributeError:
                exceptions += [
                    step.longrepr.errorstring.split(":")[0].split(".")[-1]
                    for step in failed_steps
                ]
            if not all_passed:
                # Clean up setup state.
                item.session._setupstate.stack = {}
        if handle_exceptions and not any(
            [exc in handle_exceptions for exc in exceptions]
        ):
            break
        run_count += 1
    report_run(item)
    return True
