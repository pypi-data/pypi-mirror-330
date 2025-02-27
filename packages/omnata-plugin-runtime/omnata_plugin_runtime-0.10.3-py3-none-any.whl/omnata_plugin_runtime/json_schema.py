"""
Models used to represent JSON schemas and Snowflake view definitions.
This was originally internal to the Sync Engine, but was moved to the
plugin runtime so that it could be used for testing column expressions (formulas, etc).
"""
from typing import Any, Dict, Optional, Literal, List, Union
from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator, computed_field
from jinja2 import Environment

class JsonSchemaProperty(BaseModel):
    """
    The most basic common properties for a JSON schema property, plus the extra ones we use for providing Snowflake-specific information.
    Used mainly to do partial parsing as we extract fields from within the schema
    """

    type: Optional[Union[str,List[str]]] = Field(..., description="The type of the property")
    ref: Optional[str] = Field(
        None, description="The reference to another schema", alias="$ref"
    )
    nullable: bool = Field(
        True, description="Whether the property is nullable"
    )
    description: Optional[str] = Field(
        None, description="The description of the property"
    )
    format: Optional[str] = Field(
        None, description="The format of the property, e.g. date-time"
    )
    properties: Optional[Dict[str, Self]] = Field(
        None, description="The sub-properties of the property, if the property is an object type"
    )
    snowflakeTimestampType: Optional[Literal['TIMESTAMP_TZ','TIMESTAMP_NTZ','TIMESTAMP_LTZ']] = Field(
        None, description="The Snowflake timestamp type to use when interpreting a date-time string."
    )
    snowflakeTimestampFormat: Optional[str] = Field(
        None, description="The Snowflake timestamp format to use when interpreting a date-time string."
    )
    snowflakePrecision: Optional[int] = Field(
        None, description="The Snowflake precision to assign to the column."
    )
    snowflakeScale: Optional[int] = Field(
        None, description="The Snowflake scale to assign to the column."
    )
    snowflakeColumnExpression: Optional[str] = Field(
        None,description="""When advanced processing is needed, you can provide a value here. Use {{variant_path}} to interpolate the path to the JSON field.""",
    )
    isJoinColumn: Optional[bool] = Field(
        False, description="Whether this column is sourced from a joined stream"
    )

    @model_validator(mode='after')
    def validate(self) -> Self:
        # If the type is a list, we need to condense it down to a single string
        if self.type is None:
            if self.ref is None:
                raise ValueError("You must provide either a type or a reference")
        else:
            if isinstance(self.type, list):
                data_types = [t for t in self.type if t != "null"]
                if len(data_types) == 0:
                    raise ValueError(
                        f"For a list of types, you must provide at least one non-null type ({self.type})"
                    )
                self.nullable = "null" in self.type
                self.type = data_types[0]
        return self
    
    @computed_field
    @property
    def precision(self) -> Optional[int]:
        """
        Returns the precision for this property.
        """
        precision = None
        if self.type == "number" or self.type == "integer":
            precision = 38
        if self.snowflakePrecision is not None:
            precision = self.snowflakePrecision
        return precision
    
    @computed_field
    @property
    def scale(self) -> Optional[int]:
        """
        Returns the scale for this property.
        """
        scale = None
        if self.type == "number":
            scale = 19
        if self.type == "integer":
            scale = 0
        if self.snowflakeScale is not None:
            scale = self.snowflakeScale
        return scale
    
    @computed_field
    @property
    def snowflake_data_type(self) -> str:
        """
        Returns the Snowflake data type for this property.
        """
        if self.type is not None:
            if self.type == "string":
                if self.format is not None:
                    if self.format == "date-time":
                        if self.snowflakeTimestampType is not None:
                            return self.snowflakeTimestampType
                        return "TIMESTAMP" # not sure if we should default to something that may vary according to account parameters
                    elif self.format == "time":
                        return "TIME"
                    elif self.format == "date":
                        return "DATE"
                return "VARCHAR"
            elif self.type == "number":
                return "NUMERIC"
            elif self.type == "integer":
                return "NUMERIC"
            elif self.type == "boolean":
                return "BOOLEAN"
            if self.type == "object":
                return "OBJECT"
            if self.type == "array":
                return "ARRAY"
            return "VARCHAR"
        elif self.ref is not None:
            if self.ref == "WellKnownTypes.json#definitions/Boolean":
                return "BOOLEAN"
            elif self.ref == "WellKnownTypes.json#definitions/Date":
                return "DATE"
            elif self.ref == "WellKnownTypes.json#definitions/TimestampWithTimezone":
                return "TIMESTAMP_TZ"
            elif self.ref == "WellKnownTypes.json#definitions/TimestampWithoutTimezone":
                return "TIMESTAMP_NTZ"
            elif self.ref == "WellKnownTypes.json#definitions/TimeWithTimezone":
                return "TIME"
            elif self.ref == "WellKnownTypes.json#definitions/TimeWithoutTimezone":
                return "TIME"
            elif self.ref == "WellKnownTypes.json#definitions/Integer":
                return "NUMERIC"
            elif self.ref == "WellKnownTypes.json#definitions/Number":
                return "NUMERIC"
            return "VARCHAR"


