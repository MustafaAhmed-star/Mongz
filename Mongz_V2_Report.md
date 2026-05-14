# Mongz V2 Repair Report

## English Summary

I reviewed the Django backend, the Flutter app shell, and the audit report. The main goal was to make the backend safer and runnable, connect the missing API routes, remove secrets from code, fix database/model problems, and make the Flutter project stop pointing at missing files.

### What I Fixed And Why

1. Registered missing order URLs.
   - Problem: `orders` routes existed but were not included in `core/urls.py`.
   - Why this matters: without this, `/api/orders/` and order actions could never be reached by the app.

2. Moved secrets to environment variables.
   - Problem: `SECRET_KEY`, `PAYMOB_API_KEY`, and `PAYMOB_HMAC_SECRET` were hardcoded.
   - Fix: added `python-decouple`, changed `settings.py` to read from `.env`, and added `.env.example`.
   - Why this matters: secret keys should not be pushed to GitHub because anyone with them can attack or abuse the app.

3. Added safer production settings.
   - `DEBUG` now comes from environment variables.
   - `ALLOWED_HOSTS` now comes from environment variables.
   - CORS can also be configured from environment variables.

4. Fixed Django app import structure.
   - Problem: the project mixed `apps.users` and `core.apps.users`.
   - Why this matters: Django can accidentally load the same model twice under different names, which breaks tests and can break runtime.
   - Fix: normalized app paths to `core.apps...`.

5. Added login/register rate limiting.
   - Problem: login and register endpoints had no request limit.
   - Fix: added `django-ratelimit`.
   - Why this matters: this slows down brute-force password guessing.

6. Made email unique without breaking users who do not provide email.
   - Problem: email was not unique.
   - Extra problem: many users may have blank email.
   - Fix: email is now nullable and unique, and blank email is converted to `NULL`.
   - Why this matters: real emails must be unique, but optional emails should not crash registration.

7. Improved worker category design.
   - Problem: worker skill/category was stored only as text in `profession`.
   - Fix: added optional `service_category` ForeignKey while keeping `profession` for compatibility.
   - Why this matters: ForeignKey links data correctly and avoids spelling problems like `Plumber`, `plumber`, `Plumbing`.

8. Moved worker ranking into the database.
   - Problem: workers were sorted in Python after fetching records.
   - Fix: used database annotation with score formula.
   - Why this matters: databases are better at filtering/sorting, especially when the project grows.

9. Added order fields.
   - Added `description`.
   - Added `scheduled_at`.
   - Why this matters: a real service order needs details and optional schedule time.

10. Fixed order completion crash.
    - Problem: `request.user.worker_profile` could crash if missing.
    - Fix: check that the profile exists before increasing completed jobs.

11. Improved Paymob capture timing.
    - Problem: a worker could accept before Paymob webhook saved the transaction id, so capture was skipped.
    - Fix: webhook now captures later if the order is already accepted and payment is authorized.

12. Renamed notification model field.
    - Problem: field name `type` conflicts with a Python built-in.
    - Fix: renamed it to `notification_type`.
    - API compatibility: serializer still returns `type` to Flutter.

13. Added rating validation.
    - Problem: database allowed invalid star values.
    - Fix: stars must be from 1 to 5 at model level.

14. Fixed favorites serializer context.
    - Problem: the serializer was created without request context.
    - Fix: passed `context={"request": request}`.

15. Cleaned repository junk.
    - Removed tracked `.DS_Store`.
    - Removed tracked `__pycache__` and `.pyc` files.
    - Added ignore rules for local database, virtual environment, and Python cache.

16. Fixed Flutter API route mismatch.
    - Problem: Flutter called `/register/`, `/login/`, `/me/`, but Django exposes `/auth/register/`, `/auth/login/`, `/users/me/`.
    - Fix: updated API config and services.

17. Fixed Flutter missing screens.
    - Problem: `main.dart` imported many screen files that were not in the zip.
    - Fix: added a simple `screens/app_screens.dart` containing placeholder screens.
    - Why this matters: the app now has a route shell that can be expanded instead of failing immediately on missing imports.

18. Removed missing Flutter assets/fonts from `pubspec.yaml`.
    - Problem: `pubspec.yaml` referenced folders and font files that were not included.
    - Fix: removed those declarations until real assets are added.

## Verification

