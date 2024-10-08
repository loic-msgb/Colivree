"""Added new columns or models.

Revision ID: 5828aa2ca95a
Revises: 43bd99dd9b06
Create Date: 2024-09-11 23:49:06.048259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5828aa2ca95a'
down_revision = '43bd99dd9b06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('trip', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reserved_weight', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trip', schema=None) as batch_op:
        batch_op.drop_column('reserved_weight')

    op.drop_table('booking')
    # ### end Alembic commands ###
