"""
📌 lib.py: Shared utilities and common definitions for REDCap-EDA analysis.

🔹 **Purpose**:
    - Provides reusable components across analysis modules.
    - Defines shared data structures, such as `AnalysisResult`, to ensure consistency.

🔹 **Why Use This?**
    - Avoids redundant definitions in multiple mixins.
    - Ensures consistency across numerical, categorical, and text analysis modules.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.lib import AnalysisResult
    ```

"""

from collections import namedtuple

"""
📌 AnalysisResult: Stores the results of an analysis.

🔹 **Fields**:
    - `summary` (dict): Contains computed statistical metrics.
    - `plots` (list[tuple[plt.Figure, str]]): Stores visualization figures and filenames.

🔹 **Why Use This?**
    - Standardized format ensures consistent handling of results across all mixins.
    - Enables easy extension without breaking analysis functions.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.lib import AnalysisResult
    result = AnalysisResult(summary={"mean": 42}, plots=[("plot.png")])
    ```
"""

AnalysisResult = namedtuple("AnalysisResult", ["summary", "plot_paths"])
