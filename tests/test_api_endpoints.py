from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from django.contrib.auth import get_user_model
import datetime
from src.app.db.mysql.models import InternHoursModel


class ApiIntegrationTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="password123",
        )
        self.client.force_authenticate(user=self.user)
        self.now = timezone.now()

    def create_event(self, name="Evento", admin_id=1, start=None, end=None):
        start = start or self.now
        end = end or (start + datetime.timedelta(days=1))
        payload = {
            'name': name,
            'description': 'Descripción',
            'start_date': start.isoformat(),
            'end_date': end.isoformat(),
            'admin_id': admin_id,
        }
        res = self.client.post('/api/events/', payload, format='json')
        self.assertEqual(res.status_code, 201)
        return res.data['data']['id']

    def test_create_event_and_list(self):
        url = '/api/events/'
        payload = {
            'name': 'Evento de prueba',
            'description': 'Descripción',
            'start_date': self.now.isoformat(),
            'end_date': (self.now + datetime.timedelta(days=1)).isoformat(),
            'admin_id': 1,
        }
        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data.get('status'), 'success')
        data = res.data.get('data')
        self.assertIn('id', data)

        # List events
        res2 = self.client.get('/api/events/')
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data.get('status'), 'success')
        self.assertTrue(len(res2.data.get('data')) >= 1)

    def test_send_evaluation_and_get_average(self):
        # Create event first
        event_id = self.create_event(name="Evento evaluación", admin_id=2)

        eval_payload = {
            'event_id': event_id,
            'evaluated_user_id': 10,
            'evaluator_user_id': 11,
            'type': '360',
            'answers': [
                {'criterion_id': 1, 'score': 4, 'comment': 'bien'},
                {'criterion_id': 2, 'score': 5, 'comment': 'muy bien'},
            ]
        }
        res2 = self.client.post('/api/evaluations/', eval_payload, format='json')
        self.assertEqual(res2.status_code, 201)
        self.assertEqual(res2.data.get('status'), 'success')

        # Get average for evaluated_user_id
        res3 = self.client.get(f'/api/evaluations/average/{eval_payload["evaluated_user_id"]}/')
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(res3.data.get('status'), 'success')
        avg = res3.data['data']['average_score']
        # average of 4 and 5 = 4.5
        self.assertAlmostEqual(float(avg), 4.5, places=2)

    def test_create_event_invalid_dates_returns_400(self):
        payload = {
            'name': 'Evento inválido',
            'description': 'Descripción',
            'start_date': self.now.isoformat(),
            'end_date': (self.now - datetime.timedelta(days=1)).isoformat(),
            'admin_id': 1,
        }
        res = self.client.post('/api/events/', payload, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data.get('status'), 'error')

    def test_send_evaluation_without_answers_returns_400(self):
        # create event
        event_id = self.create_event(name="Evento evaluación", admin_id=2)

        eval_payload = {
            'event_id': event_id,
            'evaluated_user_id': 10,
            'evaluator_user_id': 11,
            'type': '360',
            'answers': []
        }
        res2 = self.client.post('/api/evaluations/', eval_payload, format='json')
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res2.data.get('status'), 'error')

    def test_send_evaluation_with_invalid_event_returns_400(self):
        eval_payload = {
            'event_id': 9999,
            'evaluated_user_id': 10,
            'evaluator_user_id': 11,
            'type': '360',
            'answers': [
                {'criterion_id': 1, 'score': 3, 'comment': 'ok'},
            ]
        }
        res = self.client.post('/api/evaluations/', eval_payload, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data.get('status'), 'error')

    def test_get_evaluations_filtered_by_event(self):
        event_a = self.create_event(name="Evento A")
        event_b = self.create_event(name="Evento B", admin_id=2)

        eval_payload_a = {
            'event_id': event_a,
            'evaluated_user_id': 10,
            'evaluator_user_id': 11,
            'answers': [{'criterion_id': 1, 'score': 4, 'comment': 'bien'}],
        }
        eval_payload_b = {
            'event_id': event_b,
            'evaluated_user_id': 20,
            'evaluator_user_id': 21,
            'answers': [{'criterion_id': 1, 'score': 5, 'comment': 'excelente'}],
        }
        self.client.post('/api/evaluations/', eval_payload_a, format='json')
        self.client.post('/api/evaluations/', eval_payload_b, format='json')

        res = self.client.get(f'/api/evaluations/?event_id={event_a}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('status'), 'success')
        self.assertEqual(len(res.data['data']), 1)
        self.assertEqual(res.data['data'][0]['event_id'], event_a)

    def test_duplicate_evaluation_returns_400(self):
        event_id = self.create_event(name="Evento Único")
        eval_payload = {
            'event_id': event_id,
            'evaluated_user_id': 10,
            'evaluator_user_id': 11,
            'answers': [{'criterion_id': 1, 'score': 4, 'comment': 'bien'}],
        }
        res1 = self.client.post('/api/evaluations/', eval_payload, format='json')
        self.assertEqual(res1.status_code, 201)

        res2 = self.client.post('/api/evaluations/', eval_payload, format='json')
        self.assertEqual(res2.status_code, 400)
        self.assertEqual(res2.data.get('status'), 'error')

    def test_requests_without_auth_return_401(self):
        client = APIClient()
        res = client.get('/api/events/')
        self.assertEqual(res.status_code, 401)

    def test_intern_hours_endpoint_returns_data(self):
        InternHoursModel.objects.create(
            name="Test User",
            horas=10,
            horas_jul_oct=15,
            horas_acumuladas=25,
            horas_necesarias=480,
            horas_restantes_2212=30,
            falta_sobra=-455,
            faltaria_sobraria=-425,
            total=55,
            cumplimiento_pct=11,
        )
        res = self.client.get('/api/intern-hours/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('status'), 'success')
        self.assertGreaterEqual(len(res.data.get('data')), 1)
