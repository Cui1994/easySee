"""empty message

Revision ID: 115b3ec15167
Revises: 
Create Date: 2017-01-12 16:02:15.510250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '115b3ec15167'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_remind', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_remind')
    # ### end Alembic commands ###
