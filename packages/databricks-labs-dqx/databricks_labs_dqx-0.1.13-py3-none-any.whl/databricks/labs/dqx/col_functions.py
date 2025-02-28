import datetime
import re

import pyspark.sql.functions as F
from pyspark.sql import Column


def make_condition(condition: Column, message: Column | str, alias: str) -> Column:
    """Helper function to create a condition column.

    :param condition: condition expression
    :param message: message to output - it could be either `Column` object, or string constant
    :param alias: name for the resulting column
    :return: an instance of `Column` type, that either returns string if condition is evaluated to `true`,
             or `null` if condition is evaluated to `false`
    """
    if isinstance(message, str):
        msg_col = F.lit(message)
    else:
        msg_col = message

    return (F.when(condition, msg_col).otherwise(F.lit(None).cast("string"))).alias(_cleanup_alias_name(alias))


def _cleanup_alias_name(col_name: str) -> str:
    # avoid issues with structs
    return col_name.replace(".", "_")


def is_not_null_and_not_empty(col_name: str, trim_strings: bool = False) -> Column:
    """Creates a condition column to check if value is null or empty.

    :param col_name: column name to check
    :param trim_strings: boolean flag to trim spaces from strings
    :return: Column object for condition
    """
    column = F.col(col_name)
    if trim_strings:
        column = F.trim(column).alias(col_name)
    condition = column.isNull() | (column.cast("string").isNull() | (column.cast("string") == F.lit("")))
    return make_condition(condition, f"Column {col_name} is null or empty", f"{col_name}_is_null_or_empty")


def is_not_empty(col_name: str) -> Column:
    """Creates a condition column to check if value is empty (but could be null).

    :param col_name: column name to check
    :return: Column object for condition
    """
    column = F.col(col_name)
    condition = column.cast("string") == F.lit("")
    return make_condition(condition, f"Column {col_name} is empty", f"{col_name}_is_empty")


def is_not_null(col_name: str) -> Column:
    """Creates a condition column to check if value is null.

    :param col_name: column name to check
    :return: Column object for condition
    """
    column = F.col(col_name)
    return make_condition(column.isNull(), f"Column {col_name} is null", f"{col_name}_is_null")


def value_is_not_null_and_is_in_list(col_name: str, allowed: list) -> Column:
    """Creates a condition column to check if value is null or not in the list of allowed values.

    :param col_name: column name to check
    :param allowed: list of allowed values (actual values or Column objects)
    :return: Column object for condition
    """
    allowed_cols = [item if isinstance(item, Column) else F.lit(item) for item in allowed]
    column = F.col(col_name)
    condition = column.isNull() | ~column.isin(*allowed_cols)
    return make_condition(
        condition,
        F.concat_ws(
            "",
            F.lit("Value "),
            F.when(column.isNull(), F.lit("null")).otherwise(column.cast("string")),
            F.lit(" is not in the allowed list: ["),
            F.concat_ws(", ", *allowed_cols),
            F.lit("]"),
        ),
        f"{col_name}_value_is_not_in_the_list",
    )


def value_is_in_list(col_name: str, allowed: list) -> Column:
    """Creates a condition column to check if value not in the list of allowed values (could be null).

    :param col_name: column name to check
    :param allowed: list of allowed values (actual values or Column objects)
    :return: Column object for condition
    """
    allowed_cols = [item if isinstance(item, Column) else F.lit(item) for item in allowed]
    column = F.col(col_name)
    condition = ~column.isin(*allowed_cols)
    return make_condition(
        condition,
        F.concat_ws(
            "",
            F.lit("Value "),
            F.when(column.isNull(), F.lit("null")).otherwise(column),
            F.lit(" is not in the allowed list: ["),
            F.concat_ws(", ", *allowed_cols),
            F.lit("]"),
        ),
        f"{col_name}_value_is_not_in_the_list",
    )


normalize_regex = re.compile("[^a-zA-Z-0-9]+")


