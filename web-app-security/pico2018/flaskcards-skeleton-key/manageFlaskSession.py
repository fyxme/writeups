#!/usr/bin/env python
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer

class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
	# Override method
	# Take secret_key instead of an instance of a Flask app
	def get_signing_serializer(self, secret_key):
		if not secret_key:
			return None
		signer_kwargs = dict(
			key_derivation=self.key_derivation,
			digest_method=self.digest_method
		)
		return URLSafeTimedSerializer(secret_key, salt=self.salt,
		                              serializer=self.serializer,
		                              signer_kwargs=signer_kwargs)

def decodeFlaskCookie(secret_key, cookieValue):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.loads(cookieValue)

# Keep in mind that flask uses unicode strings for the
# dictionary keys
def encodeFlaskCookie(secret_key, cookieDict):
	sscsi = SimpleSecureCookieSessionInterface()
	signingSerializer = sscsi.get_signing_serializer(secret_key)
	return signingSerializer.dumps(cookieDict)

if __name__=='__main__':
	sk = '385c16dd09098b011d0086f9e218a0a2'
        sessionDict = {u'csrf_token': u'ddaac0bbce2b6ba7231e852d9569440aa2996f91', u'_fresh': True, u'user_id': u'1', u'_id': u'7a5c0ca28360e58c4f23b8170de6971beef61e0b5106c2dc166d94653ada5894fe155662eb59544abcbac5f09b6ad217cfa8586e2df24e1dc6c2920129612d56'}
	cookie = encodeFlaskCookie(sk, sessionDict)
        print cookie


        ecookie = ".eJwlj1tqAzEMAO_i73xIWku2cplFL9MQaGE3-Sq9exZ6gBlmftu-jjq_2v11vOvW9ke2exvGAWE0N4HiGX3R5hMHZIkO9KolWOCMIEEZKJLahTdL46l9FTKLUDkr924ebsEL1MWScMSyyVOKclEvzLgsSoCkgpQs7dbiPNb--nnW99WTaRbgHkUuboM2rMmUyqK9gxmpylK8uPdZx_8EtL8Pxj8_Og.DprhmQ.gK9viwxBEP51WwGSXHwsnCal0kQ"

        decodedDict = decodeFlaskCookie(sk, ecookie)
        print decodedDict
