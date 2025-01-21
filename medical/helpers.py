from django.db.models import Count, Avg, F, Q
from django.db.models.functions import TruncMonth, TruncYear
from .models import Treatment, Tests, Medication
from accounts.models import User

class MedicalDataAnalytics:
    """A class to generate descriptive analytics for medical data."""


    @staticmethod
    def get_research_dataset(option: str):
        """Returns csv with dataset"""
        option = option
        return None

    @staticmethod
    def get_treatment_frequency():
        """Returns the frequency of each treatment type."""
        return Treatment.objects.values('treatment_type').annotate(total=Count('treatment_type'))

    @staticmethod
    def get_treatment_age_pie():
        """Returns the frequency of each treatment type."""
        return {"0-16":35, "17-30": 10, "31-60":35, "61+": 10}#Treatment.objects.values('treatment_type').annotate(total=Count('treatment_type'))

    @staticmethod
    def get_test_age_pie():
            """Returns the frequency of each treatment type."""
            return {"0-16":9, "17-30": 12, "31-60":6, "61+": 4}#Treatment.objects.values('treatment_type').annotate(total=Count('treatment_type'))

    @staticmethod
    def get_test_gender_pie():
            """Returns the frequency of each treatment type."""
            return {"Male":17, "Female": 7}
    
    @staticmethod
    def get_treatment_gender_pie():
            """Returns the frequency of each treatment type."""
            return {"Male":3, "Female": 12}

    @staticmethod
    def get_treatment_status_breakdown():
        """Returns the distribution of treatment statuses."""
        return Treatment.objects.values('status').annotate(total=Count('status'))

    @staticmethod
    def get_average_treatment_duration():
        """Returns the average duration in days of treatments with follow-up dates."""
        avg_duration = Treatment.objects.filter(follow_up_date__isnull=False).annotate(
            duration=F('follow_up_date') - F('created')
        ).aggregate(Avg('duration'))
        return avg_duration['duration__avg'].days if avg_duration['duration__avg'] else None

    @staticmethod
    def get_symptom_diagnosis_correlation():
        """Returns a breakdown of common symptoms and associated diagnoses."""
        return Treatment.objects.values('symptoms', 'diagnosis').annotate(total=Count('pk'))


    @staticmethod
    def get_doctor_activity():
        """Returns the number of treatments handled by each doctor."""
        return Treatment.objects.values('doctor__pk', 'doctor__username').annotate(total=Count('pk')).order_by('-total')

    @staticmethod
    def get_test_type_frequency():
        """Returns the frequency of each test type."""
        return Tests.objects.values('test_type').annotate(total=Count('test_type'))

    @staticmethod
    def get_test_result_distribution():
        """Returns the distribution of test results."""
        return Tests.objects.filter(result__isnull=False).values('result').annotate(total=Count('result'))

    @staticmethod
    def get_medication_frequency():
        """Returns the frequency of each prescribed medication."""
        return Medication.objects.values('name').annotate(total=Count('name')).order_by('-total')

    @staticmethod
    def get_route_of_administration_breakdown():
        """Returns the distribution of routes of administration."""
        return Medication.objects.values('route_of_administration').annotate(total=Count('route_of_administration'))

    @staticmethod
    def get_spke_effect_report():
        """Returns count of treatments involving medications with reported spke effects."""
        return Treatment.objects.filter(medications__spke_effects__isnull=False).distinct().count()

    @staticmethod
    def get_frequency_of_dosage_patterns():
        """Returns the frequency distribution of dosage patterns (Once, Twice, Thrice, etc.)."""
        return Medication.objects.values('frequency').annotate(total=Count('frequency'))

    @staticmethod
    def get_monthly_treatment_counts():
        """Returns a monthly count of treatments."""
        return Treatment.objects.annotate(month=TruncMonth('created')).values('month').annotate(total=Count('pk'))

    @staticmethod
    def get_yearly_test_counts():
        """Returns the yearly count of tests conducted."""
        return Tests.objects.annotate(year=TruncYear('created')).values('year').annotate(total=Count('pk'))

    @staticmethod
    def get_demographic_based_treatments(gender=None, age_range=None):
        """Returns count of treatments based on patient demographics, filtered by gender and/or age range.
        
        Parameters:
            gender (str): 'Male' or 'Female' for gender-based breakdown.
            age_range (tuple): A tuple (min_age, max_age) to filter by age range.
        """
        query = Treatment.objects.all()
        if gender:
            query = query.filter(patient__gender=gender)
        if age_range:
            min_age, max_age = age_range
            query = query.filter(patient__age__gte=min_age, patient__age__lte=max_age)
        return query.count()

    @staticmethod
    def get_treatments_with_spke_effects():
        """Returns treatments with medications that list known spke effects."""
        return Treatment.objects.filter(medications__spke_effects__isnull=False).distinct()

    @staticmethod
    def get_patient_treatment_history(patient_pk):
        """Returns a summary of treatments for a specific patient."""
        return Treatment.objects.filter(patient__pk=patient_pk).values(
            'title', 'treatment_type', 'status', 'created', 'follow_up_date'
        ).order_by('-created')

    @staticmethod
    def get_treatments_by_doctor(doctor_pk):
        """Returns treatments handled by a specific doctor."""
        return Treatment.objects.filter(doctor__pk=doctor_pk).values(
            'title', 'treatment_type', 'status', 'created', 'updated'
        ).order_by('-created')

    @staticmethod
    def get_treatment_completion_rate():
        """Returns the percentage of completed treatments."""
        total_treatments = Treatment.objects.count()
        completed_treatments = Treatment.objects.filter(status='Completed').count()
        return (completed_treatments / total_treatments * 100) if total_treatments > 0 else 0

    @staticmethod
    def get_avg_treatments_per_patient():
        """Returns the average number of treatments per patient."""
        total_patients = User.objects.filter(role='Patient').count()
        total_treatments = Treatment.objects.count()
        return total_treatments / total_patients if total_patients > 0 else 0

    @staticmethod
    def get_avg_tests_per_patient():
        """Returns the average number of tests per patient."""
        total_patients = User.objects.filter(role='Patient').count()
        total_tests = Tests.objects.count()
        return total_tests / total_patients if total_patients > 0 else  0

    @staticmethod
    def get_treatments_by_age_group():
        """Returns the count of treatments segmented by age groups."""
        age_groups = {
            'Under 18':  Q(patient__pk__lt=18),
            '18-35': Q(patient__pk__gte=18, patient__pk__lte=35),
            '36-50': Q(patient__pk__gte=36, patient__pk__lte=50),
            '51-65': Q(patient__pk__gte=51, patient__pk__lte=65),
            '66 and above': Q(patient__pk__gte=66),
        }
        return {age_group: Treatment.objects.filter(criteria).count() for age_group, criteria in age_groups.items()}

    @staticmethod
    def get_treatments_by_gender():
        """Returns the count of treatments segmented by age groups."""
        gender_groups = {
            'Male':  Q(patient__profile__gender='Male'),
            'Female': Q(patient__profile__gender='Female'),
        }
        return {gender_group: Treatment.objects.filter(criteria).count() for gender_group, criteria in gender_groups.items()}

    @staticmethod
    def get_treatment_type_by_age_group():
        """Returns the count of treatments segmented by age groups."""
        age_groups = {
            'Initial Assessment':  18,
            'Follow Up': 35,
            'Therapy': 36,
            'Surgery': 51,
            'Medication': 66,
            'Rehabilitation': 23,
            'Diagnostic': 26,
            'Preventive': 15,
            'Consultation': 19
        }
        return age_groups
    
    @staticmethod
    def get_treatment_gender_bar_chart_data():
        data = {
            'keys': ['Initial Assessment', 'Follow Up', 'Therapy', 'Surgery', 'Medication', 'Rehabilitation', 'Diagnostic', 'Preventive', 'Consultation'],
            'male': [12, 34, 3, 23, 45, 23, 15, 4, 6],
            'female': [22, 14, 43, 13, 25, 13, 5, 9, 16]
        }
        return data
    
    @staticmethod
    def get_treatment_by_gender():
        """Returns the count of treatments segmented by gender groups."""
        location_groups = {
            'Harare South':  18,
            'Harare East': 35,
            'Harare West': 36,
            'Harare North': 51,
            'Other': 66,
            
        }
        return location_groups

    @staticmethod
    def get_test_by_location():
        """Returns the count of treatments segmented by gender groups."""
        location_groups = {
            'Harare South':  8,
            'Harare East': 25,
            'Harare West': 16,
            'Harare North': 31,
            'Other': 36,
            
        }
        return location_groups

    @staticmethod
    def get_dataset(data_type = None):
        if data_type == 'age':
            return Treatment.objects.values(
            'patient__profile__dob',  # Assuming patient has an 'age' field
            'treatment_type',
            'status',
            'created',
            'follow_up_date'
        )
        
        if data_type == 'gender':
            return Treatment.objects.values(
            'patient__profile__gender',
            'treatment_type',
            'status',
            'created',
            'follow_up_date'
        )        

        if data_type == 'location':
            return Treatment.objects.values(
            'patient__profile__location',
            'treatment_type',
            'status',
            'created',
            'follow_up_date'
        )        


def get_treatments_with_medication():
    treatments = []
    for medicine in Medication.objects.all():
        for treat in Treatment.objects.filter(treatment_medications= medicine):
            treatments.append({'medicine': medicine, 'treatment': treat})

    return treatments

