# -*- coding: utf-8 -*-

import requests
import hashlib


class EuroSms(object):
    def __init__(self, id, key, requests=requests,
                 target_url='http://as.eurosms.com/sms/Sender'):
        self._requests = requests
        self._target_url = target_url
        self._id = id
        self._key = key

    def _send_payload(self, sender, receiver_phone, message):
        return {
            'msg':message,
            'number':receiver_phone,
            'sender':sender,
            'i':self._id,
            's':sign_sms(self._key, receiver_phone),
            'action':'send1SMSHTTP'
        }

    def send(self, sender, receiver_phone, message):
        payload = self._send_payload(sender, receiver_phone, message)
        response = self._requests.get(self._target_url, params=payload)

        if not '|' in response.content:
            raise Exception(
                'Invalid response from EuroSMS: %r' % repr(response.content)
            )

        status, message_id = response.content.split('|', 1)

        if status.strip() != 'ok':
            raise Exception(
                'Error during sending SMS, status code: %r, params: %r'
                % (status, payload)
            )

        return message_id.strip()

    def validate(self, message_id):
        params = {'action':'status1SMSHTTP','id':str(message_id)}
        response = self._requests.get(self._target_url, params=params)

        if not '|' in response.content:
            raise Exception(
                'Invalid response from EuroSMS: %r' % repr(response.content)
            )

        status, message_status = response.content.split('|', 1)

        if status.strip() != 'ok':
            raise Exception(
                'Error during validating SMS, status code: %r, params: %r' % (
                    status, params))

        return _get_delivery_status(message_status.strip())


STATUS_OK = 'ok'
STATUS_WAITING='waiting'
STATUS_ERROR='error'


class MessageDeliveryStatus(object):
    def __init__(self, code, description, status=STATUS_ERROR):
        self.code = code
        self.description = description
        self.status = status

    @property
    def is_error(self):
        return self.status == STATUS_ERROR

    def __unicode__(self):
        return self.description

    def __repr__(self):
        return '<DeliveryStatus %s, %s>' % (self.code, self.status)


DELIVERY_STATUS = {a.code:a for a in [
    MessageDeliveryStatus('-1', u'Doručenka čaká na spracovanie – doručovací systém neposlal potvrdenie o doručení.', STATUS_WAITING),
    MessageDeliveryStatus('0', u'Doručenie zatiaľ neoverené – doručovací systém spracoval sms a nemá potvrdenie o doručení.', STATUS_WAITING),
    MessageDeliveryStatus('1', u'Doručená na cieľový telefón.', STATUS_OK),
    MessageDeliveryStatus('2', u'Chybné / neexistujúce / nepoužívané tel.číslo.', STATUS_ERROR),
    MessageDeliveryStatus('3', u'SMS nedoručená.Telefón prijímateľa nedostupný.', STATUS_ERROR),
    MessageDeliveryStatus('4', u'SMS v procese doručovania.', STATUS_WAITING),
    MessageDeliveryStatus('5', u'Prekročený čas.', STATUS_ERROR),
    MessageDeliveryStatus('ERROR100', u'Chyba SMS centra.Zopakovať poslanie.', STATUS_ERROR),
    MessageDeliveryStatus('ERROR101', u'Nesprávne formátovaná požiadavka.', STATUS_ERROR),
    MessageDeliveryStatus('ERROR102', u'Nesprávny dotaz na doručenku.', STATUS_ERROR),
    MessageDeliveryStatus('NOT_ALLOWED', u'Nemáte oprávnenie posielať do tejto siete', STATUS_ERROR),
    MessageDeliveryStatus('SENT', u'Správa poslaná cez SMSC nepodporujúce doručenky.', STATUS_ERROR),
    MessageDeliveryStatus('NOT_ENOUGH_CREDITS', u'Nedostatok prostriedkov na účte', STATUS_ERROR),
    MessageDeliveryStatus('INVALID_SOURCE_ADDRESS', u'Nesprávny odosieľateľ', STATUS_ERROR),
    MessageDeliveryStatus('ROUTE_NOT_AVAILABLE', u'Nepovolený routing', STATUS_ERROR),
    MessageDeliveryStatus('REJECTED_BY_ SMSC',u'SMS odmietnutá v SMSC.', STATUS_ERROR),
    MessageDeliveryStatus('UNKNOWN_SMSC_ERROR', u'Neznámy status SMS (SMSC vrátilo neznámu chybu).', STATUS_ERROR),
    MessageDeliveryStatus('21', u'Doručené sieti, čaká sa na telefón.', STATUS_WAITING),
    MessageDeliveryStatus('30', u'Chýbajúci routing / povolenie na SMSC.', STATUS_ERROR),
    MessageDeliveryStatus('41', u'Chybná SMS.', STATUS_ERROR),
]}


def _get_delivery_status(code):
    return DELIVERY_STATUS.get(code)


def sign_sms(key, phone_number):
    return hashlib.md5(key + phone_number).hexdigest()[10:10 + 11]

