"""create_main_tables
Revision ID: c8eef084d7c0
Revises: 
Create Date: 2021-04-03 14:06:21.868765
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from config import settings

# revision identifiers, used by Alembic
revision = 'c8eef084d7c0'
down_revision = None
branch_labels = None
depends_on = None

## todo: Fix this coupled constant TABLE NAME
def create_cleanings_table() -> None:
    op.create_table(
        "todolist2",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("timestamp", sa.TIMESTAMP, nullable=False, default=datetime.now),
        sa.Column("completed", sa.BOOLEAN, default=False),
    )


def upgrade() -> None:
    create_cleanings_table()


def downgrade() -> None:
    op.drop_table("todolist2")
