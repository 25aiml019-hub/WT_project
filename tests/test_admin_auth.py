import urllib.request
import urllib.parse
import http.cookiejar
import json
import sys

BASE_URL = "http://localhost:8000"

def get_csrf(opener):
    req = urllib.request.Request(f"{BASE_URL}/csrf-token.php")
    with opener.open(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data['csrf_token']

print("=" * 70)
print("TESTING ADMIN AUTHENTICATION (admin123 vs 123)")
print("=" * 70)

# TEST 1: Old password '123' must FAIL
cj_old = http.cookiejar.CookieJar()
opener_old = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj_old))
csrf_old = get_csrf(opener_old)

login_data_old = urllib.parse.urlencode({
    "username": "admin",
    "password": "123",
    "csrf_token": csrf_old
}).encode('utf-8')

req_old = urllib.request.Request(
    f"{BASE_URL}/process-login.php",
    data=login_data_old,
    headers={"Accept": "application/json"}
)

try:
    with opener_old.open(req_old) as resp:
        res_old = json.loads(resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    res_old = json.loads(e.read().decode('utf-8'))
    assert e.code == 401, f"Expected 401 Unauthorized, got {e.code}"

print("Attempting admin login with old password '123':")
print(res_old)
assert res_old.get('success') is False, "FAILURE: Old password '123' was accepted!"
print(" [PASS] Old password '123' successfully REJECTED.")

# TEST 2: New password 'admin123' must SUCCEED
cj_new = http.cookiejar.CookieJar()
opener_new = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj_new))
csrf_new = get_csrf(opener_new)

login_data_new = urllib.parse.urlencode({
    "username": "admin",
    "password": "admin123",
    "csrf_token": csrf_new
}).encode('utf-8')

req_new = urllib.request.Request(
    f"{BASE_URL}/process-login.php",
    data=login_data_new,
    headers={"Accept": "application/json"}
)

with opener_new.open(req_new) as resp:
    res_new = json.loads(resp.read().decode('utf-8'))

print("\nAttempting admin login with new password 'admin123':")
print(res_new)
assert res_new.get('success') is True, "FAILURE: New password 'admin123' was rejected!"
assert res_new.get('role') == 'admin', "FAILURE: Role is not admin!"
assert 'admin' in res_new.get('redirect', ''), "FAILURE: Redirect path does not point to admin portal!"
print(" [PASS] New password 'admin123' successfully ACCEPTED and authenticated.")

# TEST 3: Access Admin Portal with authenticated session
req_admin_page = urllib.request.Request(f"{BASE_URL}/admin/index.php")
with opener_new.open(req_admin_page) as resp:
    admin_html = resp.read().decode('utf-8')

assert resp.status == 200, f"FAILURE: Admin portal returned HTTP {resp.status}"
assert "Administrator Portal" in admin_html or "Admin" in admin_html, "FAILURE: Admin portal title missing"
print(" [PASS] Authenticated admin session successfully accessed Admin Portal (HTTP 200).")

# TEST 4: Verify api/auth/me.php reports authenticated admin
req_me = urllib.request.Request(f"{BASE_URL}/api/auth/me.php")
with opener_new.open(req_me) as resp:
    me_data = json.loads(resp.read().decode('utf-8'))

assert me_data.get('authenticated') is True
assert me_data.get('user', {}).get('role') == 'admin'
assert me_data.get('user', {}).get('username') == 'admin'
print(" [PASS] /api/auth/me.php confirms identity: role='admin', username='admin'.")

# TEST 5: Verify student login still functions normally
cj_stu = http.cookiejar.CookieJar()
opener_stu = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj_stu))
csrf_stu = get_csrf(opener_stu)

login_data_stu = urllib.parse.urlencode({
    "username": "25AIML002",
    "password": "25AIML002",
    "csrf_token": csrf_stu
}).encode('utf-8')

req_stu = urllib.request.Request(
    f"{BASE_URL}/process-login.php",
    data=login_data_stu,
    headers={"Accept": "application/json"}
)

with opener_stu.open(req_stu) as resp:
    res_stu = json.loads(resp.read().decode('utf-8'))

assert res_stu.get('success') is True
assert res_stu.get('role') == 'student'
print(" [PASS] Student login with 25AIML002 remains fully operational.")

print("\n" + "=" * 70)
print("ALL ADMIN AUTHENTICATION TESTS PASSED!")
print("=" * 70)
