"""Rule X"""

from .premisable import PremisableMixin

class Rule100(PremisableMixin):
    """Rule X processing"""

    @property
    def rule_attrs(self):
        """Returns premises list"""
        if self.is_exception('sub_building_name'):
            return('sub_name_and_thoroughfare_or_locality',)
        return ('sub_building_name',)

    @property
    def includes_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return self.is_exception('sub_building_name')

    @property
    def _premises_number(self):
        """Returns premises number"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            return ''
        return super()._sub_premises_number

    @property
    def _premises_name(self):
        """Returns premises name"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            return getattr(self, 'dependent_thoroughfare', '')
        return super()._sub_premises_name

    @property
    def _sub_premises_number(self):
        """Returns sub-premises number"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            return super()._sub_premises_number
        return ''

    @property
    def _sub_premises_name(self):
        """Returns sub-premises name"""
        if getattr(self, 'dependent_thoroughfare', '') != '':
            return super()._sub_premises_name
        return ''
