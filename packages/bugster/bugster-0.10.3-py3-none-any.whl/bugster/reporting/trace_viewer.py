from datetime import datetime, timezone


def start_trace(context):
    """
    Start recording a Playwright trace.
    Call this before test steps begin.
    """
    context.tracing.start(title="test_trace", snapshots=True, screenshots=True)


def stop_and_save_trace(context, output_dir="traces", test_name="test"):
    """
    Stop tracing and save the trace file.
    """
    import os

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S%f")
    filename = f"{test_name}_{timestamp}.zip"
    trace_path = os.path.join(output_dir, filename)
    context.tracing.stop(path=trace_path)
    return trace_path
