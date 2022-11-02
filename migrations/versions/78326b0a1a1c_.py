"""empty message

Revision ID: 78326b0a1a1c
Revises: 7b341695f43f
Create Date: 2022-10-28 02:19:55.784949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78326b0a1a1c'
down_revision = '7b341695f43f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('full_name', sa.String(length=250), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'full_name')
    # ### end Alembic commands ###