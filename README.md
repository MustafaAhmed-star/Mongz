# Mongz Marketplace — API Documentation

**Base URL:** `https://yourdomain.com/api`  
**Auth:** Bearer JWT — add `Authorization: Bearer <access_token>` to every protected request  
**Content-Type:** `application/json`

---

## Authentication

### Register
`POST /api/auth/register/`  
**Auth:** None

**Request**
```json
{
  "username": "ahmed",
  "phone": "01012345678",
  "address": "Cairo, Egypt",
  "password": "mypassword",
  "role": "client"
}
```
`role` must be `"client"` or `"worker"`.

**Response 201**
```json
{
  "message": "Account created successfully.",
  "user": {
    "id": 1,
    "username": "ahmed",
    "phone": "01012345678",
    "address": "Cairo, Egypt",
    "role": "client",
    "date_joined": "2024-01-15T10:00:00Z"
  },
  "tokens": {
    "access": "eyJ0eX...",
    "refresh": "eyJ0eX..."
  }
}
```

**Errors**
| Code | Reason |
|------|--------|
| 400  | Username/phone already exists, password too short, role=admin |

---

### Login
`POST /api/auth/login/`  
**Auth:** None

**Request**
```json
{
  "username": "ahmed",
  "password": "mypassword"
}
```

**Response 200**
```json
{
  "message": "Login successful.",
  "user": { "id": 1, "username": "ahmed", "role": "client", ... },
  "tokens": {
    "access": "eyJ0eX...",
    "refresh": "eyJ0eX..."
  }
}
```

**Errors**
| Code | Reason |
|------|--------|
| 400  | Wrong credentials or disabled account |

---

### Refresh Token
`POST /api/auth/token/refresh/`  
**Auth:** None

**Request**
```json
{ "refresh": "eyJ0eX..." }
```

**Response 200**
```json
{ "access": "eyJ0eX...new" }
```

---

## User Profile

### Get My Profile
`GET /api/users/me/`  
**Auth:** Required

**Response 200**
```json
{
  "id": 1,
  "username": "ahmed",
  "phone": "01012345678",
  "address": "Cairo, Egypt",
  "role": "client",
  "date_joined": "2024-01-15T10:00:00Z"
}
```

---

### Update My Profile
`PATCH /api/users/me/`  
**Auth:** Required

**Request** *(all fields optional)*
```json
{
  "username": "ahmed_new",
  "phone": "01099999999",
  "address": "Alexandria, Egypt"
}
```

**Response 200** — updated user object

---

## Service Categories

### List Categories
`GET /api/categories/`  
**Auth:** None

**Response 200**
```json
[
  { "id": 1, "name": "Plumbing" },
  { "id": 2, "name": "Electrical" },
  { "id": 3, "name": "Painting" }
]
```

---

### Create Category
`POST /api/categories/create/`  
**Auth:** Required — Admin only

**Request**
```json
{ "name": "Carpentry" }
```

**Response 201**
```json
{ "id": 4, "name": "Carpentry" }
```

**Errors**
| Code | Reason |
|------|--------|
| 403  | Not an admin |
| 400  | Category name already exists |

---

## Workers

### List Workers
`GET /api/workers/`  
**Auth:** None

**Query Parameters**
| Param | Type | Description |
|-------|------|-------------|
| `category` | integer | Filter by category ID |
| `search` | string | Partial match on profession |
| `page` | integer | Page number (default 1) |
| `page_size` | integer | Results per page (default 10, max 50) |

**Examples**
```
GET /api/workers/                         → all workers sorted by score
GET /api/workers/?category=1              → plumbers only, sorted by score
GET /api/workers/?search=elec             → electricians
GET /api/workers/?category=1&page=2       → page 2 of plumbers
GET /api/workers/?category=1&page_size=5  → 5 per page
```

**Response 200**
```json
{
  "count": 12,
  "next": "http://api/workers/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "username": "worker1",
        "phone": "01011111111",
        "address": "Cairo",
        "role": "worker",
        "date_joined": "2024-01-10T00:00:00Z"
      },
      "profession": "Plumbing",
      "experience_years": 5,
      "average_rating": 4.5,
      "completed_jobs": 20,
      "is_available": true,
      "score": 10.7,
      "created_at": "2024-01-10T00:00:00Z"
    }
  ]
}
```

**Score Formula**  
`score = (average_rating × 0.6) + (completed_jobs × 0.4)`  
Results are sorted by score descending (best workers first).

---

### Create Worker Profile
`POST /api/workers/create/`  
**Auth:** Required — Worker role only

**Request**
```json
{
  "profession": "Plumbing",
  "experience_years": 5,
  "is_available": true
}
```

**Response 201** — full WorkerProfile object

**Errors**
| Code | Reason |
|------|--------|
| 403  | Not a worker |
| 400  | Worker already has a profile |

