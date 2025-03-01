from unittest import TestCase
from ami_data_parser.parser.channel_parser import ChannelParser


class ChannelParserTestCase(TestCase):

    def test_get_data(self):
        received_data = ['Response: Success\r\n', 'ActionID: tatianno-ThinkPad-L470-00000001\r\n', 'Message: Command output follows\r\n', 'Output: SIP/IP-7436-QPQGE-00000002!C_1_ENT!997799298!1!Down!AppDial!(Outgoing Line)!997799298!3!3!3!2!!1740760337.2\r\n', 'Output: SIP/IP-101-Q14V2-00000001!macro-externa!s!22!Ring!Dial!SIP/IP-7436-QPQGE/997799298,90,TtM(saida_atendimento)!101!3!!3!2!!1740760337.1\r\n']
        expected_data = [
            {
                'channel': 'SIP/IP-7436-QPQGE-00000002',
                'context': 'C_1_ENT',
                'exten': '997799298',
                'priority': '1',
                'state': 'Down',
                'application': 'AppDial',
                'app_data': '(Outgoing Line)',
                'callerid_num': '997799298',
                'uniqueid': '1740760337.2'
            },
            {
                'channel': 'SIP/IP-101-Q14V2-00000001',
                'context': 'macro-externa',
                'exten': 's',
                'priority': '22',
                'state': 'Ring',
                'application': 'Dial',
                'app_data': 'SIP/IP-7436-QPQGE/997799298,90,TtM(saida_atendimento)',
                'callerid_num': '101',
                'uniqueid': '1740760337.1'
            }
        ]
        parser = ChannelParser()
        data = parser.get_data(received_data)
        self.assertListEqual(data, expected_data)
    
    def test_get_data_empty(self):
        received_data = ['Response: Success\r\n', 'ActionID: tatianno-ThinkPad-L470-0000000c\r\n', 'Message: Command output follows\r\n', 'Output: \r\n']
        expected_data = []
        parser = ChannelParser()
        data = parser.get_data(received_data)
        self.assertListEqual(data, expected_data)

    def test_get_parser_channel(self):
        received_data = 'Output: SIP/IP-7436-QPQGE-00000002!C_1_ENT!997799298!1!Down!AppDial!(Outgoing Line)!997799298!3!3!3!2!!1740760337.2\r\n'
        expected_data = {
            'channel': 'SIP/IP-7436-QPQGE-00000002',
            'context': 'C_1_ENT',
            'exten': '997799298',
            'priority': '1',
            'state': 'Down',
            'application': 'AppDial',
            'app_data': '(Outgoing Line)',
            'callerid_num': '997799298',
            'uniqueid': '1740760337.2'
        }
        parser = ChannelParser()
        data = parser._get_parser_channel(received_data)
        self.assertEqual(data, expected_data)

    def test_get_parse_channel_invalid_data(self):
        received_data = 'Response: Success\r\n'
        expected_data = None
        parser = ChannelParser()
        data = parser._get_parser_channel(received_data)
        self.assertEqual(data, expected_data)

    def test_get_channel(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = 'SIP/IP-7436-QPQGE-00000002'
        parser = ChannelParser()
        channel = parser._get_channel(received_data)
        self.assertEqual(channel, expected_data)
    
    def test_get_context(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = 'C_1_ENT'
        parser = ChannelParser()
        context = parser._get_context(received_data)
        self.assertEqual(context, expected_data)
    
    def test_get_exten(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = '997799298'
        parser = ChannelParser()
        exten = parser._get_exten(received_data)
        self.assertEqual(exten, expected_data)
    
    def test_get_priority(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = '1'
        parser = ChannelParser()
        priority = parser._get_priority(received_data)
        self.assertEqual(priority, expected_data)
    
    def test_get_state(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = 'Down'
        parser = ChannelParser()
        state = parser._get_state(received_data)
        self.assertEqual(state, expected_data)
    
    def test_get_application(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = 'AppDial'
        parser = ChannelParser()
        application = parser._get_application(received_data)
        self.assertEqual(application, expected_data)
    
    def test_get_app_data(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = '(Outgoing Line)'
        parser = ChannelParser()
        app_data = parser._get_app_data(received_data)
        self.assertEqual(app_data, expected_data)
    
    def test_get_callerid_num(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = '997799298'
        parser = ChannelParser()
        callerid_num = parser._get_callerid_num(received_data)
        self.assertEqual(callerid_num, expected_data)
    
    def test_get_uniqueid(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = '1740760337.2'
        parser = ChannelParser()
        callerid_num = parser._get_uniqueid(received_data)
        self.assertEqual(callerid_num, expected_data)
    
    def test_get_uniqueid_raise_except_index_error(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298']
        expected_data = None
        parser = ChannelParser()
        callerid_num = parser._get_uniqueid(received_data)
        self.assertEqual(callerid_num, expected_data)
    
    def test_get_data_list(self):
        received_data = 'Output: SIP/IP-7436-QPQGE-00000002!C_1_ENT!997799298!1!Down!AppDial!(Outgoing Line)!997799298!3!3!3!2!!1740760337.2\r\n'
        expected_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        parser = ChannelParser()
        data_list = parser._get_data_list(received_data)
        self.assertListEqual(data_list, expected_data)
    
    def test_clean_data(self):
        received_data = 'Output: SIP/IP-7436-QPQGE-00000002!C_1_ENT!997799298!1!Down!AppDial!(Outgoing Line)!997799298!3!3!3!2!!1740760337.2\r\n'
        expected_data = 'SIP/IP-7436-QPQGE-00000002!C_1_ENT!997799298!1!Down!AppDial!(Outgoing Line)!997799298!3!3!3!2!!1740760337.2'
        parser = ChannelParser()
        data = parser._clean_data(received_data)
        self.assertEqual(data, expected_data)
    
    def test_get_value_in_list(self):
        received_data = ['SIP/IP-7436-QPQGE-00000002','C_1_ENT','997799298','1','Down','AppDial','(Outgoing Line)','997799298','3','3','3','2','','1740760337.2']
        expected_data = 'Down'
        parser = ChannelParser()
        data = parser._get_value_in_list(received_data, 4)
        self.assertEqual(data, expected_data)
        expected_data = None
        data = parser._get_value_in_list(received_data, 15)
        self.assertEqual(data, expected_data)
        