import json
import logging
import sqlite3
from typing import Any, Dict, List, Optional, Union, Callable
from ..query import Query, QueryOperator
from ..operations import BulkOperations
from ..aggregations import Aggregations, AggregateFunction

class Collection:
    """Collection interface for document operations."""
    
    def __init__(self, database, name: str):
        """Initialize collection with database connection and name."""
        self.database = database
        self.name = name
        self.validator = None
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Ensure collection exists with proper locking and error handling."""
        with self.database.pool.get_connection() as conn:
            try:
                conn.execute("BEGIN IMMEDIATE")  # Get an immediate lock
                cursor = conn.cursor()
                cursor.execute("SELECT metadata FROM collections WHERE name = ?", [self.name])
                result = cursor.fetchone()
                
                if result is None:
                    # Collection doesn't exist, create it
                    metadata = {"validator": None, "indexes": [], "options": {}}
                    cursor.execute(
                        "INSERT INTO collections (name, metadata) VALUES (?, ?)",
                        [self.name, json.dumps(metadata)]
                    )
                else:
                    # Collection exists, update timestamp and load validator
                    metadata = json.loads(result[0])
                    if metadata.get("validator"):
                        self.validator = metadata["validator"]
                    cursor.execute(
                        "UPDATE collections SET updated_at = CURRENT_TIMESTAMP WHERE name = ?",
                        [self.name]
                    )
                conn.commit()
            except Exception as e:
                conn.rollback()
                logging.error(f"Failed to initialize collection {self.name}: {e}")
                raise
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def print_collection(self):
        """Print a formatted view of the collection contents."""
        print_dict = {}
        with self.database.pool.get_connection() as conn:
            cursor = conn.cursor()
            # Use row factory to allow column name access
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM collections WHERE name = ?", [self.name])
            metadata_row = cursor.fetchone()
            if metadata_row:
                print_dict["metadata"] = json.loads(metadata_row["metadata"])
                print_dict["name"] = self.name
                
                cursor.execute("SELECT * FROM documents WHERE collection = ?", [self.name])
                print_dict["documents"] = [json.loads(row["data"]) for row in cursor.fetchall()]
                
                cursor.execute("SELECT * FROM indexes WHERE collection = ?", [self.name])
                print_dict["indexes"] = [json.loads(row["fields"]) for row in cursor.fetchall()]
                
                print(json.dumps(print_dict, indent=4, ensure_ascii=False))
            else:
                print(f"Collection '{self.name}' not found")
            conn.commit()
    
    def set_validator(self, validator_func: Callable[[Dict[str, Any]], bool]):
        """Set and persist document validator function."""
        self.validator = validator_func
        with self.database.pool.get_connection() as conn:
            try:
                conn.execute("BEGIN")
                cursor = conn.cursor()
                cursor.execute("SELECT metadata FROM collections WHERE name = ?", [self.name])
                metadata = json.loads(cursor.fetchone()[0])
                metadata["validator"] = validator_func.__name__  # Store function name for reference
                cursor.execute(
                    "UPDATE collections SET metadata = ? WHERE name = ?",
                    [json.dumps(metadata), self.name]
                )
                conn.commit()
            except Exception as e:
                conn.rollback()
                logging.error(f"Failed to set validator for collection {self.name}: {e}")
                raise
    
    def insert(self, document: Dict[str, Any], doc_id: Optional[str] = None) -> str:
        """Insert a document into the collection."""
        if self.validator and not self.validator(document):
            raise ValueError("Document failed validation")
        return self.database.insert(self.name, document, doc_id)
    
    def insert_many(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Insert multiple documents into the collection."""
        if not documents:
            return []
            
        # Validate documents if a validator is set
        if self.validator:
            for doc in documents:
                if not self.validator(doc):
                    raise ValueError("Document failed validation")
        
        # Use bulk operations with proper transaction handling
        with self.database.pool.get_connection() as conn:
            try:
                conn.execute("BEGIN IMMEDIATE")
                ops = BulkOperations(conn)
                doc_ids = ops.bulk_insert(self.name, documents)
                conn.commit()
                return doc_ids
            except Exception as e:
                conn.rollback()
                logging.error(f"Failed to insert documents in bulk: {e}")
                raise
    
    def find(self, query: Optional[Union[Dict[str, Any], Query]] = None) -> List[Dict[str, Any]]:
        """Find documents in the collection."""
        if isinstance(query, dict):
            # Convert dict to Query object optimized for indexes
            base_query = Query()
            base_query.collection = self.name
            base_query.database = self.database

            # Handle full text search query with "*" field
            if len(query) == 1 and "*" in query and isinstance(query["*"], dict) and "$contains" in query["*"]:
                search_term = query["*"]["$contains"]
                return self.search_text(search_term)
            sorted_fields = []
            indexes = self.database.list_indexes(self.name)
            for index in indexes:
                index_fields = index['fields']
                if isinstance(index_fields, str):
                    index_fields = json.loads(index_fields)
                if isinstance(index_fields, list):
                    for field in index_fields:
                        if field in query and field not in sorted_fields:
                            sorted_fields.append(field)
            
            remaining_fields = [f for f in query.keys() if f not in sorted_fields]
            sorted_fields.extend(remaining_fields)

            for field in sorted_fields:
                value = query[field]
                if isinstance(value, dict):
                    for op, val in value.items():
                        op = op.lstrip("$")
                        if op == "gt":
                            base_query.where(field, QueryOperator.GT, val)
                        elif op == "gte":
                            base_query.where(field, QueryOperator.GTE, val)
                        elif op == "lt":
                            base_query.where(field, QueryOperator.LT, val)
                        elif op == "lte":
                            base_query.where(field, QueryOperator.LTE, val)
                        elif op == "ne":
                            base_query.where(field, QueryOperator.NE, val)
                        elif op == "in":
                            base_query.where(field, QueryOperator.IN, val)
                        elif op == "contains":
                            base_query.where(field, QueryOperator.CONTAINS, val)
                else:
                    base_query.where(field, QueryOperator.EQ, value)
            
            return base_query.execute()

        elif isinstance(query, Query):
            query.collection = self.name
            query.database = self.database
            return query.execute()
        else:
            base_query = Query()
            base_query.collection = self.name
            base_query.database = self.database
            return base_query.execute()
    
    def find_one(self, query: Optional[Union[Dict[str, Any], Query]] = None) -> Optional[Dict[str, Any]]:
        """Find a single document in the collection."""
        if query is None:
            query = Query(self.name, self.database)
            query.limit(1)
            results = query.execute()
            return results[0] if results else None
        
        if isinstance(query, dict):
            base_query = Query(self.name, self.database)
            for field, value in query.items():
                if isinstance(value, dict):
                    for op, val in value.items():
                        op = op.lstrip("$")
                        if op == "gte":
                            base_query.where(field, QueryOperator.GTE, val)
                        elif op == "lte":
                            base_query.where(field, QueryOperator.LTE, val)
                        elif op == "in":
                            base_query.where(field, QueryOperator.IN, val)
                        elif op == "contains":
                            base_query.where(field, QueryOperator.CONTAINS, val)
                        else:
                            base_query.where(field, QueryOperator.EQ, val)
                else:
                    base_query.where(field, QueryOperator.EQ, value)
            base_query.limit(1)
            results = base_query.execute()
            return results[0] if results else None
        
        # If it's already a Query object
        query.collection = self.name
        query.database = self.database
        query.limit(1)
        results = query.execute()
        return results[0] if results else None
    
    def update(self, query: Union[Dict[str, Any], Query], update: Dict[str, Any]) -> int:
        """Update documents in the collection."""
        if isinstance(query, Query):
            query_dict = query.to_dict()
        else:
            query_dict = query

        # Wrap update in $set if not already wrapped
        if not any(key.startswith('$') for key in update.keys()):
            update = {'$set': update}

        return self.database.update(self.name, query_dict, update)
    
    def delete(self, query: Union[Dict[str, Any], Query]) -> int:
        """Delete documents matching query."""
        if isinstance(query, Query):
            query_dict = query.to_dict()
        else:
            query_dict = query

        return self.database.delete(self.name, query_dict)

    def all(self, limit: int = None, skip: int = None, sort: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Get all documents in the collection with pagination and sorting.
        
        Args:
            limit: Maximum number of documents to return
            skip: Number of documents to skip
            sort: Dictionary of field names and sort direction ('asc' or 'desc')
        """
        query = Query(self.name, self.database)
        
        if limit is not None:
            query.limit(limit)
        if skip is not None:
            query.skip(skip)
            
        if sort:
            sql_parts = []
            for field, direction in sort.items():
                if direction.lower() not in ('asc', 'desc'):
                    raise ValueError("Sort direction must be 'asc' or 'desc'")
                sql_parts.append(f"json_extract(data, '$.{field}') {direction.upper()}")
            query.order_by(sql_parts)
            
        return query.execute()

    def count(self, filter_query: Optional[Union[Dict[str, Any], Query]] = None) -> int:
        """
        Get the number of documents in the collection.
        
        Args:
            filter_query: Optional filter criteria
        """
        with self.database.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            if filter_query is None:
                # Fast count without filtering
                cursor.execute(
                    "SELECT COUNT(*) FROM documents WHERE collection = ?",
                    [self.name]
                )
            else:
                # Convert filter to Query if needed
                if isinstance(filter_query, dict):
                    query = Query(self.name, self.database)
                    for field, value in filter_query.items():
                        if isinstance(value, dict):
                            for op, val in value.items():
                                op = op.lstrip("$")
                                if op in ("gt", "lt", "gte", "lte", "ne"):
                                    query.where(field, getattr(QueryOperator, op.upper()), val)
                                elif op == "in":
                                    query.where(field, QueryOperator.IN, val)
                                elif op == "contains":
                                    query.where(field, QueryOperator.CONTAINS, val)
                        else:
                            query.where(field, QueryOperator.EQ, value)
                else:
                    query = filter_query
                
                # Build and execute filtered count query
                conditions = []
                params = [self.name]
                
                for field, op, value in query.conditions:
                    if value is None:
                        conditions.append("json_extract(data, ?) IS NULL")
                        params.append(f"$.{field}")
                    else:
                        if op == QueryOperator.CONTAINS:
                            conditions.append("json_extract(data, ?) LIKE ?")
                            params.extend([f"$.{field}", f"%{value}%"])
                        elif op == QueryOperator.IN:
                            placeholders = ','.join(['?' for _ in value])
                            conditions.append(f"json_extract(data, ?) IN ({placeholders})")
                            params.append(f"$.{field}")
                            params.extend(value)
                        else:
                            op_map = {
                                QueryOperator.EQ: "=",
                                QueryOperator.GT: ">",
                                QueryOperator.GTE: ">=",
                                QueryOperator.LT: "<",
                                QueryOperator.LTE: "<=",
                                QueryOperator.NE: "!="
                            }
                            conditions.append(f"json_extract(data, ?) {op_map[op]} ?")
                            params.extend([f"$.{field}", value])
                
                where_clause = " AND ".join(conditions) if conditions else "1"
                cursor.execute(
                    f"SELECT COUNT(*) FROM documents WHERE collection = ? AND {where_clause}",
                    params
                )
            
            return cursor.fetchone()[0]

    def f_count(self) -> int:
        """Get the number of documents in the collection."""
        query = Query(self.name, self.database)
        return query.count()
    def delete_many(self, query: Optional[Union[Dict[str, Any], Query]] = None) -> int:
        """Delete multiple documents from the collection."""
        if query is None:
            query = {}
        return self.delete(query)
    
    def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute an aggregation pipeline."""
        agg = Aggregations(self.database)
        return agg.execute_pipeline(self.name, pipeline)
    
    def search_text(self, search_term: str, fields: Optional[List[str]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Perform a full text search on the collection.
        
        This method attempts to use a full-text search index if one exists.
        If no FTS index is available, it falls back to a slower full document scan.
        
        Args:
            search_term: Text to search for
            fields: Specific fields to search (if None, searches all fields)
            limit: Maximum number of results to return
            
        Returns:
            List of matching documents
        """
        # Check if we have any full-text search indexes for this collection
        with self.database.pool.get_connection() as conn:
            # First, try to find a FTS index for this collection
            fts_indexes = []
            cursor = conn.cursor()
            
            # Look for FTS virtual tables
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name LIKE 'fts_%' AND name LIKE ?
            """, [f"%{self.name}%"])
            
            fts_indexes = [row[0] for row in cursor.fetchall()]
            
            # If we have FTS indexes, use them for the search
            if fts_indexes:
                # Use the first FTS index
                fts_table = fts_indexes[0]
                
                # Check if specific fields were requested
                if fields:
                    # Only search in specified fields that exist in the index
                    # First, get the columns in the FTS table
                    cursor.execute(f"PRAGMA table_info({fts_table})")
                    available_fields = [row[1] for row in cursor.fetchall()]
                    
                    # Filter out requested fields that don't exist in the index
                    search_fields = [f for f in fields if f.replace('.', '_') in available_fields]
                    
                    if search_fields:
                        # Create a search query using the specified fields
                        search_expr = " OR ".join(f"{f.replace('.', '_')}:'{search_term}'" for f in search_fields)
                        cursor.execute(f"""
                            SELECT d.data
                            FROM documents d
                            JOIN {fts_table} f ON d.id = f.id
                            WHERE f.{fts_table} MATCH ? AND d.collection = ?
                            LIMIT ?
                        """, [search_expr, self.name, limit])
                    else:
                        # Fall back to standard search if no fields match
                        cursor.execute(f"""
                            SELECT d.data
                            FROM documents d
                            JOIN {fts_table} f ON d.id = f.id
                            WHERE f.{fts_table} MATCH ? AND d.collection = ?
                            LIMIT ?
                        """, [search_term, self.name, limit])
                else:
                    # Search across all fields in the FTS index
                    cursor.execute(f"""
                        SELECT d.data
                        FROM documents d
                        JOIN {fts_table} f ON d.id = f.id
                        WHERE f.{fts_table} MATCH ? AND d.collection = ?
                        LIMIT ?
                    """, [search_term, self.name, limit])
                
                # Process results
                return [json.loads(row[0]) for row in cursor.fetchall()]
            
            # Fallback: No FTS index, perform a full scan
            # Get all documents first
            all_docs = list(self.find({}))
            
            def search_value(value: Any, term: str) -> bool:
                """Recursively search through any value type for the search term."""
                if isinstance(value, str):
                    return term.lower() in value.lower()
                elif isinstance(value, (int, float)):
                    return term.lower() in str(value).lower()
                elif isinstance(value, dict):
                    return any(search_value(v, term) for v in value.values())
                elif isinstance(value, (list, tuple)):
                    return any(search_value(item, term) for item in value)
                return False
            
            # If specific fields are requested, only search in those fields
            if fields:
                results = []
                for doc in all_docs:
                    for field in fields:
                        # Handle nested fields
                        parts = field.split('.')
                        value = doc
                        for part in parts:
                            if isinstance(value, dict) and part in value:
                                value = value[part]
                            else:
                                value = None
                                break
                        
                        if value is not None and search_value(value, search_term):
                            results.append(doc)
                            break
            else:
                # Search in all fields
                results = [
                    doc for doc in all_docs 
                    if any(search_value(value, search_term) for value in doc.values())
                ]
            
            return results[:limit]
    
    def bulk_operations(self) -> BulkOperations:
        """Get bulk operations interface."""
        return self.database.bulk_operations()