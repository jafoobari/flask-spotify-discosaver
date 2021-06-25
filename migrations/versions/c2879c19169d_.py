"""empty message

Revision ID: c2879c19169d
Revises: b79d98bc08b4
Create Date: 2021-06-24 22:12:08.228574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2879c19169d'
down_revision = 'b79d98bc08b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('dw_playlist_id', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'dw_playlist_id')
    # ### end Alembic commands ###
