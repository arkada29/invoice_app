"""(add new table penjualan dan detail penjualan)

Revision ID: b9fe05bc4e01
Revises: d851a8d150ac
Create Date: 2022-06-30 09:15:10.552384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9fe05bc4e01'
down_revision = 'd851a8d150ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('penjualan',
    sa.Column('id_penjualan', sa.Integer(), nullable=False),
    sa.Column('kode_penjualan', sa.String(length=10), nullable=False),
    sa.Column('tanggal_penjualan', sa.DateTime(), nullable=True),
    sa.Column('jumlah_penjualan', sa.Integer(), nullable=True),
    sa.Column('total_pembayaran', sa.Float(precision=20, asdecimal=True, decimal_return_scale=2), nullable=True),
    sa.Column('total_kembalian', sa.Float(precision=20, asdecimal=True, decimal_return_scale=2), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], name=op.f('fk_penjualan_id_user_user')),
    sa.PrimaryKeyConstraint('id_penjualan', name=op.f('pk_penjualan')),
    sa.UniqueConstraint('kode_penjualan', name=op.f('uq_penjualan_kode_penjualan'))
    )
    op.create_table('detail_penjualan',
    sa.Column('id_detail_penjualan', sa.Integer(), nullable=False),
    sa.Column('no_urut', sa.Integer(), nullable=True),
    sa.Column('jumlah_barang', sa.Integer(), nullable=True),
    sa.Column('total_harga', sa.Float(precision=20, asdecimal=True, decimal_return_scale=2), nullable=True),
    sa.Column('sub_total', sa.Integer(), nullable=True),
    sa.Column('potongan', sa.Integer(), nullable=True),
    sa.Column('ppn', sa.Integer(), nullable=True),
    sa.Column('diskon_khusus', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=True),
    sa.Column('kode_barang', sa.Integer(), nullable=True),
    sa.Column('kode_penjualan', sa.Integer(), nullable=True),
    sa.Column('kode_diskon', sa.Integer(), nullable=True),
    sa.Column('id_grosir', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_grosir'], ['grosir.id_grosir'], name=op.f('fk_detail_penjualan_id_grosir_grosir')),
    sa.ForeignKeyConstraint(['kode_barang'], ['barang.kode_barang'], name=op.f('fk_detail_penjualan_kode_barang_barang')),
    sa.ForeignKeyConstraint(['kode_diskon'], ['diskon_khusus.kode_diskon'], name=op.f('fk_detail_penjualan_kode_diskon_diskon_khusus')),
    sa.ForeignKeyConstraint(['kode_penjualan'], ['penjualan.kode_penjualan'], name=op.f('fk_detail_penjualan_kode_penjualan_penjualan')),
    sa.PrimaryKeyConstraint('id_detail_penjualan', name=op.f('pk_detail_penjualan'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detail_penjualan')
    op.drop_table('penjualan')
    # ### end Alembic commands ###
