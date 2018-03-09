"""Add rest of token info as columns to users table.

Revision ID: 39869f041a68
Revises: 
Create Date: 2018-03-08 21:31:25.577218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39869f041a68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('access_token', sa.String(length=256), nullable=True),
    sa.Column('refresh_token', sa.String(length=256), nullable=True),
    sa.Column('token_expires_at', sa.Integer(), nullable=True),
    sa.Column('token_expires_in', sa.Integer(), nullable=True),
    sa.Column('token_scope', sa.String(length=256), nullable=True),
    sa.Column('token_type', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###