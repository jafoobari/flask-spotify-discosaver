"""playlists and songs tables

Revision ID: 4edd824d3117
Revises: b79d98bc08b4
Create Date: 2019-07-01 22:19:32.299139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4edd824d3117'
down_revision = 'b79d98bc08b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('playlist_id', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_playlist_created_at'), 'playlist', ['created_at'], unique=False)
    op.create_index(op.f('ix_playlist_name'), 'playlist', ['name'], unique=False)
    op.create_index(op.f('ix_playlist_playlist_id'), 'playlist', ['playlist_id'], unique=True)
    op.create_table('song',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('track_id', sa.String(length=64), nullable=True),
    sa.Column('playlist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_song_created_at'), 'song', ['created_at'], unique=False)
    op.create_index(op.f('ix_song_track_id'), 'song', ['track_id'], unique=False)
    op.add_column('user', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_created_at'), 'user', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_created_at'), table_name='user')
    op.drop_column('user', 'created_at')
    op.drop_index(op.f('ix_song_track_id'), table_name='song')
    op.drop_index(op.f('ix_song_created_at'), table_name='song')
    op.drop_table('song')
    op.drop_index(op.f('ix_playlist_playlist_id'), table_name='playlist')
    op.drop_index(op.f('ix_playlist_name'), table_name='playlist')
    op.drop_index(op.f('ix_playlist_created_at'), table_name='playlist')
    op.drop_table('playlist')
    # ### end Alembic commands ###