class SnowflakeViewColumn(BaseModel):
    """
    Represents everything needed to express a column in a Snowflake normalized view.
    The name is the column name, the expression is the SQL expression to use in the view.
    In other words, the column definition is "expression as name".
    """
    name: str
    expression: str
    comment: Optional[str] = Field(default=None)
    is_join_column: Optional[bool] = Field(
        default=False, description="Whether this column is sourced from a joined stream"
    )

    def __repr__(self) -> str:
        return "SnowflakeViewColumn(name=%r, definition=%r, comment=%r)" % (
            self.name,
            self.definition(),
            self.comment,
        )

    def definition(self) -> str:
        return f'{self.expression} as "{self.name}"'

    def name_with_comment(self,binding_list:Optional[List[Any]] = None) -> str:
        """
        Returns the column name (quoted), along with any comment.
        The resulting text can be used in a CREATE VIEW statement.
        If binding_list is provided, the comment will be added to the list, and a placeholder '?' will be used in the SQL.
        """
        if self.comment is None:
            return f'"{self.name}"'
        if binding_list is not None:
            binding_list.append(self.comment)
            return f'"{self.name}" COMMENT ?'
        return f'"{self.name}" COMMENT $${self.comment}$$'
    
    @classmethod
    def from_json_schema_property(cls,
                                  column_name:str,
                                  comment:str,
                                  variant_path:str,
                                  json_schema_property:JsonSchemaProperty,
                                  column_name_environment:Environment,
                                  column_name_expression:str) -> Self:
        """
        Takes a JSON schema property (which may be nested via variant_path), along with its final name and comment,
        and returns a SnowflakeViewColumn object which is ready to use in a select statement.
        It does this by applying overarching type conversion rules, and evaluating the final column name using Jinja.
        """
        jinja_vars = {"column_name": column_name}
        final_column_name = column_name_environment.from_string(column_name_expression).render(**jinja_vars)
        expression = f"""RECORD_DATA:{variant_path}"""
        if json_schema_property.snowflakeColumnExpression:
            jinja_vars = {"variant_path": expression}
            expression = column_name_environment.from_string(json_schema_property.snowflakeColumnExpression).render(
                **jinja_vars
            )
        
        if json_schema_property.precision is not None and json_schema_property.scale is not None and json_schema_property.snowflake_data_type == "NUMERIC":
            expression=f"{expression}::NUMERIC({json_schema_property.precision},{json_schema_property.scale})"
        elif json_schema_property.snowflakeTimestampType and json_schema_property.snowflakeTimestampFormat:
            timestamp_type = json_schema_property.snowflakeTimestampType
            timestamp_format = json_schema_property.snowflakeTimestampFormat
            expression=f"""TO_{timestamp_type}({expression}::varchar,'{timestamp_format}')"""
        else:
            if not json_schema_property.snowflakeColumnExpression:
                expression=f"""{expression}::{json_schema_property.snowflake_data_type}"""
        return cls(
            name=final_column_name,
            expression=expression,
            comment=comment,
            is_join_column=json_schema_property.isJoinColumn,
        )
    
    @classmethod
    def order_by_reference(cls,join_columns:List[Self]) -> List[Self]:
        """
        In some situations, column expressions may reference the alias of another column
        This is allowed in Snowflake, as long as the aliased column is defined before it's used in a later column
        So we need to sort the columns so that if the name of the column appears (in quotes) in the expression of another column, it is ordered first
        """
        
        # Collect columns to be moved
        columns_to_move:List[Self] = []
        for column in join_columns:
            for other_column in join_columns:
                if f'"{column.name}"' in other_column.expression:
                    if column not in columns_to_move:
                        columns_to_move.append(column)

        # Move collected columns to the front
        for column in columns_to_move:
            join_columns.remove(column)
            join_columns.insert(0, column)
        return join_columns


