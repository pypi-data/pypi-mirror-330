from unittest import TestCase
from ami_data_parser.parser.queue_parser import QueueParser


class QueueParserTestCase(TestCase):

    def test_get_data(self):
        received_data = ['Response: Success\r\n', 'ActionID: server-00000002\r\n', 'Message: Command output follows\r\n', "Output: Queue_11 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2930362 secs ago) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101 (ringinuse disabled) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_27 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_44 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-boazN (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101-Iathq (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_47 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', 'Output: \r\n']
        expect_data = [{'members': [{'name': 'SIP/IP-100-CdFaT', 'has_paused': True, 'paused_time': 2930362, 'logged_time': 2930362, 'total_calls': 0, 'last_call_time': 0}, {'name': 'SIP/IP-101', 'has_paused': False, 'paused_time': 0, 'logged_time': 2930362, 'total_calls': 0, 'last_call_time': 0}], 'waiting_calls': [], 'queuename': 'Queue_11', 'total_calls': 0, 'strategy': 'rrmemory', 'wait_mean': 0, 'duration_mean': 0, 'total_wait_calls': 0, 'total_completed_calls': 0, 'total_abandoned_calls': 0}, {'members': [], 'waiting_calls': [], 'queuename': 'Queue_27', 'total_calls': 0, 'strategy': 'rrmemory', 'wait_mean': 0, 'duration_mean': 0, 'total_wait_calls': 0, 'total_completed_calls': 0, 'total_abandoned_calls': 0}, {'members': [{'name': 'SIP/IP-100-boazN', 'has_paused': False, 'paused_time': 0, 'logged_time': 2930362, 'total_calls': 0, 'last_call_time': 0}, {'name': 'SIP/IP-101-Iathq', 'has_paused': False, 'paused_time': 0, 'logged_time': 2930362, 'total_calls': 0, 'last_call_time': 0}], 'waiting_calls': [], 'queuename': 'Queue_44', 'total_calls': 0, 'strategy': 'rrmemory', 'wait_mean': 0, 'duration_mean': 0, 'total_wait_calls': 0, 'total_completed_calls': 0, 'total_abandoned_calls': 0}, {'members': [], 'waiting_calls': [], 'queuename': 'Queue_47', 'total_calls': 0, 'strategy': 'rrmemory', 'wait_mean': 0, 'duration_mean': 0, 'total_wait_calls': 0, 'total_completed_calls': 0, 'total_abandoned_calls': 0}]
        queue_parser = QueueParser()
        data = queue_parser.get_data(received_data)
        self.assertListEqual(data, expect_data)
    
    def test_get_data_without_queue(self):
        received_data = ['Response: Success\r\n', 'ActionID: tatianno-ThinkPad-L470-00000003\r\n', 'Message: Command output follows\r\n', 'Output: No queues.\r\n']
        expect_data = []
        queue_parser = QueueParser()
        data = queue_parser.get_data(received_data)
        self.assertListEqual(data, expect_data)
        
    def test_get_list_queue_lines(self):
        received_data = ['Response: Success\r\n', 'ActionID: server-00000002\r\n', 'Message: Command output follows\r\n', "Output: Queue_11 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2930362 secs ago) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101 (ringinuse disabled) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_27 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_44 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-boazN (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101-Iathq (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', "Output: Queue_47 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', 'Output: \r\n']
        expect_data = [["Output: Queue_11 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2930362 secs ago) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101 (ringinuse disabled) (Not in use) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n'], ["Output: Queue_27 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n'], ["Output: Queue_44 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    Members: \r\n', 'Output:       SIP/IP-100-boazN (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:       SIP/IP-101-Iathq (ringinuse disabled) (Unavailable) has taken no calls yet (login was 2930362 secs ago)\r\n', 'Output:    No Callers\r\n', 'Output: \r\n'], ["Output: Queue_47 has 0 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s\r\n", 'Output:    No Members\r\n', 'Output:    No Callers\r\n', 'Output: \r\n', 'Output: \r\n']]
        queue_parser = QueueParser()
        data = queue_parser._get_list_queue_lines(received_data)
        self.assertListEqual(data, expect_data)

    def test_get_parser_queue_with_callers(self):
        received_data = '''Queue_1088 has 5 calls (max unlimited) in 'rrmemory' strategy (348s holdtime, 304s talktime), W:10, C:43, A:11, SL:0.0% within 0s
   Members: 
      SIP/IP1489 (ringinuse disabled) (in call) (In use) has taken 3 calls (last was 1912 secs ago)
      SIP/IP1492 (ringinuse disabled) (Unavailable) has taken no calls yet
      SIP/IP1107 (ringinuse disabled) (paused) (Not in use) has taken 4 calls (last was 1386 secs ago)

   Callers: 
      1. IAX2/SERVER_2-13471 (wait: 8:25, prio: 0)
      2. IAX2/SERVER_2-9969 (wait: 0:29, prio: 0)'''
        received_data = received_data.split('\n')
        expect_data = {
            'queuename': 'Queue_1088',
            'total_calls': 5,
            'strategy': 'rrmemory',
            'wait_mean': 348,
            'duration_mean': 304,
            'total_wait_calls': 10,
            'total_completed_calls': 43,
            'total_abandoned_calls': 11,
            'members': [
                {
                    'name': 'SIP/IP1489',
                    'has_paused': False,
                    'paused_time': 0,
                    'logged_time': 0,
                    'total_calls': 3,
                    'last_call_time': 1912
                },
                {
                    'name': 'SIP/IP1492',
                    'has_paused': False,
                    'paused_time': 0,
                    'logged_time': 0,
                    'total_calls': 0,
                    'last_call_time': 0
                },
                {
                    'name': 'SIP/IP1107',
                    'has_paused': True,
                    'paused_time': 0,
                    'logged_time': 0,
                    'total_calls': 4,
                    'last_call_time': 1386
                },
            ],
            'waiting_calls': [
                {
                    'channel': 'IAX2/SERVER_2-13471',
                    'position': 1,
                    'wait_time': 505,
                    'priority': 0
                },
                {
                    'channel': 'IAX2/SERVER_2-9969',
                    'position': 2,
                    'wait_time': 29,
                    'priority': 0
                }
            ]
        }
        parser = QueueParser()
        data = parser._get_parser_queue(received_data)
        self.assertDictEqual(data, expect_data)
    
    def test_get_parser_queue_without_callers(self):
        received_data = '''Queue_1088 has 5 calls (max unlimited) in 'rrmemory' strategy (348s holdtime, 304s talktime), W:10, C:43, A:11, SL:0.0% within 0s
   Members: 
      SIP/IP1489 (ringinuse disabled) (in call) (In use) has taken 3 calls (last was 1912 secs ago)
      SIP/IP1492 (ringinuse disabled) (Unavailable) has taken no calls yet
      SIP/IP1107 (ringinuse disabled) (paused) (Not in use) has taken 4 calls (last was 1386 secs ago)
   No Callers'''
        received_data = received_data.split('\n')
        expect_data = {
            'queuename': 'Queue_1088',
            'total_calls': 5,
            'strategy': 'rrmemory',
            'wait_mean': 348,
            'duration_mean': 304,
            'total_wait_calls': 10,
            'total_completed_calls': 43,
            'total_abandoned_calls': 11,
            'members': [
                {
                    'name': 'SIP/IP1489',
                    'has_paused': False,
                    'paused_time': 0,
                    'logged_time': 0,
                    'total_calls': 3,
                    'last_call_time': 1912
                },
                {
                    'name': 'SIP/IP1492',
                    'has_paused': False,
                    'paused_time': 0,
                    'logged_time': 0,
                    'total_calls': 0,
                    'last_call_time': 0
                },
                {
                    'name': 'SIP/IP1107',
                    'has_paused': True,
                    'paused_time': 0,
                    'logged_time': 0,
                    'total_calls': 4,
                    'last_call_time': 1386
                },
            ],
            'waiting_calls': []
        }
        parser = QueueParser()
        data = parser._get_parser_queue(received_data)
        self.assertDictEqual(data, expect_data)

    def test_get_data_queue(self):
        received_line = "Output: Queue_11 has 3 calls (max unlimited) in 'rrmemory' strategy (10s holdtime, 230s talktime), W:1, C:130, A:5, SL:0.0%, SL2:0.0% within 0s"
        parser = QueueParser()
        data = parser._get_data_queue(received_line)
        expect_data = {
            'queuename': 'Queue_11',
            'total_calls': 3,
            'strategy': 'rrmemory',
            'wait_mean': 10,
            'duration_mean': 230,
            'total_wait_calls': 1,
            'total_completed_calls': 130,
            'total_abandoned_calls': 5
        }
        self.assertDictEqual(data, expect_data)

    def test_get_data_member(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2507382 secs ago) (In use) has taken 1 calls (last was 628 secs ago) (login was 3507382 secs ago)'
        parser = QueueParser()
        data = parser._get_data_member(received_line)
        expect_data = {
            'name': 'SIP/IP-100-CdFaT',
            'has_paused': True,
            'paused_time': 2507382,
            'logged_time': 3507382,
            'total_calls': 1,
            'last_call_time': 628
        }
        self.assertDictEqual(data, expect_data)
    
    def test_get_data_channel(self):
        received_line = 'Output:       1. IAX2/SERVER_2-13471 (wait: 8:25, prio: 0)'
        parser = QueueParser()
        data = parser._get_data_channel(received_line)
        expect_data = {
            'channel': 'IAX2/SERVER_2-13471',
            'position': 1,
            'wait_time': 505,
            'priority': 0
        }
        self.assertDictEqual(data, expect_data)
    
    def test_get_queuename(self):
        received_line = "Output: Queue_11 has 1 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s"
        parser = QueueParser()
        queuename = parser._get_queuename(received_line)
        self.assertEqual(queuename, 'Queue_11')
    
    def test_get_total_calls(self):
        received_line = "Output: Queue_11 has 1 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s"
        parser = QueueParser()
        quantidade_chamadas_totais = parser._get_total_calls(received_line)
        self.assertEqual(quantidade_chamadas_totais, 1)
    
    def test_get_strategy(self):
        received_line = "Output: Queue_11 has 1 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s"
        parser = QueueParser()
        strategy = parser._get_strategy(received_line)
        self.assertEqual(strategy, 'rrmemory')
    
    def test_get_wait_mean(self):
        received_line = "Output: Queue_11 has 1 calls (max unlimited) in 'rrmemory' strategy (120s holdtime, 0s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s"
        parser = QueueParser()
        wait_mean = parser._get_wait_mean(received_line)
        self.assertEqual(wait_mean, 120)
    
    def test_get_duration_mean(self):
        received_line = "Output: Queue_11 has 1 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 90s talktime), W:0, C:0, A:0, SL:0.0%, SL2:0.0% within 0s"
        parser = QueueParser()
        duration_mean = parser._get_duration_mean(received_line)
        self.assertEqual(duration_mean, 90)

    def test_get_total_wait_calls(self):
        received_line = "Output: Queue_11 has 1 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:2, C:0, A:0, SL:0.0%, SL2:0.0% within 0s"
        parser = QueueParser()
        total_wait_calls = parser._get_total_wait_calls(received_line)
        self.assertEqual(total_wait_calls, 2)
    
    def test_get_total_completed_calls(self):
        received_line = "Output: Queue_11 has 1 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:2, C:5, A:0, SL:0.0%, SL2:0.0% within 0s"
        parser = QueueParser()
        total_completed_calls = parser._get_total_completed_calls(received_line)
        self.assertEqual(total_completed_calls, 5)
    
    def test_get_total_abandoned_calls(self):
        received_line = "Output: Queue_11 has 1 calls (max unlimited) in 'rrmemory' strategy (0s holdtime, 0s talktime), W:2, C:5, A:3, SL:0.0%, SL2:0.0% within 0s"
        parser = QueueParser()
        total_abandoned_calls = parser._get_total_abandoned_calls(received_line)
        self.assertEqual(total_abandoned_calls, 3)
    
    def test_get_queue_member(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2507382 secs ago) (In use) has taken no calls yet (login was 2507382 secs ago)'
        parser = QueueParser()
        queue_member = parser._get_member_name(received_line)
        self.assertEqual(queue_member, 'SIP/IP-100-CdFaT')

    def test_get_member_has_paused(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2507382 secs ago) (In use) has taken no calls yet (login was 2507382 secs ago)'
        parser = QueueParser()
        has_paused = parser._get_member_has_paused(received_line)
        self.assertTrue(has_paused)
    
    def test_get_member_has_paused(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (In use) has taken no calls yet (login was 2507382 secs ago)'
        parser = QueueParser()
        has_paused = parser._get_member_has_paused(received_line)
        self.assertFalse(has_paused)
    
    def test_get_member_paused(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2507382 secs ago) (In use) has taken no calls yet (login was 2507382 secs ago)'
        parser = QueueParser()
        paused_time = parser._get_member_paused(received_line)
        self.assertEqual(paused_time, 2507382)
    
    def test_get_member_not_paused(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (In use) has taken no calls yet (login was 2507382 secs ago)'
        parser = QueueParser()
        paused_time = parser._get_member_paused(received_line)
        self.assertEqual(paused_time, 0)

    def test_get_member_logged(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (In use) has taken no calls yet (login was 2507400 secs ago)'
        parser = QueueParser()
        logged_time = parser._get_member_logged(received_line)
        self.assertEqual(logged_time, 2507400)
    
    def test_get_member_not_logged(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (In use) has taken no calls yet'
        parser = QueueParser()
        logged_time = parser._get_member_logged(received_line)
        self.assertEqual(logged_time, 0)

    def test_get_member_paused_logged(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (paused was 2507382 secs ago) (In use) has taken no calls yet (login was 2507400 secs ago)'
        parser = QueueParser()
        logged_time = parser._get_member_logged(received_line)
        self.assertEqual(logged_time, 2507400)

    def test_get_member_calls(self):
        received_line = 'Output:       SIP/IP1489 (ringinuse disabled) (In use) has taken 1 calls (last was 628 secs ago)'
        parser = QueueParser()
        total_calls = parser._get_member_calls(received_line)
        self.assertEqual(total_calls, 1)
    
    def test_get_member_no_calls(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (In use) has taken no calls yet (login was 2507400 secs ago)'
        parser = QueueParser()
        total_calls = parser._get_member_calls(received_line)
        self.assertEqual(total_calls, 0)
    
    def test_get_member_last_call(self):
        received_line = 'Output:       SIP/IP1489 (ringinuse disabled) (In use) has taken 1 calls (last was 628 secs ago)'
        parser = QueueParser()
        last_call_time = parser._get_member_last_call(received_line)
        self.assertEqual(last_call_time, 628)
    
    def test_get_member_no_last_call(self):
        received_line = 'Output:       SIP/IP-100-CdFaT (ringinuse disabled) (In use) has taken no calls yet (login was 2507400 secs ago)'
        parser = QueueParser()
        total_calls = parser._get_member_last_call(received_line)
        self.assertEqual(total_calls, 0)
    
    def test_get_call_position(self):
        received_line = 'Output:       1. IAX2/SERVER_2-13471 (wait: 8:25, prio: 0)'
        parser = QueueParser()
        total_calls = parser._get_call_position(received_line)
        self.assertEqual(total_calls, 1)

    def test_get_call_channel(self):
        received_line = 'Output:       1. IAX2/SERVER_2-13471 (wait: 8:25, prio: 1)'
        parser = QueueParser()
        call_channel = parser._get_call_channel(received_line)
        self.assertEqual(call_channel, 'IAX2/SERVER_2-13471')
    
    def test_get_call_wait(self):
        received_line = 'Output:       1. IAX2/SERVER_2-13471 (wait: 8:25, prio: 0)'
        parser = QueueParser()
        total_calls = parser._get_call_wait(received_line)
        self.assertEqual(total_calls, 505)
    
    def test_get_call_priority(self):
        received_line = 'Output:       1. IAX2/SERVER_2-13471 (wait: 8:25, prio: 1)'
        parser = QueueParser()
        total_calls = parser._get_call_priority(received_line)
        self.assertEqual(total_calls, 1)