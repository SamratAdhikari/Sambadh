"""Increase password field length

Revision ID: 999abd45177d
Revises: 879cab1316c4
Create Date: 2024-09-01 18:49:14.551126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '999abd45177d'
down_revision = '879cab1316c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=25),
               type_=sa.String(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=25),
               existing_nullable=False)

    # ### end Alembic commands ###