class SnowflakeViewJoin(BaseModel):
    """
    Represents a join in a Snowflake normalized view.
    """

    left_alias: str = Field(
        ..., description="The alias to use on the left side of the join"
    )
    left_column: str = Field(
        ..., description="The column to join on from the left side"
    )
    join_stream_name: str = Field(
        ..., description="The name of the stream to join (right side)"
    )
    join_stream_alias: str = Field(
        ...,
        description="The alias to use for the joined stream, this is used in the column definitions instead of the stream name, and accomodates the possibility of multiple joins to the same stream",
    )
    join_stream_column: str = Field(
        ..., description="The column to join on from the right side"
    )

    def __repr__(self) -> str:
        return (
            "SnowflakeViewJoin(left_alias=%r, left_column=%r, join_stream_name=%r, join_stream_alias=%r, join_stream_column=%r)"
            % (
                self.left_alias,
                self.left_column,
                self.join_stream_name,
                self.join_stream_alias,
                self.join_stream_column,
            )
        )

    def definition(self) -> str:
        """
        Returns the SQL for a single join in a normalized view
        """
        # we don't need to fully qualify the table name, because they'll be aliased in CTEs
        return f"""LEFT JOIN "{self.join_stream_name}" as "{self.join_stream_alias}" 
ON "{self.left_alias}"."{self.left_column}" = "{self.join_stream_alias}"."{self.join_stream_column}" """


class FullyQualifiedTable(BaseModel):
    """
    Represents a fully qualified table name in Snowflake, including database, schema, and table name.
    This is not a template, it's a fully specified object.
    """

    database_name: Optional[str] = Field(default=None, description="The database name")
    schema_name: str = Field(..., description="The schema name")
    table_name: str = Field(..., description="The table name")

    def get_fully_qualified_name(self, table_override: Optional[str] = None) -> str:
        """
        If table_override is provided, it will be used instead of the table name
        """
        actual_table_name = (
            self.table_name if table_override is None else table_override
        )
        # We try to make this resilient to quoting
        schema_name = self.schema_name.replace('"', "")
        table_name = actual_table_name.replace('"', "")
        if self.database_name is None or self.database_name == "":
            return f'"{schema_name}"."{table_name}"'
        database_name = self.database_name.replace('"', "")
        return f'"{database_name}"."{schema_name}"."{table_name}"'

    def get_fully_qualified_stage_name(self) -> str:
        """
        Stage name is derived from the table name
        """
        return self.get_fully_qualified_name(table_override=f"{self.table_name}_STAGE")

    def get_fully_qualified_criteria_deletes_table_name(self) -> str:
        """
        Deletes table name is derived from the table name
        """
        return self.get_fully_qualified_name(
            table_override=f"{self.table_name}_CRITERIA_DELETES"
        )

class SnowflakeViewPart(BaseModel):
    """
    Represents a stream within a normalized view.
    Because a normalized view can be built from multiple streams, this is potentially only part of the view.
    """
    stream_name: str = Field(..., description="The name of the stream")
    raw_table_location: FullyQualifiedTable = Field(
        ..., description="The location of the raw table that the stream is sourced from"
    )
    comment: Optional[str] = Field(
        None, description="The comment to assign to the view"
    )
    columns: List[SnowflakeViewColumn] = Field(
        ..., description="The columns to include in the view"
    )
    joins: List[SnowflakeViewJoin] = Field(
        ..., description="The joins to include in the view"
    )

    def direct_columns(self) -> List[SnowflakeViewColumn]:
        """
        Returns the columns that are not sourced from joins.
        """
        return [c for c in self.columns if not c.is_join_column]

    def join_columns(self) -> List[SnowflakeViewColumn]:
        """
        Returns the columns that are sourced from joins.
        """
        return SnowflakeViewColumn.order_by_reference([c for c in self.columns if c.is_join_column])

    def comment_clause(self) -> str:
        """
        Returns the comment clause for the view definition.
        """
        return f"COMMENT = $${self.comment}$$ " if self.comment is not None else ""

    def column_names_with_comments(self,binding_list:Optional[List[Any]] = None) -> List[str]:
        """
        Returns a list of column names with comments, suitable for use in a CREATE VIEW statement.
        This includes direct columns first, followed by join columns.
        If binding_list is provided, the comments will be added to the list, and a placeholder '?' will be used in the SQL.
        Otherwise, the comments will be included in the SQL inside of a '$$' delimiter.
        """
        # the outer view definition has all of the column names and comments, but with the direct columns
        # first and the join columns last, same as they are ordered in the inner query
        return [
            c.name_with_comment(binding_list) for c in (self.direct_columns() + self.join_columns())
        ]
    
    def cte_text(self) -> str:
        """
        Returns the CTE text for this view part.
        """
        return f""" "{self.stream_name}" as (
    select {', '.join([c.definition() for c in self.direct_columns()])} 
    from {self.raw_table_location.get_fully_qualified_name()}
) """

