"""Add Collection model

Revision ID: 63a1371473a7
Revises: d22447872d66
Create Date: 2025-06-16 00:23:52.657723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63a1371473a7'
down_revision: Union[str, None] = 'd22447872d66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'owner_id', name='uc_collection_owner')
    )
    op.create_index(op.f('ix_collections_id'), 'collections', ['id'], unique=False)
    op.create_table('collection_documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('collection_id', sa.Integer(), nullable=True),
    sa.Column('document_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.id'], ),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('collection_id', 'document_id', name='uc_collection_document')
    )
    op.create_index(op.f('ix_collection_documents_id'), 'collection_documents', ['id'], unique=False)
    op.add_column('documents', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.drop_constraint(op.f('documents_filename_key'), 'documents', type_='unique')
    op.create_unique_constraint('uc_filename_owner', 'documents', ['filename', 'owner_id'])
    op.create_foreign_key(None, 'documents', 'users', ['owner_id'], ['id'])
    op.drop_index(op.f('ix_words_text'), table_name='words')
    op.create_index(op.f('ix_words_text'), 'words', ['text'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_words_text'), table_name='words')
    op.create_index(op.f('ix_words_text'), 'words', ['text'], unique=False)
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.drop_constraint('uc_filename_owner', 'documents', type_='unique')
    op.create_unique_constraint(op.f('documents_filename_key'), 'documents', ['filename'], postgresql_nulls_not_distinct=False)
    op.drop_column('documents', 'owner_id')
    op.drop_index(op.f('ix_collection_documents_id'), table_name='collection_documents')
    op.drop_table('collection_documents')
    op.drop_index(op.f('ix_collections_id'), table_name='collections')
    op.drop_table('collections')
    # ### end Alembic commands ###
