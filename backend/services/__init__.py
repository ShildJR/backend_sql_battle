import sqlite3
import tempfile
import os
import time
import json
from typing import List, Dict, Any, Tuple


FORBIDDEN_KEYWORDS = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'TRUNCATE', 'CREATE', 'GRANT', 'REVOKE']


def validate_query(query: str) -> Tuple[bool, str]:
    """Validate that the query is safe to execute (SELECT only)."""
    query_upper = query.upper().strip()
    
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in query_upper:
            return False, f"Forbidden keyword: {keyword}. Only SELECT queries are allowed."
    
    if not query_upper.startswith("SELECT") and not query_upper.startswith("WITH"):
        return False, "Only SELECT queries are allowed."
    
    return True, ""


def execute_sql_in_sandbox(
    query: str, 
    schema: str, 
    tables_data: List[Dict[str, Any]],
    timeout: int = 3
) -> Dict[str, Any]:
    """
    Execute SQL query in an isolated sandbox environment.
    Creates a temporary SQLite database with the given schema and data.
    """
    # Validate query first
    is_valid, error_msg = validate_query(query)
    if not is_valid:
        return {
            "status": "error",
            "message": error_msg
        }
    
    # Create temporary database
    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.db')
    os.close(tmp_fd)
    
    try:
        conn = sqlite3.connect(tmp_path, timeout=timeout)
        conn.row_factory = sqlite3.Row
        
        # Create schema
        conn.executescript(schema)
        
        # Insert sample data from tables
        for table in tables_data:
            table_name = table.get("name", "")
            sample_data = table.get("sampleData", [])
            columns = table.get("columns", [])
            
            if not sample_data or not columns:
                continue
            
            col_names = [col["name"] for col in columns]
            placeholders = ", ".join(["?"] * len(col_names))
            col_str = ", ".join(col_names)
            
            for row in sample_data:
                values = [row.get(col) for col in col_names]
                insert_sql = f"INSERT INTO {table_name} ({col_str}) VALUES ({placeholders})"
                conn.execute(insert_sql, values)
        
        conn.commit()
        
        # Execute the user's query with timing
        start_time = time.time()
        cursor = conn.execute(query)
        result_rows = cursor.fetchall()
        execution_time = time.time() - start_time
        
        # Get column names
        column_names = [description[0] for description in cursor.description] if cursor.description else []
        
        # Convert to list of dicts
        data = []
        for row in result_rows:
            row_dict = {}
            for i, col_name in enumerate(column_names):
                row_dict[col_name] = row[i]
            data.append(row_dict)
        
        conn.close()
        
        return {
            "status": "success",
            "data": data,
            "execution_time": round(execution_time, 3)
        }
        
    except sqlite3.OperationalError as e:
        return {
            "status": "error",
            "message": f"SQL Error: {str(e)}"
        }
    except sqlite3.DatabaseError as e:
        return {
            "status": "error",
            "message": f"Database Error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }
    finally:
        # Clean up temporary file
        try:
            os.unlink(tmp_path)
        except:
            pass


def compare_results(user_result: List[Dict], expected_result: List[Dict]) -> bool:
    """
    Compare user's query result with expected result.
    - Number of rows must match
    - Column names may differ (aliases are allowed)
    - Row order doesn't matter
    - Values must match (with type tolerance)
    """
    if len(user_result) != len(expected_result):
        return False
    
    if len(user_result) == 0 and len(expected_result) == 0:
        return True
    
    # Convert all values to comparable format
    def normalize_value(val):
        if val is None:
            return None
        if isinstance(val, float):
            return round(val, 2)
        return val
    
    def normalize_row(row):
        return tuple(sorted(normalize_value(v) for v in row.values()))
    
    user_normalized = sorted([normalize_row(row) for row in user_result])
    expected_normalized = sorted([normalize_row(row) for row in expected_result])
    
    return user_normalized == expected_normalized
