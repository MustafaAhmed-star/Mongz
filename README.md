# Mongz
> Django REST API providing authentication and endpoints for workers, categories, ratings, favorites, notifications, and payments webhooks.

- **Language/framework**: Python; Django `>=4.2,<5.0`; Django REST Framework `>=3.15`
- **Auth**: JWT via `djangorestframework-simplejwt >=5.3`
- **Database driver**: `psycopg2-binary >=2.9` (PostgreSQL)
- **CORS**: `django-cors-headers >=4.3`
- **HTTP client**: `requests >=2.31`
- **Gotchas / constraints**:
  - `manage.py` appends the `core/` directory to `sys.path` before executing Django management commands (see [`manage.py`](manage.py)).
  - `core/wsgi.py` also mutates `sys.path` by appending the directory containing `core/wsgi.py` (see [`core/wsgi.py`](core/wsgi.py)).
  - Favorites enforce uniqueness per `(client, worker)` pair via `unique_together` (see [`core/apps/favorites/models.py`](core/apps/favorites/models.py)).

## Architecture
- Django project package: `core`
- Entry points:
  - Management commands: [`manage.py`](manage.py)
  - WSGI: [`core/wsgi.py`](core/wsgi.py) (`DJANGO_SETTINGS_MODULE=core.settings`)
  - ASGI: [`core/asgi.py`](core/asgi.py) (`DJANGO_SETTINGS_MODULE=core.settings`)
- App layout (under `core/apps/`):
  - `favorites` (model + admin)
  - `notifications` (admin registered)
  - Additional apps are implied by routing: `users`, `workers`, `ratings`, `payments`

## API
Top-level routing (from `core/urls.py`):
- `admin/`
- `api/`

App routes:
- Workers (`core/apps/workers/urls.py`):
  - `categories/`
  - `categories/create/`
  - `workers/`
  - `workers/create/`
  - `workers/me/`
  - `workers/<int:pk>/`
- Users/Auth (`core/apps/users/urls.py`):
  - `auth/register/`
  - `auth/login/`
  - `auth/token/refresh/`
  - `users/me/`
- Ratings (`core/apps/ratings/urls.py`):
  - `ratings/`
- Payments (`core/apps/payments/urls.py`):
  - `payments/webhook/`
- Notifications (`core/apps/notifications/urls.py`):
  - `notifications/`
  - `notifications/read-all/`
  - `notifications/<int:pk>/read/`
- Favorites (`core/apps/favorites/urls.py`):
  - `favorites/`
  - `favorites/<int:pk>/`

Favorites views (declared as DRF `APIView` classes):
- `FavoriteListCreateView`: `GET` + `POST` (see [`core/apps/favorites/views.py`](core/apps/favorites/views.py))
- `FavoriteDeleteView`: `DELETE` (see [`core/apps/favorites/views.py`](core/apps/favorites/views.py))

## Data Model
### Favorite
Defined in [`core/apps/favorites/models.py`](core/apps/favorites/models.py):
- `client`: `ForeignKey(User)` with `related_name="favorites"`
- `worker`: `ForeignKey(User)` with `related_name="favorited_by"`
- `created_at`: `DateTimeField(auto_now_add=True)`
- Constraint: `unique_together = ["client", "worker"]`

## Dependencies
Pinned in [`requirements.txt`](requirements.txt):
- `Django >=4.2,<5.0`
- `djangorestframework >=3.15`
- `djangorestframework-simplejwt >=5.3`
- `django-cors-headers >=4.3`
- `psycopg2-binary >=2.9`
- `requests >=2.31`

## Getting Started
Install dependencies:
```bash
python -m pip install -r requirements.txt
```

Run management commands via `manage.py`:
```bash
python manage.py runserver
```

