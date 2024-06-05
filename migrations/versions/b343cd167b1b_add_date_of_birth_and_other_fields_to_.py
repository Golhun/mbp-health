"""Add date_of_birth and other fields to User model

Revision ID: b343cd167b1b
Revises: 87f08a9dffc0
Create Date: 2024-05-24 08:40:23.495244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b343cd167b1b'
down_revision = '87f08a9dffc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('date_of_birth', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('height', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('weight', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('medications', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('allergies', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('allergies')
        batch_op.drop_column('medications')
        batch_op.drop_column('weight')
        batch_op.drop_column('height')
        batch_op.drop_column('date_of_birth')
        batch_op.drop_column('profile_picture')

    # ### end Alembic commands ###
