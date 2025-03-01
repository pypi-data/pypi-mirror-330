import os
from datetime import datetime, timezone


def capture_screenshot(
    page, locator=None, step_name="step", output_dir="screenshots", index=0
):
    """
    Captures a screenshot of the current page state.
    step_name: A descriptive name of the step being captured.
    output_dir: Directory where screenshots are saved.
    index: An index to prepend to the filename for ordering.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S%f")
    filename = f"{index}_{step_name}_{timestamp}.png"
    path = os.path.join(output_dir, filename)
    mask = [locator] if locator else None
    mask_color = "hsla(259, 100%, 62%, 0.47)" if locator else None

    page.screenshot(path=path, mask=mask, mask_color=mask_color)
    return path
