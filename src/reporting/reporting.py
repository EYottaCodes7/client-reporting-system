from pathlib import Path

import pandas as pd


def create_summary_dataframe(kpis: dict) -> pd.DataFrame:
    """Convert KPI results into a report-friendly DataFrame."""

    return pd.DataFrame(
        {
            "metric": list(kpis.keys()),
            "value": list(kpis.values()),
        }
    )


def create_exception_dataframe(
    reconciled: pd.DataFrame,
) -> pd.DataFrame:
    """Return transactions that require attention."""

    return reconciled[
        reconciled["reconciliation_status"] != "MATCH"
    ].copy()


def generate_excel_report(
    kpis: dict,
    reconciled: pd.DataFrame,
    output_path: Path,
) -> None:
    """Generate the client-facing Excel report."""

    summary = create_summary_dataframe(kpis)

    exceptions = create_exception_dataframe(
        reconciled
    )

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl",
    ) as writer:

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False,
        )

        reconciled.to_excel(
            writer,
            sheet_name="Reconciliation",
            index=False,
        )

        exceptions.to_excel(
            writer,
            sheet_name="Exceptions",
            index=False,
        )