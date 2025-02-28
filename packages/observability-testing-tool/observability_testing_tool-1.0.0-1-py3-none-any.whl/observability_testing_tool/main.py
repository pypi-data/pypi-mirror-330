from observability_testing_tool.config.common import info_log

from observability_testing_tool.config.executor import prepare, run_logging_jobs, create_metrics_descriptors, run_monitoring_jobs


def main():
    info_log(">>> Obs Test Tool - Getting things going...")
    prepare()
    info_log(">>> Obs Test Tool - Done with preparation. Now proceeding with logging tasks...")
    p1 = run_logging_jobs()
    info_log(">>> Obs Test Tool - Done with logging tasks. Now proceeding with monitoring tasks...")
    create_metrics_descriptors()
    p2 = run_monitoring_jobs()
    info_log(">>> Obs Test Tool - Done with monitoring tasks. Now waiting for live jobs to terminate...")
    if p1 is not None: p1.join()
    if p2 is not None: p2.join()


if __name__ == '__main__':
    main()
