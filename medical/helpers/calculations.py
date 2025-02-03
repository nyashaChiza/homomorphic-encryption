from django.db.models import Sum, Avg, Count, F
from collections import Counter

from medical.models import Treatment, TreatmentMedication


class MedicalCalculations:
     def calculate_medication_adherence(self, patient_id, medication_id):
          """
          Calculate how consistently a patient adheres to a prescribed medication.
          """
          prescribed = TreatmentMedication.objects.filter(
               treatment__patient_id=patient_id,
               medication_id=medication_id
          ).aggregate(total_quantity=Sum('quantity'))['total_quantity']

          total_treatment_days = Treatment.objects.filter(
               patient_id=patient_id,
               treatment_medications__medication_id=medication_id
          ).annotate(duration=F('follow_up_date') - F('created')).aggregate(
               total_days=Sum('duration')
          )['total_days']

          if prescribed and total_treatment_days:
               expected_daily_dosage = prescribed / total_treatment_days.days
               adherence = (expected_daily_dosage / prescribed) * 100
               return {'status': 'Success', 'value':round(adherence, 2)}
          return {'status': 'Failed', 'value':"Not enough data to calculate adherence"}


     def calculate_average_recovery_time(self,treatment_type):
          """
          Calculate the average recovery time for a specific treatment type.
          """
          avg_recovery = Treatment.objects.filter(
               treatment_type=treatment_type, follow_up_date__isnull=False
          ).annotate(duration=F('follow_up_date') - F('created')).aggregate(
               Avg('duration')
          )['duration__avg']

          return {'status': 'Success','value':f"{avg_recovery.days} days"} if avg_recovery else {'status': 'Failed','value':"Not enough data"}


     def find_high_risk_patients(self,follow_up_threshold):
          """
          Identify patients requiring frequent follow-ups based on a threshold.
          """
          high_risk_patients = Treatment.objects.filter(follow_up_date__isnull=False).values(
               'patient__id', 'patient__username'
          ).annotate(follow_up_count=Count('follow_up_date')).filter(
               follow_up_count__gte=follow_up_threshold
          )
          if high_risk_patients:
               return {'status': 'Success', 'value': 'high_risk_patients'}
          else:
               return {'status': 'Failed', 'value': 'No Patients Found'}


     def calculate_treatment_success_rate(self,treatment_type):
          """
          Evaluate the percentage of successful treatments for a specific type.
          """
          total_treatments = Treatment.objects.filter(treatment_type=treatment_type).count()
          successful_treatments = Treatment.objects.filter(
               treatment_type=treatment_type, status="Completed"
          ).count()

          if total_treatments > 0:
               success_rate = (successful_treatments / total_treatments) * 100
               return {'status':'Success', 'value': f"{success_rate:.2f}% success rate"}
          return {'status':'Failed', 'value':"No data for this treatment type"}


     def get_common_symptoms_for_treatment(self,treatment_type):
          """
          Identify the most reported symptoms for a specific treatment type.
          """
          symptoms = Treatment.objects.filter(
               treatment_type=treatment_type
          ).values_list('symptoms', flat=True)

          symptom_counter = Counter(
               symptom for symptom_list in symptoms if symptom_list for symptom in symptom_list.split(",")
          )
          common_symptoms = symptom_counter.most_common(5)
          common_symptoms = [sympthom[0] for sympthom in common_symptoms]
          if common_symptoms :
               return {'status': 'Success', 'value':common_symptoms}
          else:
               return {'status': 'Failed', 'value':"no symthoms found"}

       # Return top 5 symptoms
