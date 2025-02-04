"""Create blood_pressure table

Revision ID: 350e7dcb1f98
Revises: b343cd167b1b
Create Date: 2024-05-28 03:01:42.300800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '350e7dcb1f98'
down_revision = 'b343cd167b1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blood_pressure',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('systolic', sa.Integer(), nullable=False),
    sa.Column('diastolic', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blood_pressure')
    # ### end Alembic commands ###