def sql_expression(expression: str, msg: str | None = None, name: str | None = None, negate: bool = False) -> Column:
    """Creates a condition column from the SQL expression.

    :param expression: SQL expression
    :param msg: optional message of the `Column` type, automatically generated if None
    :param name: optional name of the resulting column, automatically generated if None
    :param negate: if the condition should be negated (true) or not. For example, "col is not null" will mark null
    values as "bad". Although sometimes it's easier to specify it other way around "col is null" + negate set to False
    :return: new Column
    """
    expr_col = F.expr(expression)
    expression_msg = expression

    if negate:
        expr_col = ~expr_col
        expression_msg = "~(" + expression + ")"

    name = name if name else re.sub(normalize_regex, "_", expression)

    if msg:
        return make_condition(expr_col, msg, name)
    return make_condition(expr_col, F.concat_ws("", F.lit(f"Value matches expression: {expression_msg}")), name)


def is_older_than_col2_for_n_days(col_name1: str, col_name2: str, days: int) -> Column:
    """Creates a condition column for case when one date or timestamp column is older than another column by N days.

    :param col_name1: first column
    :param col_name2: second column
    :param days: number of days
    :return: new Column
    """
    col1_date = F.to_date(F.col(col_name1))
    col2_date = F.to_date(F.col(col_name2))
    condition = col1_date < F.date_sub(col2_date, days)

    return make_condition(
        condition,
        F.concat_ws(
            "",
            F.lit(f"Value of {col_name1}: '"),
            col1_date,
            F.lit(f"' less than value of {col_name2}: '"),
            col2_date,
            F.lit(f"' for more than {days} days"),
        ),
        f"is_col_{col_name1}_older_than_{col_name2}_for_N_days",
    )


def is_older_than_n_days(col_name: str, days: int, curr_date: Column | None = None) -> Column:
    """Creates a condition column for case when specified date or timestamp column is older (compared to current date)
    than N days.

    :param col_name: name of the column to check
    :param days: number of days
    :param curr_date: (optional) set current date
    :return: new Column
    """
    if curr_date is None:
        curr_date = F.current_date()

    col_date = F.to_date(F.col(col_name))
    condition = col_date < F.date_sub(curr_date, days)

    return make_condition(
        condition,
        F.concat_ws(
            "",
            F.lit(f"Value of {col_name}: '"),
            col_date,
            F.lit("' less than current date: '"),
            curr_date,
            F.lit(f"' for more than {days} days"),
        ),
        f"is_col_{col_name}_older_than_N_days",
    )


def not_in_future(col_name: str, offset: int = 0, curr_timestamp: Column | None = None) -> Column:
    """Creates a condition column that checks if specified date or timestamp column is in the future.
    Future is considered as grater than current timestamp plus `offset` seconds.

    :param col_name: column name
    :param offset: offset (in seconds) to add to the current timestamp at time of execution
    :param curr_timestamp: (optional) set current timestamp
    :return: new Column
    """
    if curr_timestamp is None:
        curr_timestamp = F.current_timestamp()

    timestamp_offset = F.from_unixtime(F.unix_timestamp(curr_timestamp) + offset)
    condition = F.col(col_name) > timestamp_offset

    return make_condition(
        condition,
        F.concat_ws(
            "", F.lit("Value '"), F.col(col_name), F.lit("' is greater than time '"), timestamp_offset, F.lit("'")
        ),
        f"{col_name}_in_future",
    )


def not_in_near_future(col_name: str, offset: int = 0, curr_timestamp: Column | None = None) -> Column:
    """Creates a condition column that checks if specified date or timestamp column is in the near future.
    Near future is considered as grater than current timestamp but less than current timestamp plus `offset` seconds.

    :param col_name: column name
    :param offset: offset (in seconds) to add to the current timestamp at time of execution
    :param curr_timestamp: (optional) set current timestamp
    :return: new Column
    """
    if curr_timestamp is None:
        curr_timestamp = F.current_timestamp()

    near_future = F.from_unixtime(F.unix_timestamp(curr_timestamp) + offset)
    condition = (F.col(col_name) > curr_timestamp) & (F.col(col_name) < near_future)

    return make_condition(
        condition,
        F.concat_ws(
            "",
            F.lit("Value '"),
            F.col(col_name),
            F.lit("' is greater than '"),
            curr_timestamp,
            F.lit(" and smaller than '"),
            near_future,
            F.lit("'"),
        ),
        f"{col_name}_in_near_future",
    )


