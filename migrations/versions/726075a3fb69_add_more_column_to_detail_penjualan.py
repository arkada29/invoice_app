"""(add more column to detail_penjualan)

Revision ID: 726075a3fb69
Revises: 598eea074ff4
Create Date: 2022-06-21 11:01:03.991042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '726075a3fb69'
down_revision = '598eea074ff4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('detail_penjualan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('jumlah_bayar', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('sub_total', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('potongan', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('diskon_khusus', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('detail_penjualan', schema=None) as batch_op:
        batch_op.drop_column('diskon_khusus')
        batch_op.drop_column('potongan')
        batch_op.drop_column('sub_total')
        batch_op.drop_column('jumlah_bayar')

    # ### end Alembic commands ###
