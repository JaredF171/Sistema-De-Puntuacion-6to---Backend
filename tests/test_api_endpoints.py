from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
import datetime


class ApiIntegrationTests(APITestCase):
    def test_create_event_and_list(self):
        url = '/api/events/'
        now = timezone.now()
        payload = {
            'name': 'Evento de prueba',
            'description': 'Descripción',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=1)).isoformat(),
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
        now = timezone.now()
        event_payload = {
            'name': 'Evento evaluación',
            'description': '',
            'start_date': now.isoformat(),
            'end_date': (now + datetime.timedelta(days=1)).isoformat(),
            'admin_id': 2,
        }
        res = self.client.post('/api/events/', event_payload, format='json')
        self.assertEqual(res.status_code, 201)
        event_id = res.data['data']['id']

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
