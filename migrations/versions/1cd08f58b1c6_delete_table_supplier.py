"""(delete table supplier)

Revision ID: 1cd08f58b1c6
Revises: 1838aa5ec8dd
Create Date: 2022-06-20 10:22:59.609906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cd08f58b1c6'
down_revision = '1838aa5ec8dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supplier')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supplier',
    sa.Column('id_supplier', sa.INTEGER(), nullable=False),
    sa.Column('nama_supplier', sa.VARCHAR(length=255), nullable=True),
    sa.Column('jumlah', sa.INTEGER(), nullable=True),
    sa.Column('terjual', sa.INTEGER(), nullable=True),
    sa.Column('sisa', sa.INTEGER(), nullable=True),
    sa.Column('harga_satuan', sa.FLOAT(), nullable=True),
    sa.Column('harga_total', sa.FLOAT(), nullable=True),
    sa.Column('tanggal_taruh', sa.DATETIME(), nullable=True),
    sa.Column('created_date', sa.DATETIME(), nullable=False),
    sa.Column('updated_date', sa.DATETIME(), nullable=True),
    sa.Column('id_user', sa.INTEGER(), nullable=True),
    sa.Column('id_barang', sa.INTEGER(), nullable=True),
    sa.Column('id_kategori', sa.INTEGER(), nullable=True),
    sa.Column('id_satuan', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['id_barang'], ['barang.id_barang'], ),
    sa.ForeignKeyConstraint(['id_kategori'], ['kategori.id_kategori'], ),
    sa.ForeignKeyConstraint(['id_satuan'], ['satuan.id_satuan'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_supplier'),
    sa.UniqueConstraint('nama_supplier', name='uq_supplier_nama_supplier')
    )
    # ### end Alembic commands ###
