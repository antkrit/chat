"""add author msg table

Revision ID: 37c7135b2e47
Revises: a1be75bd0666
Create Date: 2021-10-21 21:26:23.001752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37c7135b2e47'
down_revision = 'a1be75bd0666'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('author', sa.String(length=200), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'author')
    # ### end Alembic commands ###