---

### Get Worker Profile
`GET /api/workers/<id>/`  
**Auth:** None

**Response 200** — WorkerProfile object

---

### My Worker Profile
`GET /api/workers/me/`  
**Auth:** Required — Worker only  
`PATCH /api/workers/me/`  
**Auth:** Required — Worker only

**PATCH Request** *(all fields optional)*
```json
{
  "profession": "Plumbing",
  "experience_years": 6,
  "is_available": false
}
```

---

## Orders

### List My Orders
`GET /api/orders/`  
**Auth:** Required

Returns orders filtered by the caller's role:
- **Client** → sees their own orders
- **Worker** → sees orders assigned to them
- **Admin** → sees all orders

**Response 200**
```json
[
  {
    "id": 1,
    "client": { "id": 1, "username": "ahmed", "role": "client", ... },
    "worker": { "id": 2, "username": "worker1", "role": "worker", ... },
    "service_category": { "id": 1, "name": "Plumbing" },
    "commission": "20.00",
    "status": "PENDING",
    "created_at": "2024-01-15T10:00:00Z",
    "accepted_at": null,
    "completed_at": null,
    "cancelled_at": null,
    "commission_payment": {
      "amount": "20.00",
      "payment_status": "AUTHORIZED",
      "paymob_order_id": "12345",
      "paymob_transaction_id": ""
    }
  }
]
```

---

### Create Order
`POST /api/orders/`  
**Auth:** Required — Client only

**Request**
```json
{
  "service_category": 1,
  "worker_id": 2
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `service_category` | ✅ Yes | ID of the service category |
| `worker_id` | ❌ No | ID of a chosen worker. If omitted, order created without worker |

**Validation when `worker_id` is provided:**
- Worker must have a profile
- Worker must be available (`is_available = true`)
- Worker's profession must match the service category name

**Response 201**
```json
{
  "id": 5,
  "client": { ... },
  "worker": { ... },
  "service_category": { "id": 1, "name": "Plumbing" },
  "commission": "0.00",
  "status": "PENDING",
  "created_at": "2024-01-15T10:05:00Z",
  "accepted_at": null,
  "completed_at": null,
  "cancelled_at": null,
  "commission_payment": {
    "amount": "20.00",
    "payment_status": "AUTHORIZED",
    "paymob_order_id": "PAY_789",
    "paymob_transaction_id": ""
  },
  "payment_key": "ZXlKaGJHY2..."
}
```

> **`payment_key`** — use this to render the Paymob iframe so the client can enter card details.  
> It is `null` if Paymob authorization failed (order is still created).

**Errors**
| Code | Reason |
|------|--------|
| 403  | Not a client |
| 400  | Invalid category, worker not available, profession mismatch |

---

### Get Order Detail
`GET /api/orders/<id>/`  
**Auth:** Required — Owner (client or worker) or Admin

**Response 200** — full Order object (same shape as above)

---

### Accept Order
`POST /api/orders/<id>/accept/`  
**Auth:** Required — Worker only

**No request body needed.**

**What happens:**
1. Order status → `ACCEPTED`
2. `accepted_at` timestamp set
3. `commission` = `settings.COMMISSION_AMOUNT`
4. Paymob commission captured (charged from card)
5. Client notified with PUSH notification

**Response 200** — updated Order object

**Errors**
| Code | Reason |
|------|--------|
| 403  | Not a worker |
| 404  | Order not found |
| 400  | Order is not in PENDING status |

---

### Reject Order
`POST /api/orders/<id>/reject/`  
**Auth:** Required — Worker only

**What happens:**
1. Order status → `REJECTED`
2. `cancelled_at` timestamp set
3. Paymob authorization voided (card hold released)
4. Client notified

**Response 200** — updated Order object

---

### Cancel Order
`POST /api/orders/<id>/cancel/`  
**Auth:** Required — Client only

**What happens:**
1. Order status → `CANCELLED`
2. `cancelled_at` timestamp set
3. Paymob authorization voided if status was `AUTHORIZED`
4. Worker notified (if one was assigned)

**Response 200** — updated Order object

**Errors**
| Code | Reason |
|------|--------|
| 400  | Order is not in PENDING status |

---

### Complete Order
`POST /api/orders/<id>/complete/`  
**Auth:** Required — Worker only (must be the assigned worker)

**What happens:**
1. Order status → `COMPLETED`
2. `completed_at` timestamp set
3. Worker's `completed_jobs` counter incremented
4. Client notified with rating prompt

**Response 200** — updated Order object

**Errors**
| Code | Reason |
|------|--------|
| 400  | Order is not in ACCEPTED status |

---

## Order Status Flow

```
Client creates order
        │
        ▼
    PENDING ──────────────────────── Client cancels ──► CANCELLED
        │
        ├── Worker accepts ──► ACCEPTED ──► Worker completes ──► COMPLETED
        │
        └── Worker rejects ──► REJECTED
