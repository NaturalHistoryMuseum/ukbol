"""
expand bold table.

Revision ID: c22e5eca6a4d
Revises: 507c9999ba67
Create Date: 2025-03-03 12:36:50.934648
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c22e5eca6a4d'
down_revision = '507c9999ba67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('specimen', schema=None) as batch_op:
        batch_op.add_column(sa.Column('processid', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('sampleid', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('fieldid', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('museumid', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('record_id', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('specimenid', sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column('processid_minted_date', sa.String(), nullable=True)
        )
        batch_op.add_column(sa.Column('bin_created_date', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('collection_code', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('inst', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('taxid', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('tribe', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('species_reference', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('identification', sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column('identification_method', sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('identification_rank', sa.String(), nullable=True)
        )
        batch_op.add_column(sa.Column('identified_by', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('identifier_email', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('taxonomy_notes', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('sex', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('reproduction', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('life_stage', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('short_note', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('notes', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('voucher_type', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('tissue_type', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('specimen_linkout', sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column('associated_specimens', sa.String(), nullable=True)
        )
        batch_op.add_column(sa.Column('associated_taxa', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('collectors', sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column('collection_date_start', sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('collection_date_end', sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('collection_event_id', sa.String(), nullable=True)
        )
        batch_op.add_column(sa.Column('collection_time', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('collection_notes', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('geoid', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('country_ocean', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('country_iso', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('province_state', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('region', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('sector', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('site', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('site_code', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('coord', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('coord_accuracy', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('coord_source', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('elev', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('elev_accuracy', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('depth', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('depth_accuracy', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('habitat', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('sampling_protocol', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('nuc', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('nuc_basecount', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('insdc_acs', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('funding_src', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('marker_code', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('primers_forward', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('primers_reverse', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('sequence_run_site', sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column('sequence_upload_date', sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('bold_recordset_code_arr', sa.String(), nullable=True)
        )
        batch_op.add_column(sa.Column('ecoregion', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('biome', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('realm', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('sovereign_inst', sa.String(), nullable=True))
        batch_op.drop_index('ix_specimen_country')
        batch_op.create_index(
            batch_op.f('ix_specimen_country_iso'), ['country_iso'], unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_specimen_identification'), ['identification'], unique=False
        )
        batch_op.create_index(
            batch_op.f('ix_specimen_identification_rank'),
            ['identification_rank'],
            unique=False,
        )
        batch_op.drop_column('name')
        batch_op.drop_column('country')
        batch_op.drop_column('specimen_id')
        batch_op.drop_column('rank')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('specimen', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('rank', sa.VARCHAR(), autoincrement=False, nullable=True)
        )
        batch_op.add_column(
            sa.Column('specimen_id', sa.VARCHAR(), autoincrement=False, nullable=True)
        )
        batch_op.add_column(
            sa.Column('country', sa.VARCHAR(), autoincrement=False, nullable=True)
        )
        batch_op.add_column(
            sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True)
        )
        batch_op.drop_index(batch_op.f('ix_specimen_identification_rank'))
        batch_op.drop_index(batch_op.f('ix_specimen_identification'))
        batch_op.drop_index(batch_op.f('ix_specimen_country_iso'))
        batch_op.create_index('ix_specimen_country', ['country'], unique=False)
        batch_op.drop_column('sovereign_inst')
        batch_op.drop_column('realm')
        batch_op.drop_column('biome')
        batch_op.drop_column('ecoregion')
        batch_op.drop_column('bold_recordset_code_arr')
        batch_op.drop_column('sequence_upload_date')
        batch_op.drop_column('sequence_run_site')
        batch_op.drop_column('primers_reverse')
        batch_op.drop_column('primers_forward')
        batch_op.drop_column('marker_code')
        batch_op.drop_column('funding_src')
        batch_op.drop_column('insdc_acs')
        batch_op.drop_column('nuc_basecount')
        batch_op.drop_column('nuc')
        batch_op.drop_column('sampling_protocol')
        batch_op.drop_column('habitat')
        batch_op.drop_column('depth_accuracy')
        batch_op.drop_column('depth')
        batch_op.drop_column('elev_accuracy')
        batch_op.drop_column('elev')
        batch_op.drop_column('coord_source')
        batch_op.drop_column('coord_accuracy')
        batch_op.drop_column('coord')
        batch_op.drop_column('site_code')
        batch_op.drop_column('site')
        batch_op.drop_column('sector')
        batch_op.drop_column('region')
        batch_op.drop_column('province_state')
        batch_op.drop_column('country_iso')
        batch_op.drop_column('country_ocean')
        batch_op.drop_column('geoid')
        batch_op.drop_column('collection_notes')
        batch_op.drop_column('collection_time')
        batch_op.drop_column('collection_event_id')
        batch_op.drop_column('collection_date_end')
        batch_op.drop_column('collection_date_start')
        batch_op.drop_column('collectors')
        batch_op.drop_column('associated_taxa')
        batch_op.drop_column('associated_specimens')
        batch_op.drop_column('specimen_linkout')
        batch_op.drop_column('tissue_type')
        batch_op.drop_column('voucher_type')
        batch_op.drop_column('notes')
        batch_op.drop_column('short_note')
        batch_op.drop_column('life_stage')
        batch_op.drop_column('reproduction')
        batch_op.drop_column('sex')
        batch_op.drop_column('taxonomy_notes')
        batch_op.drop_column('identifier_email')
        batch_op.drop_column('identified_by')
        batch_op.drop_column('identification_rank')
        batch_op.drop_column('identification_method')
        batch_op.drop_column('identification')
        batch_op.drop_column('species_reference')
        batch_op.drop_column('tribe')
        batch_op.drop_column('taxid')
        batch_op.drop_column('inst')
        batch_op.drop_column('collection_code')
        batch_op.drop_column('bin_created_date')
        batch_op.drop_column('processid_minted_date')
        batch_op.drop_column('specimenid')
        batch_op.drop_column('record_id')
        batch_op.drop_column('museumid')
        batch_op.drop_column('fieldid')
        batch_op.drop_column('sampleid')
        batch_op.drop_column('processid')

    # ### end Alembic commands ###