Backend:

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py makemigrations --check
.venv/bin/python manage.py test
```

Result:

```text
System check identified no issues.
No changes detected.
Ran 57 tests in 28.193s
OK
```

Flutter:

```text
flutter: command not found
dart: command not found
```

So I fixed the Flutter files, but could not run `flutter analyze` or build locally because Flutter/Dart are not installed in this environment.

## How To Run The Backend Locally

1. Create a virtual environment:

```bash
python3 -m venv .venv
```

2. Activate it:

```bash
source .venv/bin/activate
```

3. Install packages:

```bash
pip install -r requirements.txt
```

4. Create your real `.env` file from `.env.example`:

```bash
cp .env.example .env
```

5. Edit `.env` and add your real secret values.

6. Apply migrations:

```bash
python manage.py migrate
```

7. Run server:

```bash
python manage.py runserver
```

8. Test API:

```text
http://127.0.0.1:8000/api/auth/register/
http://127.0.0.1:8000/api/auth/login/
http://127.0.0.1:8000/api/orders/
```

## How To Create A Project From Scratch

1. Start with the idea.
   - Example: "clients create service orders, workers accept them, the platform collects commission."

2. Design the database first.
   - User
   - WorkerProfile
   - ServiceCategory
   - Order
   - Payment
   - Rating
   - Notification
   - Favorite

3. Create backend project:

```bash
mkdir my_project
cd my_project
python3 -m venv .venv
source .venv/bin/activate
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers python-decouple
django-admin startproject core .
```

4. Create apps:

```bash
python manage.py startapp users
python manage.py startapp workers
python manage.py startapp orders
python manage.py startapp payments
```

5. Add apps to `INSTALLED_APPS`.

6. Build models.
   - Models are database tables written as Python classes.
   - Example: `Order` model becomes an `orders_order` table.

7. Create serializers.
   - Serializers convert Python/Django objects to JSON and JSON back to Python objects.

8. Create views.
   - Views receive HTTP requests like `GET /api/orders/` or `POST /api/auth/login/`.

9. Create URLs.
   - URLs connect the browser/mobile app path to the correct view.

10. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

11. Add tests.
   - Test models.
   - Test serializers.
   - Test API endpoints.

12. Run tests before pushing:

```bash
python manage.py test
```

13. Create Flutter app:

```bash
flutter create flutter_app
```

14. In Flutter, create:
   - models: data shape
   - services: API calls
   - providers: app state
   - screens: UI pages

15. Connect Flutter to Django.
   - Backend gives JSON.
   - Flutter reads JSON and shows it on screens.

16. Use Git from the first day:

```bash
git init
git add .
git commit -m "initial project"
```

17. Never push secrets.
   - Put secrets in `.env`.
   - Commit `.env.example`.
   - Ignore `.env`.

---

# تقرير إصلاح Mongz V2 بالعربي

## الملخص

راجعت مشروع Django والجزء الخاص بـ Flutter وقرأت تقرير الأخطاء. الهدف كان إصلاح المشاكل المهمة: تشغيل روابط الطلبات، إزالة الأسرار من الكود، تحسين الأمان، إصلاح مشاكل قاعدة البيانات، وتنظيف ملفات المشروع، مع تجهيز Flutter حتى لا يفشل بسبب ملفات ناقصة.

## ماذا أصلحت؟ ولماذا؟

1. أضفت روابط الطلبات `orders` داخل `core/urls.py`.
   - المشكلة: ملفات الطلبات موجودة، لكن Django لا يعرفها.
   - النتيجة: روابط مثل `/api/orders/` أصبحت تعمل.

2. نقلت الأسرار إلى ملف `.env`.
   - المشكلة: مفاتيح مثل `SECRET_KEY` و Paymob كانت مكتوبة داخل الكود.
   - لماذا هذا خطر؟ لأن GitHub قد يكشفها لأي شخص.
   - الحل: استخدمت `python-decouple` وأضفت `.env.example`.

3. جعلت إعدادات الإنتاج أكثر أمانا.
   - `DEBUG` من ملف البيئة.
   - `ALLOWED_HOSTS` من ملف البيئة.
   - CORS من ملف البيئة.

4. وحدت مسارات تطبيقات Django.
   - المشكلة: المشروع كان يستخدم أحيانا `apps.users` وأحيانا `core.apps.users`.
   - هذا يربك Django ويكسر الاختبارات.
   - الحل: استخدمت `core.apps...` في كل المشروع.

5. أضفت Rate Limiting لتسجيل الدخول والتسجيل.
   - الهدف: تقليل محاولات تخمين كلمة المرور.

6. جعلت البريد الإلكتروني فريدا بدون كسر الحسابات القديمة.
   - البريد الحقيقي يجب ألا يتكرر.
   - لكن لو المستخدم لم يضع بريد، نخزنه كـ `NULL` وليس نصا فارغا.

7. حسنت علاقة العامل بالتصنيف.
   - بدلا من الاعتماد على نص فقط مثل `Plumbing`، أضفت علاقة ForeignKey مع `ServiceCategory`.
   - أبقيت `profession` حتى لا ينكسر الكود القديم.

8. نقلت ترتيب العمال حسب النقاط إلى قاعدة البيانات.
   - هذا أسرع وأنظف عندما يزيد عدد العمال.

9. أضفت تفاصيل للطلب.
   - `description`: وصف الطلب.
   - `scheduled_at`: موعد الطلب.

10. منعت كراش عند إكمال الطلب.
    - كان الكود يفترض أن العامل لديه `worker_profile`.
    - الآن يفحص أولا.

11. أصلحت توقيت Paymob.
    - أحيانا العامل يقبل الطلب قبل وصول webhook من Paymob.
    - الآن webhook يستطيع تنفيذ capture لاحقا إذا كان الطلب مقبولا.

12. غيرت اسم حقل الإشعار من `type` إلى `notification_type`.
    - لأن `type` اسم محجوز/مشهور في Python.
    - لكن API ما زال يرجع `type` حتى لا ينكسر Flutter.

13. أضفت تحقق لتقييم النجوم.
    - النجوم يجب أن تكون من 1 إلى 5.

14. أصلحت Serializer الخاص بالمفضلة.
    - أضفت request context.

15. نظفت Git.
    - أزلت `.DS_Store`.
    - أزلت `__pycache__`.
    - أضفت تجاهل لقاعدة البيانات المحلية والبيئة الافتراضية.

16. أصلحت روابط Flutter API.
    - Flutter كان يطلب روابط غير موجودة.
    - الآن يطلب نفس روابط Django.

17. أضفت شاشات Flutter مؤقتة.
    - `main.dart` كان يستورد شاشات غير موجودة.
    - أضفت ملف `app_screens.dart` كبداية قابلة للتوسع.

18. أزلت assets/fonts غير موجودة من `pubspec.yaml`.
    - حتى لا يفشل البناء بسبب ملفات ناقصة.

## كيف تفكر كمبرمج مبتدئ؟

أي مشروع كبير نقسمه إلى أجزاء صغيرة:

1. المستخدمون: من يسجل؟ عميل أم عامل؟
2. التصنيفات: سباكة، كهرباء، نجارة.
3. الطلبات: العميل يطلب خدمة.
4. الدفع: المنصة تحصل على عمولة.
5. الإشعارات: العامل يعرف أن هناك طلبا.
6. التقييم: العميل يقيم العامل.
7. المفضلة: العميل يحفظ العمال المفضلين.

كل جزء له:

- Model: شكل البيانات في قاعدة البيانات.
- Serializer: تحويل البيانات إلى JSON.
- View: تنفيذ المنطق عند الطلب.
- URL: الرابط الذي يستدعي الـ View.
- Tests: اختبارات للتأكد أن كل شيء يعمل.

## كيف تبدأ مشروع من الصفر؟

1. اكتب الفكرة في جملة واحدة.
   - مثال: "تطبيق يربط العملاء بالعمال ويأخذ عمولة."

2. ارسم الجداول قبل البرمجة.
   - User
   - WorkerProfile
   - ServiceCategory
   - Order
   - Payment
   - Rating

3. أنشئ مشروع Django:

```bash
mkdir my_project
cd my_project
python3 -m venv .venv
source .venv/bin/activate
pip install django djangorestframework
django-admin startproject core .
```

4. أنشئ التطبيقات:

```bash
python manage.py startapp users
python manage.py startapp orders
python manage.py startapp workers
```

5. اكتب Models.

6. شغل migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

7. اكتب Serializers.

8. اكتب Views.

9. اربط URLs.

10. اختبر:

```bash
python manage.py test
```

11. ابدأ Flutter:

```bash
flutter create flutter_app
```

12. قسم Flutter إلى:
    - models
    - services
    - providers
    - screens

13. استخدم Git دائما:

```bash
git init
git add .
git commit -m "initial project"
```

14. لا ترفع الأسرار إلى GitHub.
    - `.env` يبقى على جهازك فقط.
    - `.env.example` يتم رفعه ليعرف الآخرون أسماء المتغيرات.
