"""empty message

Revision ID: dc9ba8e7a29a
Revises: 49a5d0040b0e
Create Date: 2017-01-12 18:57:38.807847

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dc9ba8e7a29a'
down_revision = '49a5d0040b0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('anchors', 'users_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('anchors', sa.Column('users_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    # ### end Alembic commands ###