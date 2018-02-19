"""Add refresh_token to users table and extend length of allowable token values

Revision ID: d1fc9767c571
Revises: eb5c65c60f08
Create Date: 2018-02-18 18:17:38.332371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1fc9767c571'
down_revision = 'eb5c65c60f08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('refresh_token', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'refresh_token')
    # ### end Alembic commands ###