def not_less_than(col_name: str, limit: int | datetime.date | datetime.datetime) -> Column:
    """Creates a condition column that checks if a value is less than specified limit.

    :param col_name: column name
    :param limit: limit to use in the condition
    :return: new Column
    """
    limit_expr = F.lit(limit)
    condition = F.col(col_name) < limit_expr

    return make_condition(
        condition,
        F.concat_ws(" ", F.lit("Value"), F.col(col_name), F.lit("is less than limit:"), F.lit(limit).cast("string")),
        f"{col_name}_less_than_limit",
    )


def not_greater_than(col_name: str, limit: int | datetime.date | datetime.datetime) -> Column:
    """Creates a condition column that checks if a value is greater than specified limit.

    :param col_name: column name
    :param limit: limit to use in the condition
    :return: new Column
    """
    limit_expr = F.lit(limit)
    condition = F.col(col_name) > limit_expr

    return make_condition(
        condition,
        F.concat_ws(" ", F.lit("Value"), F.col(col_name), F.lit("is greater than limit:"), F.lit(limit).cast("string")),
        f"{col_name}_greater_than_limit",
    )


def _get_min_max_column_expr(
    min_limit: int | datetime.date | datetime.datetime | str | None = None,
    max_limit: int | datetime.date | datetime.datetime | str | None = None,
    min_limit_col_expr: str | Column | None = None,
    max_limit_col_expr: str | Column | None = None,
) -> tuple[Column, Column]:
    """Helper function to create a condition for the is_(not)_in_range functions.

    :param min_limit: min limit value
    :param max_limit: max limit value
    :param min_limit_col_expr: min limit column name or expr
    :param max_limit_col_expr: max limit column name or expr
    :return: tuple containing min_limit_expr and max_limit_expr
    :raises: ValueError when both min_limit/min_limit_col_expr or max_limit/max_limit_col_expr are null
    """
    if (min_limit is None and min_limit_col_expr is None) or (max_limit is None and max_limit_col_expr is None):
        raise ValueError('Either min_limit / min_limit_col_expr or max_limit / max_limit_col_expr is empty')
    if min_limit_col_expr is None:
        min_limit_expr = F.lit(min_limit)
    else:
        min_limit_expr = F.col(min_limit_col_expr) if isinstance(min_limit_col_expr, str) else min_limit_col_expr
    if max_limit_col_expr is None:
        max_limit_expr = F.lit(max_limit)
    else:
        max_limit_expr = F.col(max_limit_col_expr) if isinstance(max_limit_col_expr, str) else max_limit_col_expr
    return (min_limit_expr, max_limit_expr)


def is_in_range(
    col_name: str,
    min_limit: int | datetime.date | datetime.datetime | str | None = None,
    max_limit: int | datetime.date | datetime.datetime | str | None = None,
    min_limit_col_expr: str | Column | None = None,
    max_limit_col_expr: str | Column | None = None,
) -> Column:
    """Creates a condition column that checks if a value is smaller than min limit or greater than max limit.

    :param col_name: column name
    :param min_limit: min limit value
    :param max_limit: max limit value
    :param min_limit_col_expr: min limit column name or expr
    :param max_limit_col_expr: max limit column name or expr
    :return: new Column
    """
    min_limit_expr, max_limit_expr = _get_min_max_column_expr(
        min_limit, max_limit, min_limit_col_expr, max_limit_col_expr
    )
    condition = (F.col(col_name) < min_limit_expr) | (F.col(col_name) > max_limit_expr)

    return make_condition(
        condition,
        F.concat_ws(
            " ",
            F.lit("Value"),
            F.col(col_name),
            F.lit("not in range: ["),
            min_limit_expr.cast("string"),
            F.lit(","),
            max_limit_expr.cast("string"),
            F.lit("]"),
        ),
        f"{col_name}_not_in_range",
    )


