"""Add last_name to User

Revision ID: 87f08a9dffc0
Revises: 
Create Date: 2024-05-23 10:37:54.623884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87f08a9dffc0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_name', sa.String(length=100), nullable=False))
        batch_op.add_column(sa.Column('role_A', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('role_B', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('role_C', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role_C')
        batch_op.drop_column('role_B')
        batch_op.drop_column('role_A')
        batch_op.drop_column('last_name')

    # ### end Alembic commands ###
