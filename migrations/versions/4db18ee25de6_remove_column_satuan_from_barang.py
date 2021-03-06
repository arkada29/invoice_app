"""(remove column satuan from barang)

Revision ID: 4db18ee25de6
Revises: 485ea9f9f8c6
Create Date: 2022-06-17 08:37:02.923640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4db18ee25de6'
down_revision = '485ea9f9f8c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.create_unique_constraint('fk_barang_id_satuan', ['id_satuan'])
        batch_op.drop_column('satuan')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.add_column(sa.Column('satuan', sa.VARCHAR(length=10), nullable=False))
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
