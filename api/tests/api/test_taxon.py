from itertools import cycle

from flask.testing import FlaskClient

from ukbol.data.uksi import ROOT_NAMES
from ukbol.extensions import db
from ukbol.model import Specimen, Taxon
from ukbol.schema import SpecimenSchema, TaxonSchema

taxon_schema = TaxonSchema()
specimen_schema = SpecimenSchema()


def test_roots(client: FlaskClient):
    response = client.get("/api/taxon/roots")
    assert response.is_json

    expected_roots = db.session.scalars(
        db.select(Taxon).filter(Taxon.name.in_(ROOT_NAMES))
    ).all()
    expected_json = taxon_schema.dump(expected_roots, many=True)

    assert response.json == expected_json


class TestGetTaxon:
    def test_404(self, client: FlaskClient):
        response = client.get("/api/taxon/nope")
        assert response.status_code == 404

    def test_ok(self, client: FlaskClient):
        response = client.get("/api/taxon/BMSSYS0000042047")
        assert response.is_json
        assert response.json == taxon_schema.dump(Taxon.get("BMSSYS0000042047"))


class TestTaxonChildren:
    def test_404(self, client: FlaskClient):
        response = client.get("/api/taxon/nope/children")
        assert response.status_code == 404

    def test_ok(self, client: FlaskClient):
        response = client.get("/api/taxon/NHMSYS0020535450/children")
        assert response.is_json
        # these ids are in name order as that is how the API returns the children
        child_ids = ["NHMSYS0020535046", "BMSSYS0000052700"]
        assert response.json == taxon_schema.dump(map(Taxon.get, child_ids), many=True)


class TestTaxonParents:
    def test_404(self, client: FlaskClient):
        response = client.get("/api/taxon/nope/parents")
        assert response.status_code == 404

    def test_no_parents(self, client: FlaskClient):
        response = client.get("/api/taxon/NHMSYS0020535450/parents")
        assert response.is_json
        assert response.json == []

    def test_ok(self, client: FlaskClient):
        response = client.get("/api/taxon/BMSSYS0000000001/parents")
        assert response.is_json
        assert response.json == [
            "NHMSYS0001472727",
            "BMSSYS0000042047",
            "BMSSYS0000042048",
            "NHMSYS0020535847",
            "NHMSYS0020535046",
            "NHMSYS0020535450",
        ]


def create_specimens(
    taxon: Taxon,
    matches: int,
    synonym_matches: int,
    no_matches: int,
) -> tuple[list[Specimen], list[Specimen]]:
    # i didn't set our sample uksi and bold files with crossover (i.e. there's no bold
    # specimens in the sample with names that match the uksi sample data) so we'll just
    # add some manually. This isn't a bad thing because it means we can test how the
    # matching works too
    matching_specimens = []
    not_matching_specimens = []

    for i in range(matches):
        matching_specimens.append(
            Specimen(
                specimenid=f"m-specimen-{i}",
                identification=taxon.name,
                bin_uri="bin001",
            )
        )

    for i, synonym in zip(range(synonym_matches), cycle(taxon.synonyms)):
        matching_specimens.append(
            Specimen(
                specimenid=f"s-specimen-{i}",
                identification=synonym.name,
                bin_uri="bin002",
            )
        )

    for i in range(no_matches):
        not_matching_specimens.append(
            Specimen(specimenid=f"n-specimen-{i}", identification="beans")
        )

    db.session.add_all(matching_specimens)
    db.session.add_all(not_matching_specimens)
    db.session.commit()

    # sort by identification and id just like the API does
    matching_specimens.sort(key=lambda spec: (spec.identification, spec.id))

    return matching_specimens, not_matching_specimens


class TestTaxonSpecimens:
    def test_404(self, client: FlaskClient):
        response = client.get("/api/taxon/nope/associated_specimens")
        assert response.status_code == 404

    def test_ok(self, client: FlaskClient):
        taxon = Taxon.get("BMSSYS0000000015")
        specimens, _ = create_specimens(taxon, 4, 3, 9)
        response = client.get(f"/api/taxon/{taxon.id}/associated_specimens")
        assert response.is_json
        assert response.json == {
            "count": len(specimens),
            "specimens": specimen_schema.dump(specimens, many=True),
        }

    def test_paging(self, client: FlaskClient):
        taxon = Taxon.get("BMSSYS0000000015")
        specimens, _ = create_specimens(taxon, 4, 3, 9)
        response = client.get(
            f"/api/taxon/{taxon.id}/associated_specimens?page=3&per_page=2"
        )
        assert response.is_json
        assert response.json == {
            "count": len(specimens),
            "specimens": specimen_schema.dump(specimens[4:6], many=True),
        }
