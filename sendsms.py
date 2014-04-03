#!/usr/bin/python

import logging
import sys

import getopt
import smpplib.gsm
import smpplib.client
import smpplib.consts
import MySQLdb

SMPPPORT = 2775
SMPPIP = '172.16.0.6'
SMPPSOURCEADDR = '33334'

SMPPTEXT = ''
SMPPDESTINATION = ''

def main(argv):
	try:
		opts,args = getopt.getopt(argv[1:], "ht:d:t",
		["text=", "destination="])
	except getopt.GetoptError:
		print('sendsms.py -t <Text> -d <destination>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('sendsms.py -t <Text> -d <destination>')
			sys.exit()
		elif opt in ("-t", "--text"):
			global SMPPTEXT
			SMPPTEXT=arg
			print(SMPPTEXT)
		elif opt in ("-d", "--destination"):
			global SMPPDESTINATION
			SMPPDESTINATION=arg
			print(SMPPDESTINATION)
			
	if (SMPPDESTINATION == ''):
		print('-d <Destination IP> is required')
		sys.exit()
	elif (SMPPTEXT == ''):
		print('-t <TEXT> is required')
		sys.exit()
	else:
		#logging.basicConfig(level='DEBUG')

		parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(SMPPTEXT)
		client = smpplib.client.Client(SMPPIP, SMPPPORT)

		# Print when obtain message_id
		client.set_message_sent_handler(
    			lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
		client.set_message_received_handler(
    			lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))
		try:
			client.connect()
			#client.bind_transmitter(system_id='alliance', password='Bank123asiA')
			client.bind_transceiver(system_id='aab', password='123Bank')
		except:
			print('Check IPSec Connection')
			sys.exit()
		for part in parts:
   			pdu = client.send_message(
        			source_addr_ton=0,
				#source_addr_ton=smpplib.consts.SMPP_TON_INTL,
        			source_addr_npi=1,
				#source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        			source_addr=SMPPSOURCEADDR,
        			dest_addr_ton=0,
				#dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
        			dest_addr_npi=0,
				#dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        			destination_addr=SMPPDESTINATION,
        			short_message=part,
        			data_coding=encoding_flag,
        			esm_class=msg_type_flag,
        			registered_delivery=False,
    			)
		print(pdu.sequence)
		#client.listen()
		client.unbind()
		client.disconnect()
if __name__ == '__main__':
	print(main(sys.argv))
