# Mart Model: calendar

## Overview
The `calendar` model constructs a comprehensive date dimension that spans six years from January 1, 2020. It generates a continuous date spine and enriches it with essential date attributes, including year, month, day, weekday, quarter, weekend flag, and formatted representations of month and year. Additionally, the model calculates week boundaries based on a business logic that identifies the Thursday of the current week as the week start and computes the week end date accordingly. Finally, it integrates business-specific week information by joining with a raw week number table.

## Source Data
- **Generated Date Spine:**
  - A continuous series of dates is created by adding an integer number of days (from 0 to 365×6) to the base date `2020-01-01`.

- **Raw Week Number Data:**
  - The raw table `soft-drink-grocery.raw.raw_wno` is used to append week-related attributes. Specifically, the model joins on the week end date to bring in the business-specific week number (`Week` as `w_no`) and week index (`Week_Index` as `week_index`).

## Transformations Applied
### Date Spine and Attribute Extraction
- **Date Spine Generation:**
  The `date_spine` CTE generates a continuous series of dates over a six-year period.

- **Attribute Extraction:**
  In the `calendar` CTE, the model extracts:
  - **Year, Month, and Day:**
    Using the `extract()` function on the generated date.
  - **Weekday:**
    The day of the week is extracted (where the numeric value corresponds to the day, e.g., 1 for Sunday, 7 for Saturday).
  - **Quarter:**
    The quarter of the year is determined.
  - **Weekend Flag:**
    A boolean field (`is_weekend`) is set to `true` if the day is a weekend (when `extract(dayofweek)` returns 1 or 7).

### Date Formatting and Week Boundaries
- **Formatted Date Values:**
  - **Month Name:**
    The abbreviated month name (e.g., Jan, Feb) is derived using `format_date('%b', date)`.
  - **Month/Year Combination:**
    A formatted string combining month and year (e.g., Jan/22) is generated.

- **Week Boundary Calculation:**
  - **Week Start:**
    The model calculates the start of the week by finding the Thursday of the current week. This is done using a modulus operation on the weekday value.
  - **Week End Date:**
    By adding 6 days to the calculated week start, the model determines the week end date.

### Integration of Business Week Data
- **Joining with Raw Week Data:**
  The final output is produced by joining the enriched calendar data with the `raw_wno` table. This join is performed on the condition that the calculated `week_end_date` matches the date of the `End Week` from the raw data. The join brings in:
  - **Week Number (`w_no`):**
    Derived from the `Week` column in the raw table.
  - **Week Index (`week_index`):**
    Derived from the `Week_Index` column in the raw table.

## Business Logic & Rationale
- **Time-Series Analysis Foundation:**
  A robust and detailed calendar dimension is crucial for any time-series analysis, as it allows for flexible and accurate aggregation of data over time.

- **Standardized Date Attributes:**
  The extraction and formatting of various date parts enable consistent slicing and dicing of data in downstream reporting.

- **Custom Week Definitions:**
  The calculation of week boundaries based on a business-specific definition (with Thursday as the reference) ensures that the calendar aligns with the organization’s reporting standards.

- **Integration with Business Week Data:**
  By joining with the raw week number table, the model incorporates business-specific week identifiers, providing further context for time-based analyses.

## Dependencies & Testing Considerations
- **Source Dependencies:**
  - The model depends on the generated date spine and the raw week number data from `soft-drink-grocery.raw.raw_wno`.

- **Testing Recommendations:**
  - **Date Range Verification:**
    Ensure the date spine covers the entire six-year period starting from January 1, 2020.
  - **Attribute Accuracy:**
    Verify that the extracted date components (year, month, day, weekday, quarter) match expected values.
  - **Week Boundary Calculations:**
    Validate that the `week_start` and `week_end_date` are correctly computed according to business logic.
  - **Join Integrity:**
    Confirm that the left join with `raw_wno` accurately appends the `w_no` and `week_index` based on matching week end dates.

## Conclusion
The `calendar` mart model provides a comprehensive and enriched date dimension that is fundamental for time-series reporting and analysis. By integrating detailed date attributes, custom week boundaries, and business-specific week data, this model ensures that downstream consumers have access to a robust temporal framework for their analytics.
