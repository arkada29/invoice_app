"""(add barang_pic to barang)

Revision ID: 3eba40fb3294
Revises: 60ac783e5cec
Create Date: 2022-06-16 11:40:46.527779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eba40fb3294'
down_revision = '60ac783e5cec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.add_column(sa.Column('barang_pic', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.drop_column('barang_pic')

    # ### end Alembic commands ###
