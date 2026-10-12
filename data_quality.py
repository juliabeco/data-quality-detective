
import pandas as pd


def profile_data(df):
    """Return data types, missing values and unique counts by column."""
    profile = pd.DataFrame({
        "data_type": df.dtypes.astype(str),
        "missing_count": df.isna().sum(),
        "missing_pct": (df.isna().mean() * 100).round(2),
        "unique_values": df.nunique(),
    })

    profile.index.name = "column"
    return profile.reset_index()


def summarize_data(df):
    """Return general dataset quality metrics."""
    return pd.Series({
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "total_missing_cells": int(df.isna().sum().sum()),
    }, name="value")


def validate_data(df):
    """Detect issues using rules for the example customer dataset."""

    required = {"customer_id", "age", "monthly_spend"}
    missing_columns = required - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    issues = []

    age = pd.to_numeric(df["age"], errors="coerce")
    spend = pd.to_numeric(df["monthly_spend"], errors="coerce")

    def add_issue(mask, column, rule, severity, message):
        for idx in df.index[mask]:
            issues.append({
                "row_index": idx,
                "customer_id": df.loc[idx, "customer_id"],
                "column": column,
                "rule": rule,
                "severity": severity,
                "value": df.loc[idx, column],
                "message": message,
            })

    add_issue(
        df["age"].notna() & age.isna(),
        "age", "AGE_NOT_NUMERIC", "high",
        "Age must be a numeric value."
    )

    add_issue(
        age.notna() & ~age.between(0, 100),
        "age", "AGE_OUT_OF_RANGE", "high",
        "Age must be between 0 and 100."
    )

    add_issue(
        spend.notna() & (spend < 0),
        "monthly_spend", "NEGATIVE_SPENDING", "medium",
        "Monthly spending cannot be negative."
    )

    columns = [
        "row_index", "customer_id", "column",
        "rule", "severity", "value", "message"
    ]

    return pd.DataFrame(issues, columns=columns)


def build_quality_report(df, issues_df):
    """Build an executive summary of quality metrics."""

    total_rows = len(df)
    total_cells = df.shape[0] * df.shape[1]

    affected_rows = (
        int(issues_df["row_index"].nunique())
        if not issues_df.empty else 0
    )

    return {
        "total_rows": total_rows,
        "total_columns": len(df.columns),
        "total_cells": total_cells,
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "validation_issues": len(issues_df),
        "rows_with_validation_issues": affected_rows,
        "rows_with_issues_pct": round(
            affected_rows / total_rows * 100, 2
        ) if total_rows else 0,
    }


def summarize_issues(issues_df):
    """Count issues by validation rule and severity."""

    if issues_df.empty:
        return pd.DataFrame(
            columns=["rule", "severity", "issue_count"]
        )

    return (
        issues_df.groupby(["rule", "severity"])
        .size()
        .reset_index(name="issue_count")
        .sort_values("issue_count", ascending=False)
        .reset_index(drop=True)
    )


def generate_reports(df, output_dir="reports"):
    """Run the analysis and export all report files."""
    from pathlib import Path

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    profile = profile_data(df)
    issues = validate_data(df)
    summary = build_quality_report(df, issues)
    issue_summary = summarize_issues(issues)

    pd.DataFrame(
        list(summary.items()), columns=["metric", "value"]
    ).to_csv(output_path / "quality_summary.csv", index=False)

    profile.to_csv(output_path / "quality_profile.csv", index=False)
    issues.to_csv(output_path / "quality_issues.csv", index=False)
    issue_summary.to_csv(
        output_path / "quality_issue_summary.csv", index=False
    )

    return {
        "summary": summary,
        "profile": profile,
        "issues": issues,
        "issue_summary": issue_summary,
    }
