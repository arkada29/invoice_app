"""(add status to barang)

Revision ID: 485ea9f9f8c6
Revises: 3eba40fb3294
Create Date: 2022-06-16 18:21:04.331374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '485ea9f9f8c6'
down_revision = '3eba40fb3294'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
