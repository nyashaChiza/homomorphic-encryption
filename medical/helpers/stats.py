from django.db.models import Count, Q
from django.db.models.functions import TruncMonth, TruncYear
from ..models import Treatment, Tests, Medication
from accounts.models import User
from datetime import date, timedelta

class MedicalDataAnalytics:
    """A class to generate descriptive analytics for medical data."""

    @staticmethod
    def get_research_dataset(option: str):
        """Returns dataset in CSV format based on the option."""
        # Example implementation for generating a CSV file
        if option == 'age':
            data = Treatment.objects.values('patient__profile__dob', 'treatment_type', 'status', 'created', 'follow_up_date')
        elif option == 'gender':
            data = Treatment.objects.values('patient__profile__gender', 'treatment_type', 'status', 'created', 'follow_up_date')
        elif option == 'location':
            data = Treatment.objects.values('patient__profile__location', 'treatment_type', 'status', 'created', 'follow_up_date')
        else:
            data = []

        # Code to convert data to CSV can be added here
        return data

    @staticmethod
    def get_treatment_frequency():
        """Returns the frequency of each treatment type."""
        return Treatment.objects.values('treatment_type').annotate(total=Count('treatment_type'))

    @staticmethod
    def get_test_gender_pie():
        """Returns the frequency of tests segmented by gender."""
        gender_groups = {
            'Male': Tests.objects.filter(patient__profile__gender='Male').count(),
            'Female': Tests.objects.filter(patient__profile__gender='Female').count(),
        }
        return gender_groups

    @staticmethod
    def get_treatment_gender_pie():
        """Returns the frequency of treatments segmented by gender."""
        gender_groups = {
            'Male': Treatment.objects.filter(patient__profile__gender='Male').count(),
            'Female': Treatment.objects.filter(patient__profile__gender='Female').count(),
        }
        return gender_groups

    @staticmethod
    def get_tests_by_age_group():
        """Returns the count of tests segmented by age groups."""
        age_groups = {
            'Under 18': Tests.objects.filter(patient__profile__dob__gte=date.today().replace(year=date.today().year-18)).count(),
            '18-35': Tests.objects.filter(patient__profile__dob__lte=date.today().replace(year=date.today().year-18)).filter(patient__profile__dob__gte=date.today().replace(year=date.today().year-35)).count(),
            '36-50': Tests.objects.filter(patient__profile__dob__lte=date.today().replace(year=date.today().year-36)).filter(patient__profile__dob__gte=date.today().replace(year=date.today().year-50)).count(),
            '51-65': Tests.objects.filter(patient__profile__dob__lte=date.today().replace(year=date.today().year-51)).filter(patient__profile__dob__gte=date.today().replace(year=date.today().year-65)).count(),
            '66 and above': Tests.objects.filter(patient__profile__dob__lte=date.today().replace(year=date.today().year-66)).count(),
        }
        return age_groups

    @staticmethod
    def get_treatments_by_age_group():
        """Returns the count of treatments segmented by age groups."""
        age_groups = {
            'Under 18': Treatment.objects.filter(patient__profile__dob__gte=date.today().replace(year=date.today().year-18)).count(),
            '18-35': Treatment.objects.filter(patient__profile__dob__lte=date.today().replace(year=date.today().year-18)).filter(patient__profile__dob__gte=date.today().replace(year=date.today().year-35)).count(),
            '36-50': Treatment.objects.filter(patient__profile__dob__lte=date.today().replace(year=date.today().year-36)).filter(patient__profile__dob__gte=date.today().replace(year=date.today().year-50)).count(),
            '51-65': Treatment.objects.filter(patient__profile__dob__lte=date.today().replace(year=date.today().year-51)).filter(patient__profile__dob__gte=date.today().replace(year=date.today().year-65)).count(),
            '66 and above': Treatment.objects.filter(patient__profile__dob__lte=date.today().replace(year=date.today().year-66)).count(),
        }
        return age_groups


    @staticmethod
    def get_treatment_by_gender():
        """Returns the count of treatments segmented by gender, excluding None values."""
        # Query treatments grouped by patient gender, ensuring no None values in the gender field
        gender_groups = Treatment.objects.values('patient__profile__gender') \
                                        .annotate(count=Count('id')) \
                                        .filter(patient__profile__gender__isnull=False) \
                                        .order_by('patient__profile__gender')
        
        # Create a dictionary to map gender to count, excluding any None values
        result = {gender['patient__profile__gender']: gender['count'] for gender in gender_groups if gender['patient__profile__gender'] is not None}
        
        return result



    @staticmethod
    def get_treatment_by_gender():
        """Returns the count of treatments segmented by gender."""
        gender_groups = Treatment.objects.values('patient__profile__gender') \
                                        .annotate(count=Count('id')) \
                                        .order_by('patient__profile__gender')
        
        # Create a dictionary to map gender to count
        result = {gender['patient__profile__gender']: gender['count'] for gender in gender_groups}
        return result


    @staticmethod
    def get_treatments_by_gender():
        """Returns the count of treatments segmented by gender."""
        gender_groups = {
            'Male': Treatment.objects.filter(patient__profile__gender='Male').count(),
            'Female': Treatment.objects.filter(patient__profile__gender='Female').count(),
        }
        return gender_groups

    @staticmethod
    def get_treatment_type_by_age_group():
        """Returns the count of treatments segmented by treatment types and age groups."""
        # Assuming treatment types and their age group mappings are predefined
        age_groups = {
            'Initial Assessment': Treatment.objects.filter(treatment_type='Initial Assessment').count(),
            'Follow Up': Treatment.objects.filter(treatment_type='Follow Up').count(),
            'Therapy': Treatment.objects.filter(treatment_type='Therapy').count(),
            'Surgery': Treatment.objects.filter(treatment_type='Surgery').count(),
            'Medication': Treatment.objects.filter(treatment_type='Medication').count(),
            'Rehabilitation': Treatment.objects.filter(treatment_type='Rehabilitation').count(),
            'Diagnostic': Treatment.objects.filter(treatment_type='Diagnostic').count(),
            'Preventive': Treatment.objects.filter(treatment_type='Preventive').count(),
            'Consultation': Treatment.objects.filter(treatment_type='Consultation').count()
        }
        return age_groups

    @staticmethod
    def get_treatment_gender_bar_chart_data():
        """Returns the count of treatments for each treatment type segmented by gender for a bar chart."""
        treatment_types = ['Initial Assessment', 'Follow Up', 'Therapy', 'Surgery', 'Medication', 'Rehabilitation', 'Diagnostic', 'Preventive', 'Consultation']
        male_data = [Treatment.objects.filter(treatment_type=treatment, patient__profile__gender='Male').count() for treatment in treatment_types]
        female_data = [Treatment.objects.filter(treatment_type=treatment, patient__profile__gender='Female').count() for treatment in treatment_types]
        
        data = {
            'keys': treatment_types,
            'male': male_data,
            'female': female_data
        }
        return data

    @staticmethod
    def get_treatment_by_location():
        """Returns the count of treatments segmented by location."""
        location_groups = {
            'Harare South': Treatment.objects.filter(patient__profile__location='Harare South').count(),
            'Harare East': Treatment.objects.filter(patient__profile__location='Harare East').count(),
            'Harare West': Treatment.objects.filter(patient__profile__location='Harare West').count(),
            'Harare North': Treatment.objects.filter(patient__profile__location='Harare North').count(),
            'Other': Treatment.objects.filter(~Q(patient__profile__location__in=['Harare South', 'Harare East', 'Harare West', 'Harare North'])).count(),
        }
        return location_groups

    @staticmethod
    def get_test_by_location():
        """Returns the count of tests segmented by location."""
        location_groups = {
            'Harare South': Tests.objects.filter(patient__profile__location='Harare South').count(),
            'Harare East': Tests.objects.filter(patient__profile__location='Harare East').count(),
            'Harare West': Tests.objects.filter(patient__profile__location='Harare West').count(),
            'Harare North': Tests.objects.filter(patient__profile__location='Harare North').count(),
            'Other': Tests.objects.filter(~Q(patient__profile__location__in=['Harare South', 'Harare East', 'Harare West', 'Harare North'])).count(),
        }
        return location_groups

def get_treatments_with_medication():
    """Returns treatments with their corresponding medications."""
    treatments_with_medications = []
    for medicine in Medication.objects.all():
        for treat in Treatment.objects.filter(treatment_medications=medicine):
            treatments_with_medications.append({'medicine': medicine, 'treatment': treat})

    return treatments_with_medications
