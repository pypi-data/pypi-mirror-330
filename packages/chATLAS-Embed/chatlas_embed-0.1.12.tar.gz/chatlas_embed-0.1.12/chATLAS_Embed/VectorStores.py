# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# chATLAS_Embed is free software; you can redistribute it and/or modify
# it under the terms of Apache 2.0 license; see LICENSE file for more details.
# `chATLAS_Embed/VectorStores.py`

"""
A collection of VectorStores.
"""
# For whoever next comes to debug or improve the functionality of this code, I am deeply sorry.
# For whatever dodgy SQL I eventually managed to hack together and the sprawling mess of functions and commands.

import json
import math
import re
import time
from typing import List, Tuple

from datasets.utils.deprecation_utils import deprecated
from sqlalchemy import bindparam
from sqlalchemy import create_engine, inspect
from sqlalchemy.sql import text
from sqlalchemy.exc import ProgrammingError, SQLAlchemyError, DataError
from tqdm import tqdm

from .Base import VectorStore, EmbeddingModel, Document
from .custom_stop_words import get_physics_stopwords


class PostgresParentChildVectorStore(VectorStore):
    """PostgresSQL-based vector store with pgvector extension."""

    def __init__(
        self,
        connection_string: str,
        embedding_model: EmbeddingModel,
        _update_vector_size=False,
        dictionary_type="english",
        **kwargs,
    ):
        """
        PostgresSQL-based vector store initialisation.

        Once done with the vectorstore make sure to close it by `PostgresParentChildVectorStore.close()`,
        `del PostgresParentChildVectorStore` or wrapping the usage of the vectorstore in a `with`.

        :param str connection_string:  connection string to connect to the postgres database used.
            e.g. postgresql://{user}:{password}@dbod-chatlas.cern.ch:{port}/vTEST
        :param EmbeddingModel embedding_model: Embedding model used to generate vector store
            (and used to process queries to search the db)
        :param bool _update_vector_size: Debugging parameter for using embedding models with different vector sizes
            - **NOTE** if set to true and used with a different embeding model will drop previously made embeddings
        :param str dictionary_type: "english" | "simple" | "scientific" -> What postgres dictionary to use for the
            text search.
            - "simple": Doesn't remove or stem anything - better matches for specific terms, but about 2x runtime of
                        english
            - "english": Uses pg English dictionary stop words and stems.
            - "scientific": Custom dictionary that currently works the same as english, but has scope to be extended
                (ie with other languages)
        :param kwargs: Additional args:
            - [str] custom_stop_words: List of strings containing custom stop words for scientific documents
                to exclude
        """

        super().__init__()
        self.connection_string = connection_string
        self.embedding_model = embedding_model
        self._ensure_database_exists()
        self.engine = create_engine(self.connection_string)
        self.vector_length = embedding_model.vector_size
        self._update_vector_size = _update_vector_size
        self.dictionary_type = dictionary_type
        self.kwargs = kwargs
        self.stop_words: [str] = []
        self._init_db()

    def _extract_db_info(self):
        """Extract database name and connection info from connection string."""
        pattern = r"(?P<base>postgresql://[^/]+)/(?P<dbname>[^?]+)"
        match = re.match(pattern, self.connection_string)
        if not match:
            raise ValueError("Invalid connection string format")

        return {
            "base_connection": match.group("base"),
            "database_name": match.group("dbname"),
        }

    def _ensure_database_exists(self):
        """Create database if it doesn't exist."""
        db_info = self._extract_db_info()
        base_connection = db_info["base_connection"]
        database_name = db_info["database_name"]

        # Connect to default 'postgres' database to create new database
        default_connection = f"{base_connection}/postgres"
        temp_engine = create_engine(default_connection)

        try:
            with temp_engine.connect() as conn:
                # Start transaction
                with conn.begin():
                    # Check if database exists
                    result = conn.execute(
                        text(f"SELECT 1 FROM pg_database WHERE datname = :dbname"),
                        {"dbname": database_name},
                    ).scalar()

                    if not result:
                        # Terminate existing connections
                        conn.execute(
                            text(
                                f"""
                                SELECT pg_terminate_backend(pid)
                                FROM pg_stat_activity
                                WHERE datname = :dbname
                            """
                            ),
                            {"dbname": database_name},
                        )
                        # Create database
                        # Note: We need to commit the transaction before creating the database
                        conn.execute(text(f"COMMIT"))
                        conn.execute(text(f'CREATE DATABASE "{database_name}"'))

        except Exception as e:
            print(f"Failed to create database: {str(e)}")
            raise
        finally:
            temp_engine.dispose()

    def _init_text_parser(self, stop_words: List[str]):
        """
        Initialize or update the text cleaning function in PostgreSQL.
        Creates a function that removes URLs, file paths, IP addresses, and version numbers from text.

        :param stop_words: List of stop words to remove
        :type stop_words: List[str]
        :return:
        :rtype:
        """

        # Format stop words for PostgreSQL
        pg_stop_words = "'" + "', '".join(stop_words) + "'"

        query_text = f"""
        CREATE OR REPLACE FUNCTION clean_text_for_vector(
            input_text text,
            stop_words text[] DEFAULT ARRAY[{pg_stop_words}]  -- adjust custom stopwords as needed
        )
        RETURNS text AS $$
        DECLARE
            pattern text;
            cleaned_text text;
        BEGIN
            -- If there are any custom stop words provided, build a regex pattern to match them
            IF array_length(stop_words, 1) IS NOT NULL THEN
                pattern := '\m(' || array_to_string(
                    ARRAY(
                        SELECT regexp_replace(word, '([.^$*+?()\[\]\\|])', '\\\1', 'g')
                        FROM unnest(stop_words) AS word
                    ),
                    '|'
                ) || ')\M';
                cleaned_text := regexp_replace(input_text, pattern, ' ', 'gi');
            ELSE
                cleaned_text := input_text;
            END IF;

            -- Remove URLs
            cleaned_text := regexp_replace(cleaned_text, 'https?://[^\s]+', '', 'g');
            -- Remove IP addresses
            cleaned_text := regexp_replace(cleaned_text, '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '', 'g');
            -- Replace underscores and hyphens with space
            cleaned_text := regexp_replace(cleaned_text, '[_-]', ' ', 'g');
            -- Replace punctuation with space
            cleaned_text := regexp_replace(cleaned_text, '[[:punct:]]', ' ', 'g');

            RETURN cleaned_text;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;
        """

        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    # Create or replace the function
                    conn.execute(text(query_text))

        except SQLAlchemyError as e:
            print(f"Failed to create/update clean_text_for_vector function: {str(e)}")
            raise

    def _init_scientific_dictionary(self):
        """
        Sets up the scientific dictionary for text parsing use. The scientific dictionary:

        1. Removes English Stop words
        2. Stems recognised English words
        3. Leaves all other words unchanged

        The text is then always parsed with  clean_text_for_vector which removes the custom list of HEP stopwords

        :return:
        :rtype:
        """
        scientific_dict_creation_text = """
        DROP TEXT SEARCH CONFIGURATION IF EXISTS public.scientific CASCADE;
        DROP TEXT SEARCH DICTIONARY IF EXISTS public.scientific_stem CASCADE;
        DROP TEXT SEARCH DICTIONARY IF EXISTS public.scientific_english_stop CASCADE;

        -- Create dictionary for English stop words and stemming
        CREATE TEXT SEARCH DICTIONARY public.scientific_english_stop (
            TEMPLATE = pg_catalog.snowball,
            LANGUAGE = english,
            STOPWORDS = english
        );

        -- Create the stemming dictionary
        CREATE TEXT SEARCH DICTIONARY public.scientific_stem (
            TEMPLATE = pg_catalog.snowball,
            LANGUAGE = english
        );

        -- Create the configuration
        CREATE TEXT SEARCH CONFIGURATION public.scientific (
            COPY = pg_catalog.english
        );

        ALTER TEXT SEARCH CONFIGURATION public.scientific
            ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, word, hword, hword_part
            WITH scientific_english_stop, scientific_stem;
            """
        # Execute the SQL
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(text(scientific_dict_creation_text))

    def get_current_stop_words(self):
        """
        Returns current stop words used for processing the DB.

        **NOTE**: This nay not be right if a separate instance of this class
        connected to the same DB and they have altered the stop words list independently.

        :return: stop words
        :rtype: List[str]
        """
        # NOTE:
        # We could store what stop words are currently being used in a table in the SQL and query it to get the proper
        # up-to-date version of this across users, however don't really want to update stop words regularly anyway
        # as it hsa a very large time penalty. Best to just leave this alone!

        return self.stop_words

    def update_current_stop_words(self, stop_words: List[str]):
        """
        Updates the current stored list of stop words with a new list.

        **NOTE**: This will update the text search vector for all users on this DB! Only do this on non prod DBs!
        It also has a very high time cost for the operation needing to update all parent document rows with regex!

        :return: number of rows updated
        :rtype: int
        """
        self._init_text_parser(stop_words)
        num = self.update_text_search_vector()
        return num

    @deprecated("version 0.1.10")
    def _init_scientific_dictionary_old(self, custom_stop_words=None):
        """
        **NOTE**: Legacy function to show an alternative method to the regex stripping of

        Creates a custom PostgreSQL text search dictionary named 'scientific' and text to search vector that:
        1. Stems English words and removes English stop words
        2. Removes custom stop words
        3. Leaves other words unchanged

        :param custom_stop_words: List of strings to use as stop words for scientific documents
        :type custom_stop_words: List[str]
        """
        # Create temporary stop words
        saved_hep_stop_words = get_physics_stopwords()
        stop_words = list(set(saved_hep_stop_words + (custom_stop_words or [])))

        # Format stop words for PostgreSQL
        pg_stop_words = "'" + "', '".join(stop_words) + "'"

        setup_commands = [
            # Create the custom stop words table if it doesn't exist
            """
            CREATE TABLE IF NOT EXISTS custom_stop_words (
                word text PRIMARY KEY
            );
            """,
            # Clear existing stop words to avoid duplicates
            """
            TRUNCATE custom_stop_words;
            """,
            # Insert custom stop words
            f"""
                INSERT INTO custom_stop_words (word)
                SELECT unnest(ARRAY[{pg_stop_words}]);
            """,
            # Create a materialized view of stop words for IMMUTABLE function usage
            """
            DROP MATERIALIZED VIEW IF EXISTS custom_stop_words_mv;
            CREATE MATERIALIZED VIEW custom_stop_words_mv AS
            SELECT word FROM custom_stop_words;
            CREATE UNIQUE INDEX IF NOT EXISTS custom_stop_words_mv_idx ON custom_stop_words_mv(word);
            """,
            # Drop the existing configuration and dictionaries if they exist
            """
            DROP TEXT SEARCH CONFIGURATION IF EXISTS scientific CASCADE;
            DROP TEXT SEARCH DICTIONARY IF EXISTS scientific_stem CASCADE;
            DROP FUNCTION IF EXISTS filter_custom_stopwords(tsvector);
            DROP FUNCTION IF EXISTS to_tsvector_with_custom_stops(regconfig, text);
            """,
            # Create the scientific stemming dictionary
            """
            CREATE TEXT SEARCH DICTIONARY scientific_stem (
                TEMPLATE = snowball,
                LANGUAGE = english,
                STOPWORDS = english
            );
            """,
            # Create the text search configuration
            """
            CREATE TEXT SEARCH CONFIGURATION scientific (COPY = english);
            """,
            # Set up the configuration to use our dictionaries in sequence
            """
            ALTER TEXT SEARCH CONFIGURATION scientific
            ALTER MAPPING FOR asciiword, asciihword, hword_asciipart,
                              word, hword, hword_part
            WITH scientific_stem, simple;
            """,
            # Create a function to filter out custom stop words
            """
            CREATE OR REPLACE FUNCTION filter_custom_stopwords(IN text_vector tsvector)
            RETURNS tsvector
            LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE AS
            $$
            DECLARE
                result tsvector := ''::tsvector;
                lexemes text[];
            BEGIN
                SELECT ARRAY(
                    SELECT (lexeme || CASE
                        WHEN positions IS NOT NULL THEN ':' || array_to_string(positions, ',')
                        ELSE ''
                    END)::text
                    FROM unnest(text_vector) AS t(lexeme, positions)
                    WHERE lexeme NOT IN (SELECT word FROM custom_stop_words_mv)
                ) INTO lexemes;

                IF array_length(lexemes, 1) > 0 THEN
                    SELECT array_to_tsvector(lexemes) INTO result;
                END IF;

                RETURN result;
            END;
            $$;
            """,
            # Create a wrapper function to use in text search
            """
            CREATE OR REPLACE FUNCTION to_tsvector_with_custom_stops(config regconfig, document text)
            RETURNS tsvector
            LANGUAGE plpgsql IMMUTABLE PARALLEL SAFE AS
            $$
            BEGIN
                RETURN filter_custom_stopwords(to_tsvector(config, document));
            END;
            $$;
            """,
            # Create an index refresh function
            """
            CREATE OR REPLACE FUNCTION refresh_custom_stopwords()
            RETURNS void
            LANGUAGE plpgsql
            AS $$
            BEGIN
                REFRESH MATERIALIZED VIEW CONCURRENTLY custom_stop_words_mv;
            END;
            $$;
            """,
        ]

        # Execute all setup commands within a single transaction
        with self.engine.connect() as conn:
            with conn.begin():
                for command in setup_commands:
                    conn.execute(text(command))

    def _init_db(self):
        """Initialize database schema and extensions."""
        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    # Create vector extension
                    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

                    saved_hep_stop_words = get_physics_stopwords()

                    # Initialize scientific dictionary
                    self._init_scientific_dictionary()

                    # Initialize text parser
                    self._init_text_parser(saved_hep_stop_words)

                    # Create base documents table
                    conn.execute(
                        text(
                            """
                        CREATE TABLE IF NOT EXISTS documents (
                            id TEXT PRIMARY KEY,
                            page_content TEXT,
                            metadata JSONB,
                            parent_id TEXT
                        )
                    """
                        )
                    )

                    # Add text_search_vector column
                    conn.execute(
                        text(
                            """
                        ALTER TABLE documents
                        ADD COLUMN IF NOT EXISTS text_search_vector tsvector
                    """
                        )
                    )

                    # Now create the GIN index
                    conn.execute(
                        text(
                            """
                        CREATE INDEX IF NOT EXISTS documents_text_search_idx
                        ON documents USING gin(text_search_vector)
                    """
                        )
                    )

                    # Update existing vectors
                    conn.execute(
                        text(
                            f"""
                            UPDATE documents
                            SET text_search_vector =
                                setweight(
                                    to_tsvector('{self.dictionary_type}',
                                    clean_text_for_vector(COALESCE(page_content, ''))),
                                    'A'
                                ) ||
                                setweight(
                                    to_tsvector('{self.dictionary_type}',
                                    clean_text_for_vector(COALESCE(metadata->>'topic_parent', ''))),
                                    'C'
                                ) ||
                                setweight(
                                    to_tsvector('{self.dictionary_type}',
                                    clean_text_for_vector(COALESCE(metadata->>'name', ''))),
                                    'B'
                                )
                            WHERE parent_id IS NULL
                            AND text_search_vector IS NULL
                    """
                        )
                    )

                # Check if the embeddings table exists
                result = conn.execute(
                    text(
                        """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'embeddings'
                    )
                """
                    )
                )
                table_exists = result.scalar()

                if table_exists:
                    # Check the existing dimension of the embeddings column
                    conn.execute(
                        text(
                            """
                            ALTER TABLE embeddings
                            DROP CONSTRAINT IF EXISTS embeddings_document_id_fkey
                            """
                        )
                    )

                    # Add the new constraint with CASCADE
                    conn.execute(
                        text(
                            """
                            ALTER TABLE embeddings
                            ADD CONSTRAINT embeddings_document_id_fkey
                            FOREIGN KEY (document_id)
                            REFERENCES documents(id)
                            ON DELETE CASCADE
                            """
                        )
                    )
                    result = conn.execute(
                        text(
                            """
                        SELECT pg_catalog.format_type(a.atttypid, a.atttypmod) AS type
                        FROM pg_catalog.pg_attribute a
                        WHERE a.attname = 'embedding' AND a.attrelid = (
                            SELECT c.oid FROM pg_catalog.pg_class c
                            WHERE c.relname = 'embeddings' AND c.relkind = 'r'
                        )
                    """
                        )
                    )
                    row = result.fetchone()

                    if row:
                        current_vector_type = row[0]  # Format: "vector(384)"
                        current_dimension = int(
                            current_vector_type.split("(")[1].rstrip(")")
                        )

                        # If dimensions differ, update the table schema
                        if current_dimension == self.vector_length:
                            pass
                        elif (
                            current_dimension != self.vector_length
                            and self._update_vector_size
                        ):
                            conn.execute(
                                text(
                                    "ALTER TABLE embeddings DROP COLUMN IF EXISTS embedding"
                                )
                            )
                            conn.execute(
                                text(
                                    f"ALTER TABLE embeddings ADD COLUMN embedding vector({self.vector_length})"
                                )
                            )
                        else:
                            raise ValueError(
                                """
                            The embedding model output vector size used does not match the one used to create the db.
                             Set `_update_vector_size` to True if trying to update the vectors in the database"""
                            )
                    else:
                        # If the embedding column doesn't exist, create it
                        conn.execute(
                            text(
                                f"ALTER TABLE embeddings ADD COLUMN embedding vector({self.vector_length})"
                            )
                        )
                else:
                    # Create the embeddings table if it doesn't exist
                    conn.execute(
                        text(
                            f"""
                            CREATE TABLE embeddings (
                                id TEXT PRIMARY KEY,
                                document_id TEXT REFERENCES documents(id) ON DELETE CASCADE,
                                embedding vector({self.vector_length})
                            )
                        """
                        )
                    )

                # Create the vector index
                conn.execute(
                    text(
                        """
                    CREATE INDEX IF NOT EXISTS embeddings_vector_idx
                    ON embeddings
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 250)
                """
                    )
                )

                # Set ivfflat probes
                conn.execute(text("SET ivfflat.probes = 32"))

                conn.commit()

        except Exception as e:
            print(f"Failed to initialize database schema: {str(e)}")
            raise

    def close(self):
        """Explicitly close and dispose of database connections"""
        if hasattr(self, "engine"):
            self.engine.dispose()

    def __del__(self):
        """Ensure connections are closed when object is deleted"""
        self.close()

    def __enter__(self):
        """Support context manager protocol"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatically close connections when exiting context"""
        self.close()

    ############################################################
    # NOTE FROM BEN E:
    # This function could be sped up with better SQL operations
    # this would definitely be nice, however only needs to be
    # run once when initialy setting up the db then
    # only runs on updated documents which there are never too
    # many of so not a huge concern.
    # (Definitely would be nice if we have good SQL enginners to improve this)
    ############################################################

    def add_documents(
        self, parent_docs: List[Document], child_docs: List[Document]
    ) -> None:
        """
        Add parent documents and child documents to the database.

        :param List[Document] parent_docs: Parent documents to add ot the db
        :param List[Document] child_docs: Child documents to embed and add to db
        """
        with self.engine.connect() as conn:
            with conn.begin():
                # Insert parent documents
                for parent_doc in tqdm(parent_docs, "Adding Parent Documents"):
                    conn.execute(
                        text(
                            """
                            INSERT INTO documents (id, page_content, metadata, parent_id)
                            VALUES (:id, :page_content, :metadata, NULL)
                            ON CONFLICT (id) DO NOTHING
                        """
                        ),
                        {
                            "id": parent_doc.id,
                            "page_content": parent_doc.page_content,
                            "metadata": json.dumps(parent_doc.metadata),
                        },
                    )

                # Insert child documents and embeddings
                for child_doc in tqdm(child_docs, "Adding Child Documents"):
                    conn.execute(
                        text(
                            """
                            INSERT INTO documents (id, page_content, metadata, parent_id)
                            VALUES (:id, :page_content, :metadata, :parent_id)
                            ON CONFLICT (id) DO NOTHING
                        """
                        ),
                        {
                            "id": child_doc.id,
                            "page_content": child_doc.page_content,
                            "metadata": json.dumps(child_doc.metadata),
                            "parent_id": child_doc.parent_id,
                        },
                    )

        # Prepare all child document contents for embedding
        documents_to_embed = [(doc.id, doc.page_content) for doc in child_docs]

        # Generate embeddings in batches
        embeddings = self.embedding_model.embed(
            [doc_content for _, doc_content in documents_to_embed],
            show_progress_bar=True,
        )
        print("Adding documents to db...")
        t0 = time.time()
        # Insert embeddings into the database
        with self.engine.connect() as conn:
            with conn.begin():
                conn.execute(
                    text(
                        """
                        INSERT INTO embeddings (id, document_id, embedding)
                        VALUES (:id, :doc_id, :embedding)
                        ON CONFLICT (id) DO UPDATE
                        SET embedding = EXCLUDED.embedding
                    """
                    ),
                    [
                        {"id": doc_id, "doc_id": doc_id, "embedding": embedding}
                        for (doc_id, _), embedding in zip(
                            documents_to_embed, embeddings
                        )
                    ],
                )
        print(f"Total time adding embeddings to db: {time.time() - t0:.4f}s")

        self.optimize_index_for_size()

        self.update_text_search_vector()

    def delete(self, document_ids: List[str] = None, document_name: str = None) -> None:
        """
        Delete items from the DB. Either by thier ID or by their name (not
        both at the same time)

        **NOTE** can currently only delete one document by name at a time, no options to delete before a certain date etc. There are all WIPs!

        :param document_ids: (List[str]) - list of document ids to delete
        :param document_name: (str) - Document name to delete
        """
        if document_ids is None and document_name is None:
            raise ValueError(
                "You must provide either document_ids or document_name to delete."
            )

        with self.engine.connect() as conn:
            with conn.begin():
                if document_name:
                    # Find all parent and child document IDs with the specified name in metadata
                    document_ids = (
                        conn.execute(
                            text(
                                """
                            SELECT id FROM documents
                            WHERE metadata::jsonb->>'name' = :doc_name
                        """
                            ),
                            {"doc_name": document_name},
                        )
                        .scalars()
                        .all()
                    )

                if not document_ids:
                    print(f"No documents found for the given criteria.")
                    return

                # Delete embeddings and documents
                conn.execute(
                    text(
                        """
                        DELETE FROM documents WHERE id = ANY(:doc_ids) OR parent_id = ANY(:doc_ids);
                    """
                    ),
                    {"doc_ids": document_ids},
                )
                print(f"Deleted {len(document_ids)} documents and their embeddings.")

    def _set_postgres_memory_settings(
        self, desired_mem="3GB", desired_workers=8, fallback_mem="1GB"
    ):
        with self.engine.connect() as conn:
            try:
                with conn.begin():
                    # First attempt with desired settings
                    conn.execute(
                        text(
                            f"""
                            SET maintenance_work_mem = :mem;
                            SET max_parallel_workers_per_gather = :workers;
                            """
                        ),
                        {"mem": desired_mem, "workers": desired_workers},
                    )
            except DataError as e:
                print(f"Cannot set worker mem to 3GB - defaulting back to 1GB!")
                with conn.begin():
                    conn.execute(
                        text(
                            f"""
                            SET maintenance_work_mem = :mem;
                            SET max_parallel_workers_per_gather = :workers;
                            """
                        ),
                        {"mem": fallback_mem, "workers": desired_workers},
                    )

            with conn.begin():
                # Verify final settings
                final_settings = conn.execute(
                    text(
                        """
                        SELECT name, setting
                        FROM pg_settings
                        WHERE name IN ('maintenance_work_mem', 'max_parallel_workers_per_gather');
                        """
                    )
                ).fetchall()

        return dict(final_settings)

    def update_index_lists(self, new_lists: int = 1200, new_probes: int = 50):
        """Update the IVFFlat index with a new number of lists. This will drop
        the old index and create a new one.

        :param new_lists: (int) - number of lists to use in new indexing
        :param new_probes: (int) - number of probes to use when searching embeddings
        """
        with self.engine.connect() as conn:
            with conn.begin():
                # parallel processing
                params = self._set_postgres_memory_settings()
                print(params)
                # THIS NEVER GETS RESET! an issue maybe?

                # Drop the old index
                conn.execute(
                    text(
                        """
                    DROP INDEX IF EXISTS embeddings_vector_idx;
                """
                    )
                )

                # Create new index with updated lists parameter
                conn.execute(
                    text(
                        f"""
                    CREATE INDEX embeddings_vector_idx
                    ON embeddings
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = {new_lists});
                """
                    )
                )

                conn.execute(text(f"""SET ivfflat.probes = {new_probes};"""))

    def optimize_index_for_size(self):
        """Calculate and set optimal number of lists based on embedding count.

        **NOTE**: Optimal is taken very loosely here!
        """
        with self.engine.connect() as conn:
            # Get count of embeddings
            count = conn.execute(text("SELECT COUNT(*) FROM embeddings")).scalar()

            # Calculate optimal lists (roughly sqrt of count - with an extra bit added for RAG)
            optimal_lists = int(math.sqrt(count) + 0.05 * math.sqrt(count))

            optimal_probes = max(
                4, int(optimal_lists * 0.14)
            )  # optimal bins roughly 10% of number of lists

            # For very large datasets, cap at a reasonable maximum
            optimal_lists = min(max(optimal_lists, 4), 2000)

        print(
            f"Updating index for {count} embeddings with {optimal_lists} lists and {optimal_probes} probes"
        )
        self.update_index_lists(optimal_lists, optimal_probes)

    def drop_database(self) -> None:
        """
        WARNING: USE WITH CARE - WILL DELETE EVERYTHING
        **CURRENTLY BROKEN**
        (in this db name e.g. vectordb hopefully not the entirety of the server)
        Drop the entire database and its contents. Useful for testing with a new embedding model or splitter.
        """
        db_info = self._extract_db_info()
        base_connection = db_info["base_connection"]
        database_name = db_info["database_name"]

        # Connect to the default 'postgres' database
        default_connection = f"{base_connection}/postgres"
        temp_engine = create_engine(default_connection)

        try:
            with temp_engine.connect() as conn:
                # Terminate all connections to the database
                with conn.begin():
                    conn.execute(
                        text(
                            f"""
                            SELECT pg_terminate_backend(pid)
                            FROM pg_stat_activity
                            WHERE datname = :dbname;
                        """
                        ),
                        {"dbname": database_name},
                    )

                    # Drop the database
                    conn.execute(text(f'DROP DATABASE IF EXISTS "{database_name}"'))

            print(f"Database '{database_name}' has been successfully dropped.")

        except Exception as e:
            raise Exception(f"Failed to drop database: {str(e)}")

        finally:
            temp_engine.dispose()

    def clear_database(self) -> None:
        """
        WARNING: USE WITH CARE - WILL CLEAR ALL TABLE CONTENTS
        Empties all tables in the database while preserving the database structure.
        """
        try:
            with self.engine.connect() as conn:
                inspector = inspect(self.engine)
                tables = inspector.get_table_names()

                with conn.begin():
                    for table in tables:
                        conn.execute(
                            text(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE')
                        )

                print("All tables have been cleared successfully.")
        except Exception as e:
            raise Exception(f"Failed to clear the database: {str(e)}")

    def update_text_search_vector(self) -> int:
        """
        Updates all text search vectors in the documents table using the current scientific dictionary configuration.
        This is useful after modifying the dictionary settings or stop words.

        :return: Number of rows updated
        :rtype: int
        """
        with self.engine.connect() as conn:
            with conn.begin():
                result = conn.execute(
                    text(
                        f"""
                        UPDATE documents
                        SET text_search_vector =
                            CASE
                                WHEN parent_id IS NULL THEN
                                    setweight(to_tsvector('{self.dictionary_type}',
                                        clean_text_for_vector(COALESCE(page_content, ''))), 'A') ||
                                    setweight(to_tsvector('{self.dictionary_type}',
                                        clean_text_for_vector(COALESCE(metadata->>'topic_parent', ''))), 'C') ||
                                    setweight(to_tsvector('{self.dictionary_type}',
                                        clean_text_for_vector(COALESCE(metadata->>'name', ''))), 'B')
                                ELSE NULL
                            END
                        WHERE parent_id IS NULL;  -- Only update root documents
                        """
                    )
                )
                return int(result.rowcount)

    def test_connection(self):
        """Test the connection to the PostgreSQL database.

        Returns:
            True if connection succeeded
            False if connection failed
        """
        try:
            with create_engine(self.connection_string).connect() as conn:
                # Execute a simple query to check the connection
                result = conn.execute(text("SELECT 1")).scalar()
                if result == 1:
                    return True  # Connection is good
                return False  # Connection failed unexpectedly
        except Exception as e:
            # Log the error or raise it if necessary
            print(f"Connection test failed: {str(e)}")
            return False

    ###############################################################
    # NOTES ON DECISIONS TAKEN WITH THIS SEARCH FUNCTION
    # I (Ben Elliot) am not a SQL engineer so much of this search function may be inefficient, wrong, subject to
    # SQL injection or just generally poorly implemented. This is just the best way I could get it to function, but
    # feel free to modify or alter to a better solution.

    @deprecated("0.11.1 - Deprecated due to slower search times")
    def search_together(
        self,
        query: str,
        k: int = 4,
        k_text: int = 0,
        metadata_filters: dict = None,
        date_filter: str = None,
    ) -> List[Tuple[Document, Document, float]]:
        """
        A hybrid retrieval function that performs both semantic search using vector embeddings and
        lexical search using PostgreSQL's full-text search capabilities.

        Performs the query for text and embeddings in one single query, which is much slower!

        The (similarity) score can be found in the third item of every tuple in the list.
        How the document was returned can be found in parent_doc.metadata["search_type"] = "vector" or "text"

        :param query: Query text to search for
        :type query: str
        :param k: Maximum number of results to return from vector-based semantic search
        :type k: int
        :param k_text: Maximum number of results to return from text-based lexical search
        :type k_text: int
        :param metadata_filters: Filters to apply on document metadata. Keys are metadata fields,
                                values can be strings (exact match) or lists (any match)
        :type metadata_filters: dict[str, str | list]
        :param date_filter: Date string in 'dd-mm-YYYY' format. Only returns documents modified
                           after this date (e.g. "01-03-2001")
        :type date_filter: str

        :returns: List of tuples containing (child_doc, parent_doc, similarity_score)
        :rtype: List[Tuple[Document, Document, float]]

        The function implements a hybrid retrieval approach combining:

        1. Semantic Search:
           - Uses cosine similarity between query and document embeddings
           - Returns documents most similar in meaning/context
           - Scores range from 0 to 1, where 1 indicates highest similarity

        2. Lexical Search:
           - Uses PostgreSQL's tsvector/tsquery for text matching
           - Implements weighted document ranking:
              * Document names (weight A - highest)
              * Document topics and content (weight B - medium)
           - Normalizes scores to 0-1 range

        Result Processing:
        - Both searches initially fetch k+10 results to account for:
          * Filtered results that don't meet metadata criteria
          * Duplicate removals when combining vector and text results
        - Final results are deduplicated and limited to k + k_text total documents
        - Each result includes a search_type in parent_doc.metadata indicating
          whether it was found via "vector" or "text" search

        Text Search Implementation:
        - Uses ts_rank_cd for ranking, considering term proximity and density
        - Query processing via plainto_tsquery:
          * Converts text to lowercase
          * Removes punctuation and stop words
          * Performs word stemming
          * Combines terms with AND operators
        - Scoring considers:
          * Number of matching terms
          * Term proximity
          * Term frequency
          * Document structure weights

        Note:
        The similarity scores from embedding and text searches are not directly comparable
        as they use different scoring mechanisms, though both are normalized to the
        0-1 range.
        Also note that parent documents are deduplicated with higher priority for text search, so will always return
         text searches first before the vector search if they are the same.
        Metadata filters are applied to both the child documents as well as the parent documents

        """
        # Input validation
        if not query or not query.strip():
            print("Empty query returning no results")
            return []
        # Checking k values are ints
        try:
            k = int(k)
            k_text = int(k_text)
        except ValueError as e:
            print(f"Please give k values as ether ints or int parse-able strings")
            raise

        # Making sure we don't have k in metadata filters - use metadata filter versions instead of kwargs if we have
        if metadata_filters:
            k = metadata_filters.pop("k", k)
            k_text = metadata_filters.pop("k_text", k_text)

        # Generate embedding for the query
        query_embedding = self.embedding_model.embed(query)

        # Build metadata filter conditions using bind parameters for safety
        metadata_filter_conditions = []
        filter_params = {}

        # Process the Query
        def clean_query_for_tsquery(query: str) -> str:
            """Clean and format query string for PostgreSQL tsquery."""
            # Remove special characters but preserve compound terms
            cleaned = re.sub(r"([^a-zA-Z0-9/\s])", " ", query)

            # current_term = []
            #
            # for word in cleaned.split():
            #     # Keep compound/technical terms together
            #     if word.isupper() or any(c.isupper() for c in word):
            #         current_term.append(word)
            #     else:
            #         if current_term:
            #             words.append("_".join(current_term))
            #             current_term = []
            #         words.append(word)
            #
            # if current_term:
            #     words.append("_".join(current_term))

            # Remove the stop words
            cleaned = re.sub(
                r"\b(" + "|".join(map(re.escape, self.stop_words)) + r")\b",
                " ",
                cleaned,
                flags=re.IGNORECASE,
            )
            words = [word for word in cleaned.split() if word.strip()]

            # Group terms logically with & between significant terms
            terms = []
            for i in range(0, len(words), 3):
                group = words[i : i + 8]
                if group:
                    # Join each group with & and add :* for prefix matching
                    group_terms = [f"'{w}:*'" for w in group]
                    terms.append("(" + " | ".join(group_terms) + ")")

            # Join groups with | for some flexibility between concept groups
            return " & ".join(terms) if terms else "dummy_term_that_wont_match"

        processed_query = clean_query_for_tsquery(query)

        if not processed_query:
            processed_query = (
                "dummy_term_that_wont_match"  # Fallback for empty processed query
            )

        if metadata_filters:
            for idx, (key, value) in enumerate(metadata_filters.items()):
                param_key = f"key_{idx}"
                param_value = f"value_{idx}"

                # Handle different types of metadata values
                if isinstance(value, list):
                    # For list values, check if the metadata field contains ANY of the filter values
                    metadata_filter_conditions.append(
                        f"CAST(d_child.metadata::jsonb->:key_{idx} AS jsonb) ?| :value_{idx}"
                    )
                else:
                    # For string values, use exact match
                    metadata_filter_conditions.append(
                        f"d_child.metadata->>:key_{idx} = :value_{idx}"
                    )

                filter_params[param_key] = key
                filter_params[param_value] = (
                    value if isinstance(value, list) else str(value)
                )

        # Add date filter condition
        if date_filter:
            metadata_filter_conditions.append(
                "TO_DATE(d_child.metadata->>'last_modification', 'DD-MM-YYYY') > TO_DATE(:date_filter, 'DD-MM-YYYY')"
            )
            filter_params["date_filter"] = date_filter

        # Combine all filter conditions
        metadata_filter_clause = " AND ".join(metadata_filter_conditions)
        where_clause = (
            f"WHERE {metadata_filter_clause}" if metadata_filter_conditions else ""
        )

        # Final SQL query with metadata filtering
        query_text = f"""
        WITH vector_results AS (
            -- First get the vector similarity results from child documents
            SELECT
                e.document_id,
                d_child.parent_id,
                1 - (e.embedding <=> CAST(:query_embedding AS vector)) AS score,
                'vector' as search_type
            FROM embeddings e
            JOIN documents d_child ON e.document_id = d_child.id
            {where_clause}
            ORDER BY e.embedding <=> CAST(:query_embedding AS vector)
            LIMIT :k_vector
        ),
        -- Get the best score per parent for vector results
        best_vector_results AS (
            SELECT DISTINCT ON (parent_id)
                document_id,
                parent_id,
                score,
                search_type
            FROM vector_results
            ORDER BY parent_id, score DESC
        ),
        text_results AS (
            -- Get text search results directly from parent documents
            SELECT
                d_parent.id as parent_id,
                ts_rank_cd(d_parent.text_search_vector,
                          to_tsquery('{self.dictionary_type}', :text_query), 32) as raw_score,
                'text' as search_type
            FROM documents d_parent
            WHERE d_parent.text_search_vector IS NOT NULL
            {f"AND {metadata_filter_clause.replace('d_child' ,'d_parent')}" if metadata_filter_conditions else ""}
        ),
        normalized_text_results AS (
            -- Normalize text search scores
            SELECT
                parent_id,
                CASE
                    WHEN MAX(raw_score) OVER () > 0
                    THEN raw_score / MAX(raw_score) OVER ()
                    ELSE 0
                END as score,
                search_type
            FROM text_results
            WHERE raw_score > 0
            ORDER BY raw_score DESC
            LIMIT :k_text
        ),
        -- Combine the best vector results and text results
        combined_results AS (
            SELECT parent_id, score, search_type
            FROM (
                SELECT parent_id, score, search_type
                FROM best_vector_results
                UNION ALL
                SELECT parent_id, score, search_type
                FROM normalized_text_results
            ) all_results
        ),
        -- Get the best score per parent across both search types
        best_scores AS (
            SELECT DISTINCT ON (parent_id)
                parent_id,
                score,
                search_type
            FROM combined_results
            ORDER BY parent_id, score DESC
        )
        -- Final result with one child document per parent
        SELECT
            d_child.id AS child_id,
            d_child.page_content AS child_content,
            d_child.metadata AS child_metadata,
            d_child.parent_id,
            d_parent.id AS parent_id,
            d_parent.page_content AS parent_content,
            d_parent.metadata AS parent_metadata,
            bs.score,
            bs.search_type
        FROM best_scores bs
        JOIN documents d_parent ON bs.parent_id = d_parent.id
        -- Get a sample child document for each parent
        LEFT JOIN LATERAL (
            SELECT id, page_content, metadata, parent_id
            FROM documents
            WHERE parent_id = d_parent.id
            LIMIT 1
        ) d_child ON true
        ORDER BY bs.score DESC;
            """

        try:
            with self.engine.connect() as conn:
                # Execute the query with parameters
                results = conn.execute(
                    text(query_text).bindparams(
                        query_embedding=bindparam("query_embedding"),
                        k_vector=bindparam("k_vector"),
                        k_text=bindparam("k_text"),
                        text_query=bindparam("text_query"),
                        **{key: bindparam(key) for key in filter_params.keys()},
                    ),
                    {
                        "query_embedding": query_embedding,
                        "k_vector": (
                            (k + 10) if filter_params and k > 0 else k
                        ),  # Return extra docs if there are filters
                        "k_text": (
                            (k_text + 10) if filter_params and k_text > 0 else k_text
                        ),  # Same for text results
                        "text_query": processed_query,
                        **filter_params,
                    },
                )

                # Process results and construct Document objects
                search_results = []
                counts = {"vector": 0, "text": 0}
                limits = {"vector": k, "text": k_text}

                for row in results:
                    # Skip if we have enough results of this type
                    if counts[row.search_type] >= limits[row.search_type]:
                        continue

                    # Create child document
                    child_doc = Document(
                        id=row.child_id,
                        page_content=row.child_content,
                        metadata=row.child_metadata if row.child_metadata else {},
                        parent_id=row.parent_id,
                    )

                    # Create parent document with search type metadata
                    parent_metadata = (
                        row.parent_metadata.copy() if row.parent_metadata else {}
                    )
                    parent_metadata["search_type"] = row.search_type

                    parent_doc = Document(
                        id=row.parent_id,
                        page_content=row.parent_content,
                        metadata=parent_metadata,
                        parent_id=None,
                    )

                    search_results.append((child_doc, parent_doc, float(row.score)))
                    counts[row.search_type] += 1

                    # Break if we have enough results of both types
                    if all(counts[t] >= limits[t] for t in counts):
                        break

                return search_results

        except Exception as e:
            print(f"Error in search: {e}")
            raise

    def search(
        self,
        query: str,
        k: int = 4,
        k_text: int = 0,
        metadata_filters: dict = None,
        date_filter: str = None,
        with_timings: bool = False,
    ) -> List[Tuple[Document, Document, float]]:
        """
        A hybrid retrieval function that performs both semantic search using vector embeddings and
        lexical search using PostgreSQL's full-text search capabilities, but executed separately.

        The (similarity) score can be found in the third item of every tuple in the list.
        How the document was returned can be found in parent_doc.metadata["search_type"] = "vector" or "text"

        :param query: Query text to search for
        :type query: str
        :param k: Maximum number of results to return from vector-based semantic search
        :type k: int
        :param k_text: Maximum number of results to return from text-based lexical search
        :type k_text: int
        :param metadata_filters: Filters to apply on document metadata. Keys are metadata fields,
                                values can be strings (exact match) or lists (any match)
        :type metadata_filters: dict[str, str | list]
        :param date_filter: Date string in 'dd-mm-YYYY' format. Only returns documents modified
                           after this date (e.g. "01-03-2001")
        :type date_filter: str

        :returns: List of tuples containing (child_doc, parent_doc, similarity_score)
        :rtype: List[Tuple[Document, Document, float]]

        The function implements a hybrid retrieval approach combining:

        1. Semantic Search:
           - Uses cosine similarity between query and document embeddings
           - Returns documents most similar in meaning/context
           - Scores range from 0 to 1, where 1 indicates highest similarity

        2. Lexical Search:
           - Uses PostgreSQL's tsvector/tsquery for text matching
           - Implements weighted document ranking:
              * Document names (weight A - highest)
              * Document topics and content (weight B - medium)
           - Normalizes scores to 0-1 range

        Result Processing:
        - Both searches initially fetch k+10 results to account for:
          * Filtered results that don't meet metadata criteria
          * Duplicate removals when combining vector and text results
        - Final results are deduplicated and limited to k + k_text total documents
        - Each result includes a search_type in parent_doc.metadata indicating
          whether it was found via "vector" or "text" search

        Text Search Implementation:
        - Uses ts_rank_cd for ranking, considering term proximity and density
        - Query processing via plainto_tsquery:
          * Converts text to lowercase
          * Removes punctuation and stop words
          * Performs word stemming
          * Combines terms with AND operators
        - Scoring considers:
          * Number of matching terms
          * Term proximity
          * Term frequency
          * Document structure weights

        Note:
        The similarity scores from embedding and text searches are not directly comparable
        as they use different scoring mechanisms, though both are normalized to the
        0-1 range.
        Also note that parent documents are deduplicated with higher priority for text search, so will always return
         text searches first before the vector search if they are the same.
        Metadata filters are applied to both the child documents as well as the parent documents


        RETURNS EMPTY CHILD DOCUMENTS FOR TEXT SEARCH!
        """
        if with_timings:
            pre_processing_t0 = time.perf_counter()

        # Input validation
        if not query or not query.strip():
            print("Empty query returning no results")
            return []

        # Checking k values are ints
        try:
            k = int(k)
            k_text = int(k_text)
        except ValueError as e:
            print(f"Please give k values as ether ints or int parse-able strings")
            raise

        # Making sure we don't have k in metadata filters
        if metadata_filters:
            metadata_filters = (
                metadata_filters.copy()
            )  # Create a copy to avoid modifying original
            k = metadata_filters.pop("k", k)
            k_text = metadata_filters.pop("k_text", k_text)

        # Build metadata filter conditions
        metadata_filter_conditions = []
        filter_params = {}

        if metadata_filters:
            for idx, (key, value) in enumerate(metadata_filters.items()):
                param_key = f"key_{idx}"
                param_value = f"value_{idx}"

                if isinstance(value, list):
                    metadata_filter_conditions.append(
                        f"CAST(d_child.metadata::jsonb->:key_{idx} AS jsonb) ?| :value_{idx}"
                    )
                else:
                    metadata_filter_conditions.append(
                        f"d_child.metadata->>:key_{idx} = :value_{idx}"
                    )

                filter_params[param_key] = key
                filter_params[param_value] = (
                    value if isinstance(value, list) else str(value)
                )

        # Add date filter condition
        if date_filter:
            metadata_filter_conditions.append(
                "TO_DATE(d_child.metadata->>'last_modification', 'DD-MM-YYYY') > TO_DATE(:date_filter, 'DD-MM-YYYY')"
            )
            filter_params["date_filter"] = date_filter

        # Combine filter conditions
        metadata_filter_clause = " AND ".join(metadata_filter_conditions)
        where_clause = (
            f"WHERE {metadata_filter_clause}" if metadata_filter_conditions else ""
        )

        vector_results = []
        text_results = []

        if with_timings:
            pre_processing_t1 = time.perf_counter()
            print(
                f"TIME TAKEN FOR PREPROCESSING: {pre_processing_t1 - pre_processing_t0}"
            )

        if k > 0:
            # 1. Perform Vector Search
            if with_timings:
                vector_t0 = time.perf_counter()
            vector_results = self._vector_search(query, k, where_clause, filter_params)
            if with_timings:
                vector_t1 = time.perf_counter()
                print(f"TIME TAKEN FOR VECTOR SEARCH: {vector_t1 - vector_t0}")

        if k_text > 0:
            # 2. Perform Text Search
            if with_timings:
                text_t0 = time.perf_counter()
            text_results = self._text_search(
                query, k_text, filter_params, metadata_filter_clause
            )
            if with_timings:
                text_t1 = time.perf_counter()
                print(f"TIME TAKEN FOR TEXT SEARCH: {text_t1 - text_t0}")

        # No results at all
        if not vector_results and not text_results:
            return []

        # 3. Combine and deduplicate results
        # Create a dictionary to track the best score for each parent_id
        combined_results = {}

        # Process vector results first (higher priority for duplicates
        for result in vector_results:
            parent_id = result[1].id  # parent_doc.id
            combined_results[parent_id] = result

        # Process text results
        for result in text_results:
            parent_id = result[1].id  # parent_doc.id
            if parent_id not in combined_results:
                combined_results[parent_id] = result

        # Convert back to list and sort by score
        final_results = sorted(
            combined_results.values(), key=lambda x: x[2], reverse=True
        )

        return final_results

    def _vector_search(
        self,
        query,
        k: int,
        where_clause: str,
        filter_params: dict,
    ) -> List[Tuple[Document, Document, float]]:
        """Execute vector-based semantic search."""

        # Generate embedding for vector search
        query_embedding = self.embedding_model.embed(query)

        vector_query = f"""
        WITH vector_results AS (
            SELECT
                e.document_id,
                d_child.parent_id,
                1 - (e.embedding <=> CAST(:query_embedding AS vector)) AS score
            FROM embeddings e
            JOIN documents d_child ON e.document_id = d_child.id
            {where_clause}
            ORDER BY e.embedding <=> CAST(:query_embedding AS vector)
            LIMIT :k_vector
        ),
        best_vector_results AS (
            SELECT DISTINCT ON (parent_id)
                document_id,
                parent_id,
                score
            FROM vector_results
            ORDER BY parent_id, score DESC
        )
        SELECT
            d_child.id AS child_id,
            d_child.page_content AS child_content,
            d_child.metadata AS child_metadata,
            d_child.parent_id,
            d_parent.id AS parent_id,
            d_parent.page_content AS parent_content,
            d_parent.metadata AS parent_metadata,
            bvr.score
        FROM best_vector_results bvr
        JOIN documents d_parent ON bvr.parent_id = d_parent.id
        JOIN documents d_child ON bvr.document_id = d_child.id
        ORDER BY bvr.score DESC;
        """

        with self.engine.connect() as conn:
            conn.execute(text("SET plan_cache_mode = force_generic_plan"))
            results = conn.execute(
                text(vector_query),
                {
                    "query_embedding": query_embedding,
                    "k_vector": k + 10 if filter_params else k,
                    **filter_params,
                },
            )

            vector_results = []
            for i, row in enumerate(results):
                if i >= k:
                    break
                child_doc = Document(
                    id=row.child_id,
                    page_content=row.child_content,
                    metadata=row.child_metadata if row.child_metadata else {},
                    parent_id=row.parent_id,
                )

                parent_metadata = (
                    row.parent_metadata.copy() if row.parent_metadata else {}
                )
                parent_metadata["search_type"] = "vector"

                parent_doc = Document(
                    id=row.parent_id,
                    page_content=row.parent_content,
                    metadata=parent_metadata,
                    parent_id=None,
                )

                vector_results.append((child_doc, parent_doc, float(row.score)))

            return vector_results

    def _text_search(
        self,
        query: str,
        k_text: int,
        filter_params: dict,
        metadata_filter_clause: str,
    ) -> List[Tuple[Document, Document, float]]:
        """
        Execute text-based lexical search.

        Note returns empty child documents!
        """

        # Process query for text search
        processed_query = self._clean_query_for_tsquery(query)
        if not processed_query:
            processed_query = "dummy_term_that_wont_match"
        text_query = f"""
        WITH ranked_results AS (
            SELECT
                id AS parent_id,
                ts_rank_cd(
                    text_search_vector,
                    to_tsquery('{self.dictionary_type}', :text_query),
                    32
                ) AS raw_score
            FROM documents
            WHERE text_search_vector @@ to_tsquery('{self.dictionary_type}', :text_query)
            ORDER BY raw_score DESC
            LIMIT :k_text  -- Reduce number of rows early
        ),
        normalized_results AS (
            SELECT
                parent_id,
                raw_score / (SELECT MAX(raw_score) FROM ranked_results) AS score
            FROM ranked_results
        )
        SELECT
            d_parent.id AS parent_id,
            d_parent.page_content AS parent_content,
            d_parent.metadata AS parent_metadata,
            nr.score
        FROM normalized_results nr
        JOIN documents d_parent ON nr.parent_id = d_parent.id
         {f"WHERE {metadata_filter_clause.replace('d_child', 'd_parent')}" if metadata_filter_clause else ""}
        ORDER BY nr.score DESC;
        """

        with self.engine.connect() as conn:
            conn.execute(
                text("""SET enable_seqscan = OFF;""")
            )  # This really doesn't need to be run every time!
            results = conn.execute(
                text(text_query),
                {
                    "text_query": processed_query,
                    "k_text": k_text + 10 if filter_params else k_text,
                    **filter_params,
                },
            )

            text_results = []
            for i, row in enumerate(results):
                # make sure we only take top k_text docs
                if i >= k_text:
                    break

                child_doc = Document(
                    id="0",
                    page_content="RESULT FROM TEXT SEARCH - NO CHILD DOCUMENTS",
                    metadata={},
                    parent_id=row.parent_id,
                )

                parent_metadata = (
                    row.parent_metadata.copy() if row.parent_metadata else {}
                )
                parent_metadata["search_type"] = "text"

                parent_doc = Document(
                    id=row.parent_id,
                    page_content=row.parent_content,
                    metadata=parent_metadata,
                    parent_id=None,
                )

                text_results.append((child_doc, parent_doc, float(row.score)))

            return text_results

    def _clean_query_for_tsquery(self, query: str) -> str:
        """Clean and format query string for PostgreSQL tsquery.

        Uses precompiled regex patterns, set lookups for stop words, and optimized word grouping.
        """
        # Class-level precompiled patterns for reuse (defined in __init__)
        if not hasattr(self, "_special_char_pattern"):
            self._special_char_pattern = re.compile(r"[^a-zA-Z0-9/\s]")
            self._stop_word_pattern = re.compile(
                r"\b(" + "|".join(map(re.escape, self.stop_words)) + r")\b",
                flags=re.IGNORECASE,
            )
            self._stop_words_set = set(word.lower() for word in self.stop_words)

        # Remove special characters
        cleaned = self._special_char_pattern.sub(" ", query)

        # Split and filter words in one pass
        words = [
            word
            for word in cleaned.lower().split()
            if word and word not in self._stop_words_set
        ]

        if not words:
            return "dummy_term_that_wont_match"

        # Create word groups more efficiently
        GROUP_SIZE = 8
        terms = []
        for i in range(0, len(words), GROUP_SIZE):
            group = words[i : i + GROUP_SIZE]
            if group:
                term = "(" + " | ".join(f"'{w}:*'" for w in group) + ")"
                terms.append(term)

        return " & ".join(terms)
