from dataclasses import dataclass


@dataclass
class JobProgress:
    """Defines a common interface that should be returned when querying render_providers
    for the progress of a job
    'success' and 'failed' will always be false if the job has not ended.
    """

    ended: bool  # The job has ended, but could be successful or failed.
    failed: bool  # The job failed
    success: bool  # The job succeeded (no failures/issues deteced)
