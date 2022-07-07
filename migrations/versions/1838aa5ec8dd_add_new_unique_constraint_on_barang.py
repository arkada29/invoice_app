"""(add new unique constraint on barang)

Revision ID: 1838aa5ec8dd
Revises: 4db18ee25de6
Create Date: 2022-06-17 11:21:01.910278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1838aa5ec8dd'
down_revision = '4db18ee25de6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.drop_constraint('fk_barang_id_satuan', type_='unique')
        batch_op.create_unique_constraint('uq_barang_kode_nama_satuan', ['kode_barang', 'nama_barang', 'id_satuan'])

    with op.batch_alter_table('diskon_khusus', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_diskon_khusus_kode_diskon'), ['kode_diskon'])

    with op.batch_alter_table('kategori', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_kategori_kode_kategori'), ['kode_kategori'])

    with op.batch_alter_table('penjualan', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_penjualan_kode_penjualan'), ['kode_penjualan'])

    with op.batch_alter_table('satuan', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_satuan_satuan'), ['satuan'])

    with op.batch_alter_table('supplier', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_supplier_nama_supplier'), ['nama_supplier'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_name'), ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_name'), type_='unique')

    with op.batch_alter_table('supplier', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_supplier_nama_supplier'), type_='unique')

    with op.batch_alter_table('satuan', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_satuan_satuan'), type_='unique')

    with op.batch_alter_table('penjualan', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_penjualan_kode_penjualan'), type_='unique')

    with op.batch_alter_table('kategori', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_kategori_kode_kategori'), type_='unique')

    with op.batch_alter_table('diskon_khusus', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_diskon_khusus_kode_diskon'), type_='unique')

    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.drop_constraint('uq_barang_kode_nama_satuan', type_='unique')
        batch_op.create_unique_constraint('fk_barang_id_satuan', ['id_satuan'])

    # ### end Alembic commands ###
