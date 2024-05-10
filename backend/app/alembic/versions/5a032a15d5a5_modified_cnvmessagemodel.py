"""Modified CnvMessageModel

Revision ID: 5a032a15d5a5
Revises: cc6656d4c653
Create Date: 2024-05-10 18:35:35.785116

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '5a032a15d5a5'
down_revision = 'cc6656d4c653'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('conversation', 'modified_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conversation', sa.Column('modified_at', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