class SnowflakeViewParts(BaseModel):
    """
    Represents a set of streams within a normalized view.
    This is the top level object that represents the whole view.
    """

    main_part: SnowflakeViewPart = Field(
        ..., description="The main part of the view, which is the stream that the view is named after"
    )
    joined_parts: List[SnowflakeViewPart] = Field(
        ..., description="The other streams that are joined to the main stream"
    )

    def view_body(self):
        """
        Creates a view definition from the parts
        """
        ctes = [self.main_part.cte_text()] + [part.cte_text() for part in self.joined_parts]
        all_ctes = "\n,".join(ctes)
        join_columns = self.main_part.join_columns()
        join_column_clauses = [c.definition() for c in join_columns]
        # we select * from the original view (in the CTE) and then add any expressions that come from the join columns
        final_column_clauses = [f'"{self.main_part.stream_name}".*'] + join_column_clauses
        view_body = f"""with {all_ctes}
    select {', '.join(final_column_clauses)}
    from "{self.main_part.stream_name}" """
        if len(self.main_part.joins) > 0:
            join_clauses = [join.definition() for join in self.main_part.joins]
            view_body += "\n" + ("\n".join(join_clauses))
        return view_body

    @classmethod
    def generate(cls,
        raw_stream_locations: Dict[str,FullyQualifiedTable],
        stream_schemas: Dict[str,Dict],
        stream_name: str,
        include_default_columns: bool = True,
        column_name_environment: Environment = Environment(),
        column_name_expression: str = "{{column_name}}"
    ) -> Self:
        """
        Returns the building blocks required to create a normalized view from a stream.
        This includes any joins that are required, via CTEs.
        """
        # we start with the view parts for the view we are building
        main_stream_view_part = normalized_view_part(
            stream_name=stream_name,
            raw_table_location=raw_stream_locations[stream_name],
            include_default_columns=include_default_columns,
            stream_schema=stream_schemas.get(stream_name),
            column_name_environment=column_name_environment,
            column_name_expression=column_name_expression
        )
        joined_parts = []
        for join in main_stream_view_part.joins:
            if join.join_stream_name not in raw_stream_locations:
                raise ValueError(f"Stream {join.join_stream_name} is required as a join for stream {stream_name}, but its location was not provided")
            if join.join_stream_name not in stream_schemas:
                raise ValueError(f"Stream {join.join_stream_name} is required as a join for stream {stream_name}, but its schema was not provided")
            joined_parts.append(normalized_view_part(
                stream_name=join.join_stream_name,
                raw_table_location=raw_stream_locations[join.join_stream_name],
                include_default_columns=include_default_columns,
                stream_schema=stream_schemas[join.join_stream_name],
                column_name_environment=column_name_environment,
                column_name_expression=column_name_expression
            ))
        return cls(main_part=main_stream_view_part, joined_parts=joined_parts)

    

