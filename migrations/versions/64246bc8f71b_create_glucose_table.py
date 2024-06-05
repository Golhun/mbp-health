"""Create glucose table

Revision ID: 64246bc8f71b
Revises: 9d6dfa224538
Create Date: 2024-06-01 20:11:51.903055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '64246bc8f71b'
down_revision = '9d6dfa224538'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('glucose', schema=None) as batch_op:
        batch_op.alter_column('glucose_level',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.Numeric(precision=5, scale=2),
               existing_nullable=False)
        batch_op.alter_column('timestamp',
               existing_type=mysql.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('glucose', schema=None) as batch_op:
        batch_op.alter_column('timestamp',
               existing_type=mysql.DATETIME(),
               nullable=True)
        batch_op.alter_column('glucose_level',
               existing_type=sa.Numeric(precision=5, scale=2),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)

    # ### end Alembic commands ###
