import json, requests
from MidoWebLib import apis_url
from MidoWebLib import servergaps as gaps

class gaps_clinit: 
  def __init__(self, token):
    try:
      r = requests.get(f"{apis_url.API_TOKEN_Check}?access_token={token}")
      data = r.json() 
      ok_status = data.get('ok', None)
      if ok_status is None:
        raise ConnectionError("الموقع فاصل دلوقت، حاول لاحقًا.")
      if ok_status == "False":
        raise ValueError(data.get("message", "Check your token"))
      self.token = token
    except requests.exceptions.RequestException:
      raise ConnectionError("Server is down now... Try in another time.")

  def eand_alahly_hours(self, phone, email, password):
    if not all([phone, email, password]):
      return {'ok': 'False', 'message': 'All fields must be completed'}
    data = {
      'phone': phone,
      'email': email,
      'password': password,
      'access_token': self.token
    }
    status, d = gaps.eand_AlAhly_hours(number=data['phone'], password=data['password'], email=data['email'])
    try:
      if str(status) == 'True':
        requests.post(apis_url.approved_api, json={'token': self.token, 'system_token': '28572119:S645gWIMpvy21toMpcG3jIhmnV9szQ'})
      else:
        requests.post(apis_url.rejected_api, json={'token': self.token, 'system_token': '28572119:S645gWIMpvy21toMpcG3jIhmnV9szQ'})
      return {'ok': str(status), 'message': str(status)}
    except requests.exceptions.RequestException as e:
      return {'ok': 'False', 'message': f'Error: {str(e)}....'}
  
  def orange_500_mega(self, phone, password):
    if not all([phone, password]):
      return {'ok': 'False', 'message': 'All fields must be completed'}
    data = {
      'phone': phone,
      'password': password,
    }
    status, d = gaps.orange_500_mega(number=data['phone'], password=data['password'])
    try:
      if str(status) == 'True':
        requests.post(apis_url.approved_api, json={'token': self.token, 'system_token': '28572119:S645gWIMpvy21toMpcG3jIhmnV9szQ'})
      else:
        requests.post(apis_url.rejected_api, json={'token': self.token, 'system_token': '28572119:S645gWIMpvy21toMpcG3jIhmnV9szQ'})
      return {'ok': str(status), 'message': str(status)}
    except requests.exceptions.RequestException as e:
      return {'ok': 'False', 'message': f'Error: {str(e)}....'}
  
  def orange_luck_wheel(self, phone, password):
    if not all([phone, password]):
      return {'ok': 'False', 'message': 'All fields must be completed'}
    data = {
      'phone': phone,
      'password': password,
      'access_token': self.token
    }
    status, d = gaps.orange_wheel(number=data['phone'], password=data['password'])
    try:
      if str(status) == 'True':
        requests.post(apis_url.approved_api, json={'token': self.token, 'system_token': '28572119:S645gWIMpvy21toMpcG3jIhmnV9szQ'})
      else:
        requests.post(apis_url.rejected_api, json={'token': self.token, 'system_token': '28572119:S645gWIMpvy21toMpcG3jIhmnV9szQ'})
      return {'ok': str(status), 'message': str(status)}
    except requests.exceptions.RequestException as e:
      return {'ok': 'False', 'message': f'Error: {str(e)}'}