class JsonSchemaTopLevel(BaseModel):
    """
    This model is used as a starting point for parsing a JSON schema.
    It does not validate the whole thing up-front, as there is some complex recursion as well as external configuration.
    Instead, it takes the basic properties and then allows for further parsing on demand.
    """
    description: Optional[str] = Field(
        None, description="The description of the schema"
    )
    joins: Optional[List[SnowflakeViewJoin]] = Field(
        None, description="The joins to include in the view"
    )
    properties: Optional[Dict[str, Any]] = Field(
        None, description="The properties of the schema. This is left as a dictionary, and parsed on demand."
    )

    def build_view_columns(self,
            column_name_environment: Environment,                
            column_name_expression: str
        ) -> List[SnowflakeViewColumn]:
        """
        Returns a list of column definitions from a json schema
        """
        if self.properties is None:
            return []
        columns = [
            self._extract_view_columns(
                property_name=property_name,
                property_value=property_value,
                column_name_environment=column_name_environment,
                column_name_expression=column_name_expression,
            )
            for property_name, property_value in self.properties.items()
        ]
        return [item for sublist in columns for item in sublist]


    def _extract_view_columns(
        self,
        property_name: str,
        property_value: Dict,
        column_name_environment: Environment,                
        column_name_expression: str,
        current_field_name_path: List[str] = [],
        current_comment_path: List[str] = []
    ) -> List[SnowflakeViewColumn]:
        """
        Recursive function which returns a list of column definitions.
        - property_name is the name of the current property.
        - property_value is the value of the current property, (the JSON-schema node).
        - current_field_name_path is [] on initial entry, then contains parent path field names as it recurses.
        - current_comment_path is the same length as above, and contains any "description" values found on the way down
        """
        json_property = JsonSchemaProperty.model_validate(property_value)
        # bit of basic home-grown validation, could probably use a library for this
        if json_property.type:
            if json_property.type == "object":
                # TODO: make this depth configurable on the sync
                if len(current_field_name_path) < 5 and json_property.properties is not None:
                    children = [
                        self._extract_view_columns(
                            property_name=child_property_name,
                            property_value=child_property_value,
                            column_name_environment=column_name_environment,
                            column_name_expression=column_name_expression,
                            current_field_name_path=current_field_name_path + [property_name],
                            current_comment_path=current_comment_path + [json_property.description or ""],
                        )
                        for child_property_name, child_property_value in json_property.properties.items()
                    ]
                    return [item for sublist in children for item in sublist]

        current_field_name_path = current_field_name_path + [property_name]
        current_comment_path = current_comment_path + [
            json_property.description or ""
        ]
        # remove empty strings from current_comment_path
        current_comment_path = [c for c in current_comment_path if c]

        return [SnowflakeViewColumn.from_json_schema_property(
            column_name="_".join(current_field_name_path),
            comment=" -> ".join(current_comment_path),
            variant_path=":".join([f'"{p}"' for p in current_field_name_path if p]),
            json_schema_property=json_property,
            column_name_environment=column_name_environment,
            column_name_expression=column_name_expression
        )]
    

def normalized_view_part(
    stream_name:str,
    raw_table_location:FullyQualifiedTable,
    include_default_columns: bool,
    column_name_environment: Environment,                
    column_name_expression: str,
    stream_schema: Optional[Dict] = None,
) -> SnowflakeViewPart:
    """
    Returns an object containing:
    - A top level comment for the view
    - A list of SnowflakeViewColumn objects, representing the columns to create in the view
    - A list of SnowflakeViewJoin objects, representing the joins to create in the view
    """
    snowflake_columns: List[SnowflakeViewColumn] = []
    if include_default_columns:
        snowflake_columns.append(
            SnowflakeViewColumn(
                name="OMNATA_APP_IDENTIFIER",
                expression="APP_IDENTIFIER",
                comment="The value of the unique identifier for the record in the source system",
            )
        )
        snowflake_columns.append(
            SnowflakeViewColumn(
                name="OMNATA_RETRIEVE_DATE",
                expression="RETRIEVE_DATE",
                comment="The date and time the record was retrieved from the source system",
            )
        )
        snowflake_columns.append(
            SnowflakeViewColumn(
                name="OMNATA_RAW_RECORD",
                expression="RECORD_DATA",
                comment="The raw semi-structured record as retrieved from the source system",
            )
        )
        snowflake_columns.append(
            SnowflakeViewColumn(
                name="OMNATA_IS_DELETED",
                expression="IS_DELETED",
                comment="A flag to indicate that the record was deleted from the source system",
            )
        )
        snowflake_columns.append(
            SnowflakeViewColumn(
                name="OMNATA_RUN_ID",
                expression="RUN_ID",
                comment="A flag to indicate which run the record was last processed in",
            )
        )
    view_columns = snowflake_columns
    joins = []
    comment = None
    if stream_schema is not None:
        json_schema = JsonSchemaTopLevel.model_validate(stream_schema)
        view_columns += json_schema.build_view_columns(
            column_name_environment=column_name_environment,
            column_name_expression=column_name_expression
        )
        if json_schema.joins:
            joins = json_schema.joins
        comment = json_schema.description

    return SnowflakeViewPart(
        stream_name=stream_name,
        raw_table_location=raw_table_location,
        columns=view_columns,
        joins=joins,
        comment=comment
    )
