"""added updated at field

Revision ID: cc6656d4c653
Revises: 2bcdf4d781c2
Create Date: 2024-05-10 18:17:50.960249

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'cc6656d4c653'
down_revision = '2bcdf4d781c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conversation', sa.Column('modified_at', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('conversation', 'modified_at')
    # ### end Alembic commands ###