```

---

## Ratings

### Submit Rating
`POST /api/ratings/`  
**Auth:** Required — Client only

**Request**
```json
{
  "order": 5,
  "stars": 5,
  "review": "Excellent work, very professional!"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `order` | ✅ | ID of a COMPLETED order belonging to this client |
| `stars` | ✅ | Integer 1–5 |
| `review` | ❌ | Optional text review |

**Response 201**
```json
{
  "id": 1,
  "order": 5,
  "stars": 5,
  "review": "Excellent work!",
  "created_at": "2024-01-15T12:00:00Z"
}
```

**Side effect:** worker's `average_rating` is recalculated immediately.

**Errors**
| Code | Reason |
|------|--------|
| 403  | Not a client |
| 400  | Order not completed, already rated, wrong client, stars out of range |

---

## Favorites

### List My Favorites
`GET /api/favorites/`  
**Auth:** Required — Client only

**Response 200**
```json
[
  {
    "id": 1,
    "worker_info": {
      "id": 2, "username": "worker1", "role": "worker", ...
    },
    "created_at": "2024-01-15T09:00:00Z"
  }
]
```

---

### Add Favorite
`POST /api/favorites/`  
**Auth:** Required — Client only

**Request**
```json
{ "worker_id": 2 }
```

**Response 201** — Favorite object

**Errors**
| Code | Reason |
|------|--------|
| 400  | Already in favorites, user is not a worker |

---

### Remove Favorite
`DELETE /api/favorites/<id>/`  
**Auth:** Required — Client only

**Response 204** No Content

---

## Notifications

### List My Notifications
`GET /api/notifications/`  
**Auth:** Required

**Response 200** — newest first
```json
[
  {
    "id": 1,
    "title": "Order Accepted ✅",
    "message": "worker1 accepted your order #5.",
    "type": "push",
    "is_read": false,
    "created_at": "2024-01-15T10:10:00Z"
  }
]
```

**Notification types:** `push`, `in_app`, `email`

---

### Mark One as Read
`POST /api/notifications/<id>/read/`  
**Auth:** Required

**Response 200** — updated Notification object

---

### Mark All as Read
`POST /api/notifications/read-all/`  
**Auth:** Required

**Response 200**
```json
{ "message": "All notifications marked as read." }
```

---

## Payments — Webhook

### Paymob Webhook
`POST /api/payments/webhook/?hmac=<hmac_signature>`  
**Auth:** None — Paymob calls this automatically

This endpoint is called by Paymob after every payment event. You must register this URL in your Paymob dashboard under **Settings → Notifications → Transaction processed callback**.

The URL must be publicly accessible (not localhost).

---

## Notification Events Reference

| Event | Who receives | Type |
|-------|-------------|------|
| Order created | All available workers in the category | push |
| Client chose a specific worker | That worker | push |
| Order accepted | Client | push |
| Order rejected | Client | in_app |
| Order cancelled | Worker (if assigned) | in_app |
| Order completed | Client | push |

---

## Error Response Format

All errors return a consistent JSON format:
```json
{ "error": "Human-readable error message." }
```

Validation errors from serializers:
```json
{
  "worker_id": ["This worker is not currently available."],
  "service_category": ["This field is required."]
}
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted (no body) |
| 400 | Bad request / validation error |
| 401 | No token or token expired |
| 403 | Authenticated but not permitted |
| 404 | Resource not found |

---

## Flutter Quick Start

```dart
// 1. Store tokens after login
final prefs = await SharedPreferences.getInstance();
await prefs.setString('access_token', response['tokens']['access']);

// 2. Add to every request
final headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ${prefs.getString("access_token")}',
};

// 3. Refresh when you get 401
if (response.statusCode == 401) {
  final refresh = await http.post(
    Uri.parse('$baseUrl/auth/token/refresh/'),
    body: json.encode({'refresh': prefs.getString('refresh_token')}),
    headers: {'Content-Type': 'application/json'},
  );
  final newAccess = json.decode(refresh.body)['access'];
  await prefs.setString('access_token', newAccess);
}

// 4. Browse workers for a category
final workers = await http.get(
  Uri.parse('$baseUrl/workers/?category=1&page=1'),
);

// 5. Create an order (with chosen worker)
final order = await http.post(
  Uri.parse('$baseUrl/orders/'),
  headers: headers,
  body: json.encode({'service_category': 1, 'worker_id': 2}),
);

// 6. Show Paymob iframe using payment_key
final paymentKey = json.decode(order.body)['payment_key'];
// Navigate to WebView with:
// https://accept.paymob.com/api/acceptance/iframes/<IFRAME_ID>?payment_token=<paymentKey>
```
