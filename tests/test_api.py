import unittest
import app

class TestJanDrishtiAPI(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        app.init_db()

    def test_get_stats(self):
        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('total', data['stats'])

    def test_get_issues(self):
        response = self.client.get('/api/issues')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)

    def test_create_issue(self):
        payload = {
            'title': 'Test Hazard',
            'description': 'Automated test issue description',
            'category': 'Roads & Infrastructure',
            'severity': 'Medium',
            'location_name': 'Test Ward',
            'latitude': 12.9716,
            'longitude': 77.5946
        }
        response = self.client.post('/api/issues', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.get_json()['success'])

if __name__ == '__main__':
    unittest.main()
