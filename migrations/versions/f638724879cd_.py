"""empty message

Revision ID: f638724879cd
Revises: e163567be09f
Create Date: 2017-01-13 15:20:33.471895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f638724879cd'
down_revision = 'e163567be09f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('user_name', sa.String(length=64), nullable=True),
    sa.Column('user_email', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_user_email'), 'messages', ['user_email'], unique=False)
    op.create_index(op.f('ix_messages_user_name'), 'messages', ['user_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_messages_user_name'), table_name='messages')
    op.drop_index(op.f('ix_messages_user_email'), table_name='messages')
    op.drop_table('messages')
    # ### end Alembic commands ###