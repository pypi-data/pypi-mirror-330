from typing import Dict, Optional, List
from psycopg.errors import Error as PsycopgError

from ...errors import TransactionError
from ...transaction import TransactionManager, IsolationLevel


class PostgreSQLTransactionManager(TransactionManager):
    """PostgreSQL transaction manager implementation"""

    # PostgreSQL supported isolation level mappings
    _ISOLATION_LEVELS: Dict[IsolationLevel, str] = {
        IsolationLevel.READ_UNCOMMITTED: "READ UNCOMMITTED",
        IsolationLevel.READ_COMMITTED: "READ COMMITTED",  # PostgreSQL default
        IsolationLevel.REPEATABLE_READ: "REPEATABLE READ",
        IsolationLevel.SERIALIZABLE: "SERIALIZABLE"
    }

    def __init__(self, connection):
        """Initialize PostgreSQL transaction manager

        Args:
            connection: PostgreSQL database connection
        """
        super().__init__()
        self._connection = connection
        self._active_savepoint = None
        self._savepoint_counter = 0
        self._deferred_constraints: List[str] = []
        self._is_deferrable = False
        self._active_transaction = False

    def _set_isolation_level(self) -> None:
        """Set transaction isolation level

        This is called at the start of each transaction
        """
        if self._isolation_level:
            level = self._ISOLATION_LEVELS.get(self._isolation_level)
            if level:
                try:
                    cursor = self._connection.cursor()
                    cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {level}")
                    cursor.close()
                except PsycopgError as e:
                    raise TransactionError(
                        f"Failed to set isolation level to {level}: {str(e)}"
                    )
            else:
                raise TransactionError(
                    f"Unsupported isolation level: {self._isolation_level}"
                )

    def set_deferrable(self, deferrable: bool = True) -> None:
        """Set transaction deferrable mode

        In PostgreSQL, DEFERRABLE only affects SERIALIZABLE transactions

        Args:
            deferrable: Whether constraints should be deferrable
        """
        self._is_deferrable = deferrable
        if self.is_active:
            raise TransactionError(
                "Cannot change deferrable mode of active transaction"
            )

    def defer_constraint(self, constraint_name: str) -> None:
        """Defer constraint checking until transaction commit

        Args:
            constraint_name: Name of the constraint to defer

        Raises:
            TransactionError: If constraint deferral fails
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"SET CONSTRAINTS {constraint_name} DEFERRED")
            cursor.close()
            self._deferred_constraints.append(constraint_name)
        except PsycopgError as e:
            raise TransactionError(f"Failed to defer constraint {constraint_name}: {str(e)}")

    def _do_begin(self) -> None:
        """Begin PostgreSQL transaction

        Sets isolation level and starts transaction

        Raises:
            TransactionError: If begin fails
        """
        try:
            # Set connection to non-autocommit mode
            if self._connection.autocommit:
                self._connection.autocommit = False

            # Start transaction with isolation level
            self._set_isolation_level()

            # Build BEGIN statement
            sql_parts = ["BEGIN"]

            # Add isolation level
            if self._isolation_level:
                level = self._ISOLATION_LEVELS.get(self._isolation_level)
                if level:
                    sql_parts.append(f"ISOLATION LEVEL {level}")

            # Add deferrable mode for SERIALIZABLE transactions
            if (self._isolation_level == IsolationLevel.SERIALIZABLE and
                    self._is_deferrable is not None):
                sql_parts.append(
                    "DEFERRABLE" if self._is_deferrable else "NOT DEFERRABLE"
                )

            # Execute BEGIN statement
            cursor = self._connection.cursor()
            cursor.execute(" ".join(sql_parts))
            cursor.close()

            self._active_transaction = True

        except PsycopgError as e:
            raise TransactionError(f"Failed to begin transaction: {str(e)}")

    def _do_commit(self) -> None:
        """Commit PostgreSQL transaction

        Raises:
            TransactionError: If commit fails
        """
        try:
            self._connection.commit()
            self._active_transaction = False
        except PsycopgError as e:
            raise TransactionError(f"Failed to commit transaction: {str(e)}")
        finally:
            self._active_savepoint = None
            self._savepoint_counter = 0
            self._deferred_constraints.clear()

    def _do_rollback(self) -> None:
        """Rollback PostgreSQL transaction

        Raises:
            TransactionError: If rollback fails
        """
        try:
            self._connection.rollback()
            self._active_transaction = False
        except PsycopgError as e:
            raise TransactionError(f"Failed to rollback transaction: {str(e)}")
        finally:
            self._active_savepoint = None
            self._savepoint_counter = 0
            self._deferred_constraints.clear()

    def _generate_savepoint_name(self) -> str:
        """Generate unique savepoint name

        Returns:
            str: Unique savepoint name
        """
        self._savepoint_counter += 1
        return f"SP_{self._savepoint_counter}"

    def _do_create_savepoint(self, name: str) -> None:
        """Create PostgreSQL savepoint

        Args:
            name: Savepoint name

        Raises:
            TransactionError: If create savepoint fails
        """
        try:
            # PostgreSQL requires active transaction for savepoints
            if not self.is_active:
                self._do_begin()

            cursor = self._connection.cursor()
            cursor.execute(f"SAVEPOINT {name}")
            cursor.close()
            self._active_savepoint = name
        except PsycopgError as e:
            raise TransactionError(f"Failed to create savepoint {name}: {str(e)}")

    def _do_release_savepoint(self, name: str) -> None:
        """Release PostgreSQL savepoint

        Args:
            name: Savepoint name

        Raises:
            TransactionError: If release savepoint fails
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"RELEASE SAVEPOINT {name}")
            cursor.close()
            if self._active_savepoint == name:
                self._active_savepoint = None
        except PsycopgError as e:
            raise TransactionError(f"Failed to release savepoint {name}: {str(e)}")

    def _do_rollback_savepoint(self, name: str) -> None:
        """Rollback to PostgreSQL savepoint

        Args:
            name: Savepoint name

        Raises:
            TransactionError: If rollback to savepoint fails
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"ROLLBACK TO SAVEPOINT {name}")
            cursor.close()
            if self._active_savepoint == name:
                self._active_savepoint = None
        except PsycopgError as e:
            raise TransactionError(
                f"Failed to rollback to savepoint {name}: {str(e)}"
            )

    def supports_savepoint(self) -> bool:
        """Check if savepoints are supported

        Returns:
            bool: Always True for PostgreSQL
        """
        return True

    def get_active_savepoint(self) -> Optional[str]:
        """Get name of active savepoint

        Returns:
            Optional[str]: Active savepoint name or None
        """
        return self._active_savepoint

    def get_deferred_constraints(self) -> List[str]:
        """Get list of currently deferred constraints

        Returns:
            List[str]: Names of deferred constraints
        """
        return self._deferred_constraints.copy()

    @property
    def is_active(self) -> bool:
        """Check if transaction is active

        Returns:
            bool: True if in transaction
        """
        if not self._connection or self._connection.closed:
            return False

        # By default, check based on autocommit mode
        if self._connection.autocommit:
            return False

        # If we've explicitly tracked transaction state, use that
        return self._active_transaction

    def get_current_isolation_level(self) -> IsolationLevel:
        """Get current transaction isolation level

        Returns:
            IsolationLevel: Current isolation level

        Raises:
            TransactionError: If getting isolation level fails
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute("SHOW transaction_isolation")
            result = cursor.fetchone()
            cursor.close()

            if result:
                # Convert PostgreSQL level name to IsolationLevel enum
                level_name = result[0].upper().replace(' ', '_')
                for isolation_level, pg_level in self._ISOLATION_LEVELS.items():
                    if pg_level.upper().replace(' ', '_') == level_name:
                        return isolation_level

            # Default to READ COMMITTED if not found
            return IsolationLevel.READ_COMMITTED

        except PsycopgError as e:
            raise TransactionError(
                f"Failed to get transaction isolation level: {str(e)}"
            )