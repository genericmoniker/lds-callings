from application import lds, models
from application.tenant import activate_tenant
from worker.app import db


def synchronize(s, unit):
    activate_tenant(db, unit)
    data = lds.fetch_callings(s, unit)
    households = data['households']
    for household in households:
        _sync_household(household)
    db.session.commit()


def _sync_household(household):
    _sync_individual(household['headOfHouse'])
    children = household['children']
    for child in children:
        _sync_individual(child)


def _sync_individual(individual_data):
    individual = models.Individual(
        id=individual_data['individualId'],
        preferred_name=individual_data['preferredName']
    )
    db.session.merge(individual)