def is_not_in_range(
    col_name: str,
    min_limit: int | datetime.date | datetime.datetime | str | None = None,
    max_limit: int | datetime.date | datetime.datetime | str | None = None,
    min_limit_col_expr: str | Column | None = None,
    max_limit_col_expr: str | Column | None = None,
) -> Column:
    """Creates a condition column that checks if a value is within min and max limits.

    :param col_name: column name
    :param min_limit: min limit value
    :param max_limit: max limit value
    :param min_limit_col_expr: min limit column name or expr
    :param max_limit_col_expr: max limit column name or expr
    :return: new Column
    """
    min_limit_expr, max_limit_expr = _get_min_max_column_expr(
        min_limit, max_limit, min_limit_col_expr, max_limit_col_expr
    )
    condition = (F.col(col_name) > min_limit_expr) & (F.col(col_name) < max_limit_expr)

    return make_condition(
        condition,
        F.concat_ws(
            " ",
            F.lit("Value"),
            F.col(col_name),
            F.lit("in range: ["),
            min_limit_expr.cast("string"),
            F.lit(","),
            max_limit_expr.cast("string"),
            F.lit("]"),
        ),
        f"{col_name}_in_range",
    )


def regex_match(col_name: str, regex: str, negate: bool = False) -> Column:
    """Creates a condition column to check if value not matches given regex.

    :param col_name: column name to check
    :param regex: regex to check
    :param negate: if the condition should be negated (true) or not
    :return: Column object for condition
    """
    if negate:
        condition = F.col(col_name).rlike(regex)

        return make_condition(condition, f"Column {col_name} is matching regex", f"{col_name}_matching_regex")

    condition = ~F.col(col_name).rlike(regex)

    return make_condition(condition, f"Column {col_name} is not matching regex", f"{col_name}_not_matching_regex")


def is_not_null_and_not_empty_array(col_name: str) -> Column:
    """
    Creates a condition column to check if an array is null and or empty.
    :param col_name: column name to check
    :return: Column object for condition
    """
    column = F.col(col_name)
    condition = column.isNull() | (F.size(column) == 0)
    return make_condition(condition, f"Column {col_name} is null or empty array", f"{col_name}_is_null_or_empty_array")


def is_valid_date(col_name: str, date_format: str | None = None) -> Column:
    """
    Creates a condition column to check if a string is a valid date.
    :param col_name: column name to check
    :param date_format: date format (e.g. 'yyyy-mm-dd')
    :return: Column object for condition
    """
    column = F.col(col_name)
    date_col = F.try_to_timestamp(column) if date_format is None else F.try_to_timestamp(column, F.lit(date_format))
    condition = F.when(column.isNull(), F.lit(None)).otherwise(date_col.isNull())
    condition_str = "' is not a valid date"
    if date_format is not None:
        condition_str += f" with format '{date_format}'"
    return make_condition(
        condition,
        F.concat_ws("", F.lit("Value '"), column, F.lit(condition_str)),
        f"{col_name}_is_not_valid_date",
    )


def is_valid_timestamp(col_name: str, timestamp_format: str | None = None) -> Column:
    """
    Creates a condition column to check if a string is a valid timestamp.
    :param col_name: column name to check
    :param timestamp_format: timestamp format (e.g. 'yyyy-mm-dd HH:mm:ss')
    :return: Column object for condition
    """
    column = F.col(col_name)
    ts_col = (
        F.try_to_timestamp(column) if timestamp_format is None else F.try_to_timestamp(column, F.lit(timestamp_format))
    )
    condition = F.when(column.isNull(), F.lit(None)).otherwise(ts_col.isNull())
    condition_str = "' is not a valid timestamp"
    if timestamp_format is not None:
        condition_str += f" with format '{timestamp_format}'"
    return make_condition(
        condition,
        F.concat_ws("", F.lit("Value '"), column, F.lit(condition_str)),
        f"{col_name}_is_not_valid_timestamp",
    )
