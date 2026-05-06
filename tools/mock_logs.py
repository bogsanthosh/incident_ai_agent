def get_mock_logs(service_name: str):
    scenarios = {
        "payment-api": [
            "2026-05-05 02:01:12 ERROR payment-api returned HTTP 503 from auth-service",
            "2026-05-05 02:01:14 WARN retry attempt 1 failed for auth-service",
            "2026-05-05 02:01:17 ERROR connection timeout to auth-service",
            "2026-05-05 02:01:20 INFO circuit breaker opened for auth-service",
        ],
        "order-api": [
            "2026-05-05 03:11:02 ERROR order-api database connection timeout",
            "2026-05-05 03:11:06 WARN connection pool exhausted",
            "2026-05-05 03:11:10 ERROR query execution exceeded 30 seconds",
        ],
        "auth-service": [
            "2026-05-05 04:21:33 ERROR auth-service token validation failed",
            "2026-05-05 04:21:35 WARN invalid JWT signature detected",
            "2026-05-05 04:21:40 ERROR multiple authentication failures",
        ],
        "inventory-service": [
            "2026-05-05 05:31:44 ERROR inventory-service memory usage exceeded 92%",
            "2026-05-05 05:31:50 WARN garbage collection pause detected",
            "2026-05-05 05:32:02 ERROR pod restarted due to OOMKilled",
        ],
        "deployment-service": [
            "2026-05-05 06:41:11 ERROR deployment failed during rollout",
            "2026-05-05 06:41:18 WARN health check failed for new version",
            "2026-05-05 06:41:25 ERROR rollback triggered automatically",
        ],
    }

    return scenarios.get(service_name, scenarios["payment-api"])