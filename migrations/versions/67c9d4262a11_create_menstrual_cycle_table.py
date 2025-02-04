"""Create menstrual_cycle table

Revision ID: 67c9d4262a11
Revises: 64246bc8f71b
Create Date: 2024-06-01 20:28:04.842419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67c9d4262a11'
down_revision = '64246bc8f71b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menstrual_cycle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('cycle_length', sa.Integer(), nullable=False),
    sa.Column('period_length', sa.Integer(), nullable=False),
    sa.Column('ovulation_day', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menstrual_cycle')
    # ### end Alembic commands ###
